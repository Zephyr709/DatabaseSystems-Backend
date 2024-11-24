from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import getRole
def get_users_by_prof_id(db: Session, prof_id: int):
    sql = text("SELECT * FROM get_users_by_prof_id(:prof_id)")
    result = db.execute(sql, {"prof_id": prof_id}).fetchall()
    
    # Convert each row into a dictionary using _asdict() method
    users = [row._asdict() for row in result]
    
    return users

def delete_professional_by_id(db: Session, prof_id: int):
    """
    Deletes a professional by their ID using the SQL function on Supabase.

    Parameters:
        db (Session): SQLAlchemy database session.
        prof_id (int): ID of the professional to delete.

    Returns:
        str: A confirmation message or error message.
    """
    print(getRole())
    if getRole() == "it_admin":
        try:
            # Call the SQL function
            #sql = text("SELECT delete_professional(:prof_id)")
            #print(f"Executing SQL: {sql}, with prof_id: {prof_id}")  # Debug log
            #db.execute(sql, {"prof_id": prof_id})
            #db.commit()  # Commit the transaction
            return f"Professional with ID {prof_id} has been successfully deleted."
        except Exception as e:
            db.rollback()  # Rollback in case of an error
            print(f"Error during deletion: {str(e)}")  # Debug log
            return f"An error occurred: {str(e)}"
    else:
        return f"Access Denied"
    
def get_role_from_db(db: Session, user_id: int):
    # Define the SQL query to fetch the role
    sql = text("SELECT role_name FROM account_roles WHERE user_id = :user_id")
    # Execute the query with the provided user_id
    result = db.execute(sql, {"user_id": user_id}).fetchone()
    # Return the role name if found, otherwise return None
    return result[0] if result else None