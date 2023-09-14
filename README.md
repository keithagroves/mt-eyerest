# Mt. Eyerest

## Overview

Mt. Eyerest is a macOS status bar application designed to remind you to take breaks and rest your eyes during extended computer usage. Built using PyQt6 and Rumps, this application provides an overlay screen that darkens your display, encouraging you to close your eyes for a short break. A bell sound will play when it's time to resume work.

## Features

- Automatically reminds you to take a break every 20 minutes.
- Displays a semi-opaque overlay on the screen with instructions.
- Plays a bell sound to indicate the end of the break period.
- Skip option for immediately resuming work.
- Easily accessible from the macOS status bar.

## Installation

### Prerequisites

- Python 3.x
- PyQt6
- Rumps

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/eyerest.git
    ```

2. Navigate to the directory:
    ```bash
    cd eyerest
    ```

3. Install the required packages:
    ```bash
    pip3 install -r requirements.txt
    ```

4. Add the launch agent plist for running the app at login (optional):
    ```bash
    cp com.eyerest.plist ~/Library/LaunchAgents/
    ```
    Modify `com.eyerest.plist` to include the correct path to your Python script.

5. Run the application:
    ```bash
    python3 eyerest.py
    ```

## Usage

Once the application is running, it will automatically remind you to take a break every 20 minutes. An overlay will appear with a message to close your eyes. You can either wait for the bell sound to resume your work or click the "SKIP" button to immediately close the overlay.

### Menu Options

- **Preferences**: Currently not available
- **Quit**: Closes the application

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.
