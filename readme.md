# CEN322 - Network Diagnostic and Tool Package

## 📌 Project Overview
This project is a comprehensive **Network Diagnostic and Tool Package** developed for the CEN322 Network Programming course. It integrates multiple standalone network utilities into a single, user-friendly graphical interface (GUI) built with Python's `tkinter` library. 

The application provides hands-on demonstrations of fundamental network operations, socket programming, multi-threading, and error management across different operating systems (Cross-platform support for Windows, Linux, and macOS).

## 🚀 Features (Modules)

*   **Module A: Machine Information**
    *   Retrieves and displays the local machine's hostname.
    *   Fetches network interfaces and active IPv4/IPv6 addresses using OS-level commands (`ipconfig` for Windows, `ip addr` for Linux/Mac).
*   **Module B: Echo Test**
    *   A simple TCP Client/Server architecture.
    *   Sends a text message to a specified port and verifies if the exact same data is echoed back, testing basic connectivity.
*   **Module C: SNTP Time Synchronization**
    *   Connects to an internet NTP server (`time.google.com`) via UDP (Port 123).
    *   Fetches raw binary time packets, unpacks them, calculates the 70-year epoch difference, and synchronizes with the local system time.
*   **Module D: Chat Client/Server**
    *   A fully functional, multi-threaded TCP chat application.
    *   Allows the user to host a server or connect as a client.
    *   All conversations are automatically logged with timestamps to a local `chat_log.txt` file.
*   **Module E: Socket Settings & Error Management**
    *   Demonstrates how to manipulate socket kernel settings such as Send/Receive Buffer sizes (`SO_SNDBUF`, `SO_RCVBUF`) and Timeouts.
    *   Tests and safely catches real-world network exceptions including `socket.timeout`, `ConnectionRefusedError`, and `BlockingIOError` (Non-blocking mode).
*   **Module F: System Logs**
    *   A built-in GUI console that tracks and displays all background system activities, thread launches, and errors.

## 🛠️ Prerequisites & Installation

This project is built using strictly **Python 3 Standard Libraries**. You do not need to install any external packages via `pip`.

The following built-in libraries are utilized:
*   `tkinter` (for the GUI)
*   `socket` (for network connections)
*   `threading` (for preventing GUI freezes during network wait times)
*   `subprocess`, `platform` (for OS-level commands)
*   `struct`, `datetime`, `time` (for packet parsing and time management)

## 💻 How to Run

1. Open a terminal or command prompt.
2. Navigate to the directory containing the project file.
3. Run the application using Python:

```bash
python main.py
# or depending on your OS alias:
python3 main.py
```

## 🧪 Testing Guide

To properly test the **Echo Test (Module B)** or the **Chat Client/Server (Module D)**, you need to simulate two separate entities:

1. **Start the Server:** Open the application, go to the Chat module, select **Role: Server**, and click *Start/Connect*. The server will start listening in the background.
2. **Start the Client:** Open a **second, completely separate terminal window** and run `python main_4.py` again so that you have two application windows side-by-side. On the second window, select **Role: Client** and click *Start/Connect*.
3. You can now send messages between the two windows seamlessly!

## ⚠️ Notes
* **Port Conflicts:** If you abruptly close the application while a server is actively listening, the port (e.g., `65432`) might remain locked by the OS for a few seconds. The code handles this via `SO_REUSEADDR`, but if you encounter an `Address already in use` error, wait a few seconds and try again, or use the built-in *Disconnect* button before closing.
