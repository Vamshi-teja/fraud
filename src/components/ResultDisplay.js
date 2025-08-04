import React from 'react';

const ResultDisplay = ({ prediction }) => {
  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'High': return '#ff4757';
      case 'Medium': return '#ffa502';
      case 'Low': return '#2ed573';
      default: return '#747d8c';
    }
  };

  const getStatusColor = (status) => {
    return status === 'Fraudulent' ? '#ff4757' : '#2ed573';
  };

  return (
    <div className="result-display">
      <h2>Analysis Result</h2>
      
      <div className="result-card">
        <div className="result-status">
          <span 
            className="status-badge"
            style={{ backgroundColor: getStatusColor(prediction.prediction) }}
          >
            {prediction.prediction}
          </span>
        </div>
        
        <div className="result-details">
          <div className="detail-item">
            <span className="label">Confidence:</span>
            <span className="value">{(prediction.probability * 100).toFixed(2)}%</span>
          </div>
          
          <div className="detail-item">
            <span className="label">Risk Level:</span>
            <span 
              className="value risk-level"
              style={{ color: getRiskColor(prediction.risk_level) }}
            >
              {prediction.risk_level}
            </span>
          </div>
        </div>

        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ 
              width: `${prediction.probability * 100}%`,
              backgroundColor: getRiskColor(prediction.risk_level)
            }}
          />
        </div>
      </div>

      {prediction.prediction === 'Fraudulent' && (
        <div className="warning-message">
          ⚠️ This transaction shows signs of potential fraud. Please review carefully.
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;