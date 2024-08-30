# Activity Tracker Application

## Overview

This project is a comprehensive activity tracking application that monitors user activity, captures screenshots at specified intervals, and uploads them to Dropbox. It also tracks mouse clicks and keyboard presses, and offers options to configure screenshot settings and handle errors gracefully.

## Features

- **Automatic Screenshot Capture**: Capture screenshots at configurable intervals.
- **Activity Tracking**: Monitors mouse clicks and keyboard presses.
- **Dropbox Integration**: Upload screenshots to Dropbox.
- **Error Handling**: Handles network issues, application disconnections, and firewall restrictions.
- **GUI Interface**: A user-friendly GUI to start/stop tracking, configure settings, and manually upload files.

## Table of Contents

1. [Installation](#installation)
2. [Dependencies](#dependencies)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Optional and Advanced Features](#optional-and-advanced-features)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/activity-tracker.git
    cd activity-tracker
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Dependencies

This project relies on the following third-party libraries:

- **`tkinter`**: For the GUI.
- **`Pillow`**: For capturing screenshots.
- **`dropbox`**: For uploading screenshots to Dropbox.
- **`pynput`**: For tracking mouse and keyboard activity.
- **`pyinstaller`**: For creating standalone executables (optional).

You can find the full list of dependencies in the `requirements.txt` file.

## Configuration

1. **Dropbox Access Token**:
    - Replace the placeholder in `data_upload.py` with your actual Dropbox access token.

2. **Configuration Settings**:
    - Modify `config.py` to set default values for screenshot intervals, blur settings, and time zone.

3. **GUI Settings**:
    - In the GUI, you can configure the screenshot interval and whether to blur screenshots.

## Running the Application

1. **Start the GUI**:
    ```bash
    python gui.py
    ```

2. **In the GUI**:
    - Enter the desired screenshot interval in seconds.
    - Check or uncheck the blur screenshots option.
    - Click "Start Tracking" to begin monitoring activity and capturing screenshots.
    - Click "Stop Tracking" to halt activity monitoring.
    - Use "Manual Upload" to upload files manually to Dropbox.

3. **Stopping the Application**:
    - Use the GUI "Stop Tracking" button or close the application window.

## Optional and Advanced Features

- **Error Handling**:
    - The application handles network issues by retrying uploads when the connection is restored.
    - It safely handles abrupt disconnections and firewall restrictions.

- **Timezone Management**:
    - Detects and adjusts timestamps based on system timezone changes.

- **Activity Differentiation**:
    - Differentiates genuine user input from scripted activity emulators.

## Testing

### Unit Tests

1. **Create Test Cases**:
    - Write unit tests for individual functions and methods in your modules.

2. **Run Unit Tests**:
    ```bash
    pytest tests/
    ```

### Integration Tests

1. **Set Up Integration Tests**:
    - Create test cases that involve interactions between multiple components.

2. **Run Integration Tests**:
    ```bash
    pytest --integration tests/
    ```

## Troubleshooting

- **Application Doesn't Start**:
  - Ensure all dependencies are installed and the virtual environment is activated.

- **Screenshot Upload Issues**:
  - Verify that the Dropbox access token is correct and has the required permissions.

- **GUI Errors**:
  - Make sure you're using a compatible version of Python and Tkinter.


