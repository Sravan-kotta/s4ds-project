import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './Evaluation.css';


const Evaluation = () => {
  let path2 = useLocation();
  let path3 = path2.state;
  let path4 = path3.fetchedData;
  let file_path = path4.result
  let result = path4.transcript
  console.log(file_path);
  //const {file_path, result, j} = path;
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
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ file_path, result }),
        });

        const data = await response.json();
        console.log(data);
        setEvaluationResult(data.evaluation_result); // Set the result to state
      } catch (err) {
        setError(`Failed to fetch evaluation result: ${err.message}`);

      } finally {
        setIsLoading(false); // Ensure loading is stopped regardless of success/failure
      }
    };

    // Trigger fetching the evaluation result
    fetchEvaluationResult();
  }, []);
  // Empty dependency array means this runs only once when the component mounts

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
