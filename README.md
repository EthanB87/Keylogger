# Keylogger

This Python script implements a simple keylogger that tracks keystrokes and sends them via email after a certain number of keystrokes are logged.

## Features

- Records keystrokes in the background while the script is running.
- Logs keystrokes to a file and sends them via email after a specified number of keystrokes are recorded.
- Configurable via `config.ini` file for email settings.
- Supports logging of different log levels for debugging purposes.

## Prerequisites

- Python 3.x installed on your system.
- Required Python packages installed:
    - pip install pynput configparser
- Ensure that you have permissions to run scripts in your system.

## Usage

1. Clone the repository or download the script file (`keylogger.py`).
2. Install the required Python packages using `pip install pynput configparser`.
3. Configure the email settings in the `config.ini` file.
4. Run the keylogger script using Python:- Ensure that you have permissions to run scripts in your system.
5. Press keys on the keyboard to record keystrokes.
6. After a specified number of keystrokes (default: 75), the keystrokes will be logged to a file and sent via email.

## Important Note

- This keylogger script is intended for educational purposes and should only be used with the explicit consent of the computer's owner.

## License

This project is licensed under the [MIT License](LICENSE).
