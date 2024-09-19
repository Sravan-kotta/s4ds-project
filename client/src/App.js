import './App.css';
import Login from './components/Login/Login';
import Home from './components/Home/Home'
import {Route, Routes, Navigate} from 'react-router-dom'
import Evaluation from './components/Evaluation/Evaluation';
function App() {
  return (
    <div className="App">
      <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
        <Route path='Login' element={<Login/>}/>
        <Route path='Home' element={<Home/>}/>
        <Route path='Evaluation' element={<Evaluation/>}/>
      </Routes>
    </div>
  );
}

export default App;

