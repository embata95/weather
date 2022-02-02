import React, { useState } from 'react';
import axios from 'axios';

function SubscribeForm() {
    const [email, setEmail] = useState("");
    const [response, setResponse] = useState("")
  
    const handleSubmit = e => {
      e.preventDefault();
      if (!email) return;
      console.log(email)
      axios.post(`http://127.0.0.1:8080/subscribe-API/`, {'email': email})
      .then(function (response) {
        setEmail("");
        setResponse(email + " Successfully subscribed!")
      })
      .catch(function (error) {
        setResponse('Bad request!')
      });
      console.log(response)
    };
  
    return (
      <div>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            className="input"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
          <button>Subscribe</button>
        </form>
        {response !== '' ? <h4>{response}</h4> : ''}
    </div>
    )
  }

  export default SubscribeForm;