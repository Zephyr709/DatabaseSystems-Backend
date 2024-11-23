from sqlalchemy.orm import Session
from sqlalchemy.sql import text

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
    try:
        # Call the SQL function
        sql     = text("SELECT delete_professional(:prof_id)")
        print(f"Executing SQL: {sql}, with prof_id: {prof_id}")  # Debug log
        db.execute(sql, {"prof_id": prof_id})
        db.commit()  # Commit the transaction
        return f"Professional with ID {prof_id} has been successfully deleted."
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        print(f"Error during deletion: {str(e)}")  # Debug log
        return f"An error occurred: {str(e)}"
    


#Added in branch
def get_specific_user_by_id(db: Session, sUserID: int):
    try:
        # Execute the SQL function to get the user details
        sql = text("SELECT * FROM get_user_by_userid(:sUserID)")
        result = db.execute(sql, {"sUserID": sUserID}).fetchone()

        # Convert the SQL result to a dictionary
        user = result._asdict()
        return user

    except Exception as e:
        # Log or handle exceptions
        print(f"Error fetching user by ID {sUserID}: {str(e)}")
        return f"An error occurred: {str(e)}"  
