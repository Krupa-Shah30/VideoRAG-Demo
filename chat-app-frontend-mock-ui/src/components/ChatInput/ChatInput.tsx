import React, { useState } from 'react';
// import './ChatInput.css'; // Assuming you have a CSS file for styling

const ChatInput = () => {
    const [message, setMessage] = useState('');
    const [model, setModel] = useState('Model 1');

    const handleSend = () => {
        if (message.trim()) {
            // Logic to send the message
            console.log('Message sent:', message);
            setMessage('');
        }
    };

    return (
        <div className="chat-input">
            <select value={model} onChange={(e) => setModel(e.target.value)} className="model-selector">
                <option value="Model 1">Model 1</option>
                <option value="Model 2">Model 2</option>
                <option value="Model 3">Model 3</option>
            </select>
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                className="message-input"
            />
            <button onClick={handleSend} className="send-button">Send</button>
            <button className="attachment-button">📎</button>
            <button className="search-button">🔍</button>
        </div>
    );
};

export default ChatInput;