from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from ml_model import FraudDetectionModel
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration - UPDATE WITH YOUR CREDENTIALS
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '######',  # Update with your MySQL password
    'database': 'fraud_detection',
    'buffered': True,  # ← FIX: This prevents "Unread result found"
    'consume_results': True  # ← FIX: This consumes all results automatically
}

# Initialize ML model
try:
    ml_model = FraudDetectionModel()
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print(f"⚠️ ML Model loading error: {e}")
    ml_model = None

def get_db_connection():
    """Get database connection with proper buffering"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        raise

def safe_execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Execute query safely with proper connection handling"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(buffered=True, dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = None
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
            
        # Consume any remaining results
        if cursor.with_rows:
            cursor.fetchall()
            
        connection.commit()
        return result
        
    except Error as e:
        if connection:
            connection.rollback()
        print(f"❌ Query execution failed: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.route('/', methods=['GET'])
def home():
    """Home endpoint to fix 404 error"""
    return jsonify({
        'message': 'Credit Card Fraud Detection API',
        'status': 'running',
        'endpoints': [
            '/api/test-db',
            '/api/predict',
            '/api/transactions',
            '/api/stats'
        ]
    })

# Removed duplicate /api/stats endpoint that referenced undefined Transaction

@app.route('/api/predict', methods=['POST'])
def predict_fraud():
    try:
        data = request.json
        
        if not ml_model:
            return jsonify({'error': 'ML Model not loaded'}), 500
        
        # Extract features for ML model
        features = [
            float(data.get('amount', 0)),
            float(data.get('merchant_category', 1)),
            float(data.get('hour', datetime.now().hour)),
            float(data.get('day_of_week', datetime.now().weekday() + 1)),
            float(data.get('is_weekend', 0)),
            float(data.get('transaction_count_1h', 1)),
            float(data.get('avg_amount_1h', data.get('amount', 0)))
        ]
        
        # Predict fraud
        prediction = ml_model.predict([features])[0]
        probability = ml_model.predict_proba([features])[0]
        
        # Store transaction in database
        safe_execute_query("""
            INSERT INTO transactions 
            (card_number, amount, merchant, location, prediction, probability, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            str(data.get('card_number', '0000'))[-4:],
            float(data.get('amount', 0)),
            str(data.get('merchant', 'Unknown')),
            str(data.get('location', 'Unknown')),
            int(prediction),
            float(max(probability)),
            datetime.now()
        ))
        
        return jsonify({
            'prediction': 'Fraudulent' if prediction == 1 else 'Legitimate',
            'probability': float(max(probability)),
            'risk_level': 'High' if max(probability) > 0.7 else 'Medium' if max(probability) > 0.4 else 'Low'
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        transactions = safe_execute_query("""
            SELECT * FROM transactions 
            ORDER BY timestamp DESC 
            LIMIT 50
        """, fetch_all=True)
        
        if not transactions:
            transactions = []
        
        # Convert datetime objects to strings
        for transaction in transactions:
            if 'timestamp' in transaction and transaction['timestamp']:
                transaction['timestamp'] = transaction['timestamp'].isoformat()
        
        return jsonify(transactions)
        
    except Exception as e:
        print(f"Get transactions error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        # Get all stats in one query to avoid multiple connections
        stats_query = """
        SELECT 
            COUNT(*) as total_transactions,
            SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as fraud_transactions,
            SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END) as legitimate_transactions
        FROM transactions
        """
        
        result = safe_execute_query(stats_query, fetch_one=True)
        
        if not result:
            result = {'total_transactions': 0, 'fraud_transactions': 0, 'legitimate_transactions': 0}
        
        total = result['total_transactions']
        fraud = result['fraud_transactions']
        legitimate = result['legitimate_transactions']
        
        return jsonify({
            'total_transactions': total,
            'fraud_transactions': fraud,
            'legitimate_transactions': legitimate,
            'fraud_rate': (fraud / total * 100) if total > 0 else 0
        })
        
    except Exception as e:
        print(f"Get stats error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask application...")
    print("🔄 Testing database connection...")
    
    try:
        # Test database connection on startup
        test_result = safe_execute_query("SELECT 1 as test", fetch_one=True)
        if test_result:
            print("✅ Database connection successful!")
        else:
            print("⚠️ Database connection test returned no result")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("💡 Please check your MySQL Workbench setup and credentials")
        
    print("🌐 Available endpoints:")
    print("   - http://localhost:5000/ (Home)")
    print("   - http://localhost:5000/api/test-db (Database Test)")
    print("   - http://localhost:5000/api/predict (Fraud Detection)")
    print("   - http://localhost:5000/api/transactions (Transaction History)")
    print("   - http://localhost:5000/api/stats (Statistics)")
    

    app.run(debug=True, port=5000, host='0.0.0.0')
