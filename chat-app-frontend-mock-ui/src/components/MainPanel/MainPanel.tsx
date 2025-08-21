import React from 'react';

const MainPanel: React.FC = () => {
    return (
        <div className="main-panel">
            <header className="main-panel-header">
                <h1>Chat Application</h1>
                <div className="action-buttons">
                    <button>Create</button>
                    <button>Explore</button>
                    <button>Code</button>
                    <button>Learn</button>
                </div>
            </header>
            <div className="suggested-questions">
                <h2>Suggested Questions</h2>
                <ul>
                    <li>What is the best way to learn React?</li>
                    <li>How do I manage state in a React application?</li>
                    <li>What are hooks in React?</li>
                    <li>How can I optimize my React app's performance?</li>
                </ul>
            </div>
        </div>
    );
};

export default MainPanel;