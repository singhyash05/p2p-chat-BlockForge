# P2P Chat Application - Blockchain Course (CS216)

## Overview
This is a **peer-to-peer (P2P) chat application** developed for **CS216: Introduction to Blockchain**. It enables simultaneous **sending and receiving** of messages, supports **multiple peers**, and allows users to **query and retrieve active peers**. 

## Features
- **Simultaneous Send & Receive**: Uses multithreading to enable real-time communication.
- **Persistent Peer Tracking**: Maintains a list of peers based on messages received.
- **Active Peer Querying**: Users can check which peers are currently online.
- **Ephemeral Port Handling**: Ensures consistent peer identification despite changing ephemeral ports.
- **Mandatory Connection**: Messages are always sent to two predefined IP addresses.

## Mandatory Peer Addresses
Your client must **mandatorily** send messages to the following peers:
- **IP:** 10.206.4.122 **PORT:** 1255
- **IP:** 10.206.5.228 **PORT:** 6555

## Message Format Standardization
To ensure consistency, messages must follow this format:
```
<IP_ADDRESS:PORT> <team_name> <message>
```
Example:
```
10.206.4.201:8080 blockchain hello
```

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/singhyash05/p2p-chat-BlockForge
   ```
2. Navigate to the project directory:
   ```sh
   cd p2p-chat-BlockForge
   ```
3. Run the script:
   ```sh
   python3 p2p_chat.py
   ```
4. Enter your **team name** and **port number** when prompted.

## Usage Instructions
1. Start the chat application.
2. Enter the recipient's IP and port to send messages.
3. Query active peers using the menu.
4. Optionally, connect to active peers.

### Menu Options
```
1. Send message
2. Query active peers
3. Connect to active peers
0. Quit
```

## Handling Ephemeral Ports
- If a peer reconnects using an ephemeral port, it might be misidentified as a new peer.
- The **listening port** of a peer is stored separately to ensure correct reconnection.


## Contributors
- **Team Name:** BlockForge
- **Member 1:** Yash Singh - **Roll Number** 230051019
- **Member 2:** Shorya Kshettry - **Roll Number** 230003070
- **Member 3:** Hardik Bansal  - **Roll Number** 230001031

## References
- [GeeksforGeeks: Socket Programming](https://www.geeksforgeeks.org/socket-programming-cc/)
- [Linux IP Address Guide](https://www.ionos.com/digitalguide/hosting/technical-matters/get-linux-ip-address/)
