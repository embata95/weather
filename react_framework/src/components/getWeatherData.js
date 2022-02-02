import axios from 'axios';

function fetch_data({ addData }) {
    axios.get(`http://127.0.0.1:8080/weather-info/`)
      .then(res => {
        const data = res.data;
        addData(data);
      })
  }

export default fetch_data;