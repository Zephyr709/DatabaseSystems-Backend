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


#Meal Log view
def get_meal_view(db: Session):
    sql = text("SELECT * FROM meal_log_view")
    result = db.execute(sql).fetall()
    
    meals = [row._asdict() for row in result]
    
    return meals
#added for search button

def search_table_column_row(db: Session, table, column, searchQ):
    
    if table == 'Users':
        responseFormat = text('userid BIGINT, country TEXT, city TEXT, height NUMERIC(5,2), gender TEXT, weight NUMERIC(5,2), birthdate TIMESTAMP WITH TIME ZONE, email TEXT, name TEXT, nutritiongoal TEXT, macrosplit TEXT, totallogins INT, lastlogin TIMESTAMP, createdat TIMESTAMP, subscriptionid BIGINT, professionalid BIGINT')

    elif table == 'Professional':
        responseFormat = text('professionalid BIGINT, name TEXT, email TEXT, maxseats INT, currentseats INT, subscriptionid BIGINT')

    elif table == 'Subscription':
        responseFormat = text('subscriptionid BIGINT, subscriptiontype TEXT, billingcycle TEXT, startdate TIMESTAMP WITH TIME ZONE, renewaldate TIMESTAMP WITH TIME ZONE, paymentstatus TEXT')

    elif table == 'DailyMealLog':
        responseFormat = text('mealLogId BIGINT, userid BIGINT, foodItemId INT, dateLogged TEXT')
    
    elif table == 'Metrics':
        responseFormat = text('metricsid INT, inputtokenusage INT, outputtokenusage INT, userid INT')

    table = table.lower()

    sql = text(f"""
        SELECT * FROM search_table_col_row(:table_name, :column_name, :search_query) 
        AS result({responseFormat})
    """)
    result = db.execute(sql, {
            "table_name": table,
            "column_name": column,
            "search_query": searchQ
        }).fetchall()
    
    # Convert each row into a dictionary using _asdict() method
    users = [row._asdict() for row in result]
    
    return users