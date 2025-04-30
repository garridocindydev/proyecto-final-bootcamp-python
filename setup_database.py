import pymysql

def setup_database():
    # First connect without specifying a database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root'
    )
    
    try:
        with connection.cursor() as cursor:
            # Read the SQL file
            with open('flask_app/database/setup.sql', 'r') as file:
                # Split the file into individual statements
                sql_commands = file.read().split(';')
                
                # Execute each command
                for command in sql_commands:
                    # Skip empty commands
                    if command.strip():
                        cursor.execute(command)
                        print(f"Executed: {command[:50]}...")  # Print first 50 chars of each command
                
                connection.commit()
                print("Database setup completed successfully!")
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    setup_database()
