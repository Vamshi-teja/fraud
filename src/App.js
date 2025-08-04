import React, { useState, useEffect } from 'react';
import './App.css';
import TransactionForm from './components/TransactionForm';
import Dashboard from './components/Dashboard';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [currentView, setCurrentView] = useState('form');
  const [prediction, setPrediction] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ Credit Card Fraud Detection System</h1>
        <nav>
          <button 
            className={currentView === 'form' ? 'active' : ''}
            onClick={() => setCurrentView('form')}
          >
            Check Transaction
          </button>
          <button 
            className={currentView === 'dashboard' ? 'active' : ''}
            onClick={() => setCurrentView('dashboard')}
          >
            Dashboard
          </button>
        </nav>
      </header>

      <main className="main-content">
        {currentView === 'form' && (
          <>
            <TransactionForm 
              setPrediction={setPrediction} 
              fetchStats={fetchStats}
            />
            {prediction && <ResultDisplay prediction={prediction} />}
          </>
        )}
        
        {currentView === 'dashboard' && (
          <Dashboard stats={stats} />
        )}
      </main>
    </div>
  );
}

export default App;