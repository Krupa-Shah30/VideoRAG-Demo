import React from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import MainPanel from './components/MainPanel/MainPanel';
import ChatInput from './components/ChatInput/ChatInput';
import ThemeControls from './components/ThemeControls/ThemeControls';
import './App.css'; // Assuming you have some global styles

const App: React.FC = () => {
    return (
        <div className="app-container">
            <Sidebar />
            <div className="main-content">
                <MainPanel />
                <ChatInput />
            </div>
            <ThemeControls />
        </div>
    );
};

export default App;