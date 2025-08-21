# Chat Application

This is a modular chat application built with React and TypeScript. The application features a clean and user-friendly interface, allowing users to engage in conversations seamlessly.

## Project Structure

The project is organized into the following main directories and files:

- **src/**: Contains all the source code for the application.
  - **components/**: Contains reusable components for the application.
    - **Sidebar/**: The sidebar component with navigation and user options.
    - **MainPanel/**: The main panel displaying chat content and actions.
    - **ChatInput/**: The input area for typing messages and sending them.
    - **ThemeControls/**: Controls for theme settings (light/dark mode).
    - **Settings/**: Component for managing application settings.
  - **App.tsx**: The main application component that integrates all components.
  - **index.tsx**: The entry point of the application.
  - **types/**: Contains TypeScript types and interfaces used throughout the application.

- **public/**: Contains static files, including the main HTML template.
  - **index.html**: The HTML file that serves as the template for the application.

- **package.json**: Configuration file for npm, listing dependencies and scripts.

- **tsconfig.json**: TypeScript configuration file specifying compiler options.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd chat-app-frontend
   ```

3. Install dependencies:
   ```
   npm install
   ```

4. Start the development server:
   ```
   npm start
   ```

5. Open your browser and go to `http://localhost:3000` to view the application.

## Usage Guidelines

- Use the sidebar to navigate through different chat options.
- The main panel displays the chat interface and suggested questions.
- Type your messages in the chat input box at the bottom of the screen.
- Use the theme controls to switch between light and dark modes.
- Access settings to customize your application preferences.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.