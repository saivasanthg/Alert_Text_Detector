import os

def delete_database(db_name="tweets.db"):
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Database '{db_name}' has been deleted successfully!")
    else:
        print(f"Database '{db_name}' does not exist.")

# Call the function to delete the database
if __name__ == "__main__":
    delete_database()
