from config.config import db_connection
from datetime import datetime

class Claim:
    def __init__(self, insurance_id, claim_date, reason, claim_amount, status, resolution_date=None, id=None):
        self.id = id
        self.insurance_id = insurance_id
        self.claim_date = claim_date
        self.reason = reason
        self.claim_amount = claim_amount
        self.status = status
        self.resolution_date = resolution_date

    def validate(self):
        
        if not isinstance(self.insurance_id, int) or self.insurance_id <= 0:
            return False, "Invalid insurance ID"

        try:
            datetime.strptime(self.claim_date, "%Y-%m-%d")  # Assuming date format is 'YYYY-MM-DD'
        except ValueError:
            return False, "Invalid claim date. Please use the format YYYY-MM-DD"

        if not isinstance(self.claim_amount, (int, float)) or self.claim_amount <= 0:
            return False, "Claim amount must be a positive number"

        valid_claim_statuses = ["Pending", "Approved", "Rejected"]
        if self.status not in valid_claim_statuses:
            return False, f"Claim status must be one of: {', '.join(valid_claim_statuses)}"

        if not isinstance(self.reason, str) or len(self.reason) == 0:
            return False, "Claim reason cannot be empty"

        if self.resolution_date:
            try:
                datetime.strptime(self.resolution_date, "%Y-%m-%d")
            except ValueError:
                return False, "Invalid resolution date. Please use the format YYYY-MM-DD"

        # All validations passed
        return True, "Validation successful"
    
    def save(self):
        
        conn = db_connection()
        query = """
        INSERT INTO claims (insurance_id, claim_date, reason, claim_amount, status, resolution_date)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        values = (self.insurance_id, self.claim_date, self.reason, self.claim_amount, self.status, self.resolution_date)

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                self.id = cursor.fetchone()['id']  # Fetch the newly inserted claim ID
                return True, self.id  # Return the newly inserted claim_id
            
        except Exception as e:
            conn.rollback()
            return None, str(e)
        
        finally:
            conn.close()

    @staticmethod
    def update(claim_id, **kwargs):
        
        conn = db_connection()
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values()) + [claim_id]
        query = f"UPDATE claims SET {set_clause} WHERE id = %s RETURNING id;"

        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
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
        
        conn = db_connection()
        where_clause = " AND ".join([f"{k} = %s" for k in filters.keys()])
        query = (f"SELECT insurance_id, claim_date, reason, claim_amount, status, resolution_date "
        f"FROM claims WHERE {where_clause};" if filters 
        else "SELECT insurance_id, claim_date, reason, claim_amount, status, resolution_date FROM claims;")
        values = list(filters.values())
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                return cursor.fetchall(), None
            
        except Exception as e:
            return None, str(e)
        
        finally:
            conn.close()

    @staticmethod
    def delete(claim_id):
        
        conn = db_connection()
        query = "DELETE FROM claims WHERE id = %s RETURNING id;"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (claim_id,))
                conn.commit()
                deleted_id = cursor.fetchone()
                
                if deleted_id:
                    return True, deleted_id['id']
                else:
                    return False, "Claim record not found"
                
        except Exception as e:
            conn.rollback()
            return False, str(e)
        
        finally:
            conn.close()
