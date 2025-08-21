import React from 'react';
// import { FaSun, FaCog } from 'react-icons/fa';

const ThemeControls: React.FC = () => {
    const toggleTheme = () => {
        // Logic to toggle between light and dark mode
    };

    const openSettings = () => {
        // Logic to open settings
    };

    return (
        <div className="theme-controls">
            <button onClick={toggleTheme} aria-label="Toggle theme">
                {/* <FaSun /> */}
            </button>
            <button onClick={openSettings} aria-label="Open settings">
                {/* <FaCog /> */}
            </button>
        </div>
    );
};

export default ThemeControls;