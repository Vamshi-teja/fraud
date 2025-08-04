import React, { useState } from 'react';
import axios from 'axios';

const TransactionForm = ({ setPrediction, fetchStats }) => {
  const [formData, setFormData] = useState({
    card_number: '',
    amount: '',
    merchant: '',
    location: '',
    merchant_category: '1',
    hour: new Date().getHours(),
    day_of_week: new Date().getDay() + 1,
    is_weekend: [0, 6].includes(new Date().getDay()) ? 1 : 0,
    transaction_count_1h: '1',
    avg_amount_1h: ''
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post('http://localhost:5000/api/predict', {
        ...formData,
        avg_amount_1h: formData.avg_amount_1h || formData.amount
      });
      
      setPrediction(response.data);
      fetchStats(); // Refresh stats
    } catch (error) {
      console.error('Error:', error);
      alert('Error processing transaction. Make sure Flask backend is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="transaction-form">
      <h2>Transaction Details</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Card Number (last 4 digits):</label>
          <input
            type="text"
            name="card_number"
            value={formData.card_number}
            onChange={handleChange}
            placeholder="1234"
            maxLength="4"
            required
          />
        </div>

        <div className="form-group">
          <label>Amount ($):</label>
          <input
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            placeholder="100.00"
            step="0.01"
            required
          />
        </div>

        <div className="form-group">
          <label>Merchant:</label>
          <input
            type="text"
            name="merchant"
            value={formData.merchant}
            onChange={handleChange}
            placeholder="Amazon Store"
            required
          />
        </div>

        <div className="form-group">
          <label>Location:</label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            placeholder="New York, NY"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Merchant Category:</label>
            <select
              name="merchant_category"
              value={formData.merchant_category}
              onChange={handleChange}
            >
              <option value="1">Gas Station</option>
              <option value="2">Grocery Store</option>
              <option value="3">Restaurant</option>
              <option value="4">Online Retail</option>
              <option value="5">Department Store</option>
              <option value="6">ATM</option>
              <option value="7">Hotel</option>
              <option value="8">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Transactions in Last Hour:</label>
            <input
              type="number"
              name="transaction_count_1h"
              value={formData.transaction_count_1h}
              onChange={handleChange}
              min="1"
              max="20"
            />
          </div>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Check Transaction'}
        </button>
      </form>
    </div>
  );
};

export default TransactionForm;