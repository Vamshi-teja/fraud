# Credit Card Fraud Detection

This project is a full-stack application for detecting fraudulent credit card transactions. It consists of a Python backend (Flask) for machine learning inference and a React frontend for user interaction and dashboard analytics.

## Features

- **Fraud Prediction:** Predicts whether a transaction is fraudulent using a trained machine learning model.
- **Dashboard:** Displays statistics such as total transactions, fraud count, fraud rate, total amount, and average fraud amount.
- **Recent Transactions:** Shows the latest transactions and their fraud status.
- **REST API:** Backend exposes endpoints for transaction prediction and dashboard data.
- **Modern UI:** Frontend built with React and Lucide icons for a clean, responsive interface.

## Project Structure

```
credit card fraud detection/
│
├── backend/                # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├──  ml_model.py         # Trained ML model
│                            # Python dependencies
│
├── frontend/
│   └── fraud/
│       ├── src/
│       │   ├── components/
│       │   │   ├── Dashboard.js
│       │   │   ├── TransactionForm.js
│       │   │   └── ResultDisplay.js
│       │   ├── App.js
│       │   └── App.css
│       ├── public/
│       └── package.json
│
└── README.md               # Project documentation
```

## Getting Started

### Backend Setup

1. Navigate to the backend folder:
   ```sh
   cd backend
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the Flask server:
   ```sh
   python app.py
   ```
   The API will run at `http://localhost:5000`.

### Frontend Setup

1. Navigate to the frontend folder:
   ```sh
   cd frontend/fraud
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the React development server:
   ```sh
   npm start
   ```
   The app will run at `http://localhost:3000`.

### API Endpoints

- `POST /api/predict`  
  Predicts if a transaction is fraudulent.  
  **Request:** JSON with transaction details  
  **Response:** JSON with prediction and confidence

- `GET /api/transactions`  
  Returns recent transactions for dashboard analytics.

## Technologies Used

- **Backend:** Python, Flask, scikit-learn, Pandas, NumPy
- **Frontend:** React, Lucide React (icons), JavaScript, CSS,HTML
- **Other:**  npm
