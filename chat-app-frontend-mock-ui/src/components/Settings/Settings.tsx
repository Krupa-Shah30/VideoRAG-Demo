import React from 'react';

const Settings: React.FC = () => {
    return (
        <div className="settings">
            <h2>Settings</h2>
            <div className="setting-option">
                <label htmlFor="notifications">Enable Notifications</label>
                <input type="checkbox" id="notifications" />
            </div>
            <div className="setting-option">
                <label htmlFor="language">Language</label>
                <select id="language">
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                </select>
            </div>
            <div className="setting-option">
                <label htmlFor="theme">Theme</label>
                <select id="theme">
                    <option value="light">Light</option>
                    <option value="dark">Dark</option>
                </select>
            </div>
            <button className="save-settings">Save Settings</button>
        </div>
    );
};

export default Settings;