import React, { useState, useEffect } from 'react';

const Evaluation = () => {
  const [evaluationResult, setEvaluationResult] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Initialize as false
  const [error, setError] = useState('');

  useEffect(() => {
    // Function to fetch evaluation result from backend
    const fetchEvaluationResult = async () => {
      setIsLoading(true); // Show loading before fetch
      setError(''); // Clear previous error if any

      try {
        const response = await fetch('http://127.0.0.1:5000/evaluation', {
          method: 'POST', // Make a POST request, as required by the backend
        });

        if (!response.ok) {
          // Throw error with the status code and message
          throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        setEvaluationResult(data.evaluation_result); // Set the result to state
      } catch (err) {
        setError(`Failed to fetch evaluation result: ${err.message}`);
      } finally {
        setIsLoading(false); // Ensure loading is stopped regardless of success/failure
      }
    };

    // Trigger fetching the evaluation result
    fetchEvaluationResult();
  }, []); // Empty dependency array means this runs only once when the component mounts

  return (
    <div>
      <h2>Evaluation Result</h2>
      {isLoading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>Error: {error}</p>
      ) : (
        <div>
          <h3>Result:</h3>
          <p>{evaluationResult ? evaluationResult : 'No result available yet.'}</p>
        </div>
      )}
    </div>
  );
};

export default Evaluation;
