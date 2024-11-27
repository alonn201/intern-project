from config.config import db_connection

class Insurance:
    
    def __init__(self, age=None, sex=None, bmi=None, children=None, smoker=None, region=None, charges=None, id=None):
        
        self.id = id
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.children = children
        self.smoker = smoker
        self.region = region
        self.charges = charges
        
    def validate(self):
        
        if not isinstance(self.age, int) or self.age <= 0:
            return False, "Age must be a positive integer."
        if self.sex not in ['male', 'female']:
            return False, "Sex must be either 'male' or 'female'."
        if not isinstance(self.bmi, (float, int)) or self.bmi <= 0:
            return False, "BMI must be a positive number."
        if not isinstance(self.children, int) or self.children < 0:
            return False, "Children must be a non-negative integer."
        if self.smoker not in ['yes', 'no']:
            return False, "Smoker must be either 'yes' or 'no'."
        if not isinstance(self.region, str) or len(self.region) == 0:
            return False, "Region is required."
        if not isinstance(self.charges, (float, int)) or self.charges < 0:
            return False, "Charge must be a non-negative number."
        return True, ""
    
    def save(self):
        
        conn = db_connection()
        query = """
        INSERT INTO insurance (age, sex, bmi, children, smoker, region, charges)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING uuid;
        """
        values = (self.age, self.sex, self.bmi, self.children, self.smoker, self.region, self.charges)
        try:
            with conn.cursor() as cursor:
                
                cursor.execute(query, values)
                conn.commit()
                self.id = cursor.fetchone()['uuid']                
            return True, self.id
        
        except Exception as e:
            conn.rollback()
            return False, str(e)
        
        finally:
            conn.close()
            
    @staticmethod
    def delete(record_id):

        conn = db_connection()
        query = "DELETE FROM insurance WHERE uuid = %s RETURNING uuid;"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (record_id,))
                conn.commit()
                deleted_id = cursor.fetchone()
                
                if deleted_id:
                    return True, deleted_id['uuid']  # Return both success and ID
                else:
                    return False, "Record not found"
                
        except Exception as e:
            conn.rollback()
            return False, str(e)
        
        finally:
            conn.close()
    
    @staticmethod
    def update(record_id, **kwargs):
        
        conn = db_connection()
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [record_id]
        query = f"UPDATE insurance SET {set_clause} WHERE uuid = %s RETURNING uuid;"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                if cursor.rowcount == 0:
                    # No rows were affected, implying the UUID was invalid
                    return False, "Record not found or no changes made"
                conn.commit()
                updated_id = cursor.fetchone()
                return True, updated_id
            
        except Exception as e:
            conn.rollback()
            return False, str(e)
        
        finally:
            conn.close()
    
    @staticmethod
    def search(filters):
        
        if 'id' in filters:
            try:
                record_id = int(filters['id'])  # Attempt to convert to integer
                if record_id <= 0:
                    return None, "id must be a positive integer"
                
            except ValueError:
                return None, "id must be a valid integer"
    
        conn = db_connection()
        where_clause = " AND ".join([f"{k} = %s" for k in filters.keys()])
        query = (f"SELECT age, sex, bmi, children, smoker, region, charges "
        f"FROM insurance WHERE {where_clause};" if filters 
        else "SELECT age, sex, bmi, children, smoker, region, charges FROM insurance;")
        values = list(filters.values())
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                return cursor.fetchall(), None
            
        except Exception as e:
            return None, str(e)
        
        finally:
            conn.close()