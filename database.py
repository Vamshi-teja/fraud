import mysql.connector
from mysql.connector import Error

# Database configuration - UPDATE WITH YOUR CREDENTIALS
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vamshi3405$',  # Update this
    'database': 'fraud_detection'
}

def test_connection():
    """Test database connection only - no creation"""
    try:
        print("🔄 Testing connection to existing database...")
        
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            print("✅ Connected to MySQL database successfully!")
            
            cursor = connection.cursor()
            
            # Test if our table exists
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Available tables: {tables}")
            
            # Test sample data
            cursor.execute("SELECT COUNT(*) FROM transactions")
            count = cursor.fetchone()[0]
            print(f"📊 Transaction records: {count}")
            
            cursor.close()
            connection.close()
            print("🔒 Connection closed successfully")
            return True
            
    except Error as e:
        print(f"❌ MySQL Error: {e}")
        print(f"💡 Make sure:")
        print(f"   - MySQL Workbench database is created")
        print(f"   - Credentials in DB_CONFIG are correct")
        print(f"   - MySQL service is running")
        return False
        
    except Exception as e:
        print(f"❌ General Error: {e}")
        return False

def get_db_connection():
    """Get database connection for the Flask app"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"❌ Connection failed: {e}")
        raise

if __name__ == "__main__":
    print("🧪 Testing database connection...")
    test_connection()