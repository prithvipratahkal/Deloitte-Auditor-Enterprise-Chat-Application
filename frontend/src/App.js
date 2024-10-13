import React, { useState } from 'react';
import './App.css';


function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  
  async function handleSend() {
    // Call the gpt api
    if (!prompt.trim()) {
      alert('Please enter a prompt.');
      return;
    }

    try {
      const chatgptAPIEndpoint = 'http://0.0.0.0:8888/tax-chat';

      const res = await fetch(chatgptAPIEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          userPrompt: prompt
        }),
      });

      const data = await res.json();
      console.log(data)
      setResponse(data.response);
    } catch (error) {
      console.error('Error fetching response:', error);
      setResponse('An error occurred while fetching the response.');
    }
  }

  const handleCancel = () => {
    setPrompt('')
    setResponse('')
  }

  const handlePromptChange = (event) => {
    setPrompt(event.target.value)
  }

  return (
    <div className='App'>
      
      {/* Deloitte banner */}
      <header className="App-header">
        <div>Deloitte Auditor Enterprise Chat UI</div>
        <div>Deloitte.</div>
      </header>
      
      {/* Promt */}
      <textarea class="prompt-input" placeholder="Enter your prompt here..." value={prompt} onChange={handlePromptChange}></textarea>

      {/* Buttons */}
      <div className="button-group">
        <button className="button send-button" onClick={handleSend}>Send</button>
        <button className="button cancel-button" onClick={handleCancel}>Cancel</button>
      </div>

      {/* Response */}
      <div className="response-section">
        <h3>Response:</h3>
        <div className="response-content">
          {response || 'No response yet.'}
        </div>
      </div>
      
    </div>
  );
}

export default App;
