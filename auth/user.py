import bcrypt
from config.config import db_connection

class User:
    
    def __init__(self, username, password):
        
        self.username = username
        self.password = password

    def hash_password(self):
        
        # Hash the password for secure storage
        salt = bcrypt.gensalt()  # Default rounds are fine for most cases        
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def validate(username):
        
        conn = db_connection()
        query = "SELECT * FROM users WHERE username = %s;"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                user = cursor.fetchone() # Fetch the returned username
                if user:
                    return False, "Username is taken"
                
                return True, ""
            
        except Exception as e:
            
            conn.rollback()
            return False, str(e)  # Return failure and the error message
        
        finally:
            conn.close()

    def save(self):
        
        conn = db_connection()
        query = 'INSERT INTO "users" (username, password) VALUES (%s, %s);'
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (self.username, self.password))
                conn.commit()
                return True  # Return success and the ID of the created user
            
        except Exception as e:
            conn.rollback()
            return False, str(e)  # Return failure and the error message
        
        finally:
            conn.close()

        
    @staticmethod
    def authenticate(username, password):
        
        conn = db_connection()
        query = "SELECT * FROM users WHERE username = %s;"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    return user['id']
                return None
        finally:
            conn.close()