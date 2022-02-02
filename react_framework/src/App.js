import './App.css';
import React, { useState, useEffect } from 'react';
import SubscribeForm from './components/subsribe';
import fetch_data from './components/getWeatherData';
import ShowData from './components/renderWeatherData';


function App() {
  const [weather_data, setWeatherData] = useState([])
  const addData = data => {
    setWeatherData(data)
  }
  useEffect(() => fetch_data({ addData }), [])

  return (
    <div className="App">
      <h1>Hello from the weather app!</h1>
        <ShowData weather_data={weather_data} />
        <SubscribeForm />
    </div>
  );
}

export default App;
