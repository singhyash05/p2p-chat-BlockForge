import socket
import threading
import sys

active_peers = {}  # Key: "IP:PORT", Value: team name
peer_listening_ports = {} # For Epheral
IP = socket.gethostbyname(socket.gethostname())  # IP of Client Connecting

## Input PORT on which server will RUN
PORT = int(input("Enter the PORT number: "))

team_name = input("Enter your team name (as mentioned in your form): ").strip()

print(f"Peer running on PORT : {PORT}")

MANDATORY_PEERS = [
    ("10.206.4.122", 1255),
    ("10.206.5.228", 6555)
]

# Client Socket Initialized
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (IP, PORT)

print(f"Connected via IP : {ADDR}")

try:
    server.bind(ADDR)
except Exception as e:
    print("Error binding to port:", e)
    sys.exit(1)


def receiver(conn, addr):
    try:
        message = conn.recv(1024).decode().strip()
        if message:
            # Expecting message format: "<sender_IP:sender_PORT> <team_name> <message_text>"
            parts = message.split(maxsplit=2)
            if len(parts) < 3:
                print("Received improperly formatted message:", message)
            else:
                sender_info, sender_team, msg_body = parts
                sender_ip, sender_port = sender_info.split(":")
                sender_port = int(sender_port)

                if sender_ip not in peer_listening_ports:
                    peer_listening_ports[sender_ip] = sender_port  

                fixed_peer_info = f"{sender_ip}:{peer_listening_ports[sender_ip]}"
                active_peers[fixed_peer_info] = sender_team

                print(f"\nReceived from {fixed_peer_info} ({sender_team}): {msg_body}")
                print("\nEnter Choice :")

        conn.close()
    except Exception as e:
        print("Error in receiver thread:", e)


def send_to_mandatory_peers(full_message):
    """ Sends message to mandatory peers """
    for ip, port in MANDATORY_PEERS:
        try:
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_socket.settimeout(7)
            sender_socket.connect((ip, port))
            sender_socket.sendall(full_message.encode())
            sender_socket.close()
            print(f"Sent to mandatory peer {ip}:{port}")
        except Exception as e:
            print(f"Failed to send to {ip}:{port}: {e}")


def check_connected_peers():
    """ Sends a ping to all stored peers and removes inactive ones """
    print("\nChecking connected peers...")

    active_list = []

    for peer_info, peer_team in list(active_peers.items()):
        peer_ip, peer_port = peer_info.split(":")
        peer_port = int(peer_port)

        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(1)
            test_socket.connect((peer_ip, peer_port))
            test_socket.close()
            active_list.append(f"('{peer_team}', '{peer_info}')")

        except Exception:
            del active_peers[peer_info]

    if active_list:
        print("\nActive Peers: [", ", ".join(active_list), "]")
    else:
        print("\nNo connected peers.")


def connect_to_active_peers():
    """ Connects to all active peers and sends a handshake message """
    print("\nAttempting to connect to active peers...")

    for peer_ip, peer_port in peer_listening_ports.items():  
        try:
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_socket.connect((peer_ip, peer_port))
            handshake_message = f"{IP}:{PORT} {team_name} CONNECTING"
            sender_socket.sendall(handshake_message.encode())
            sender_socket.close()
            print(f"Connected to {peer_ip}:{peer_port}")
        except Exception as e:
            print(f"Failed to connect to {peer_ip}:{peer_port}: {e}")


def handle_connections():
    while True:
        conn, addr = server.accept()
        thread_receive = threading.Thread(target=receiver, args=(conn, addr))
        thread_receive.start()


# Main function
def main():
    server.listen()
    thread_recieve_message = threading.Thread(target=handle_connections, daemon=True)
    thread_recieve_message.start()

    while True:

        print("\n<====== ***** Menu ***** =======>")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Connect to active peers")
        print("0. Quit")
        choice = input("Enter Choice : ")

        if choice == "1":
            recipient_ip = input("Enter the recipient's IP address: ").strip()
            try:
                recipient_port = int(input("Enter the recipient's port number: ").strip())
            except ValueError:
                print("Invalid port number. Returning to menu.")
                continue
            msg = input("Enter your message: ").strip()
            full_message = f"{IP}:{PORT} {team_name} {msg}"

            try:
                sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sender_socket.connect((recipient_ip, recipient_port))
                sender_socket.sendall(full_message.encode())
                sender_socket.close()
                print(f"Sent exit message to {recipient_ip}:{recipient_port}")

                send_to_mandatory_peers(full_message)

            except Exception as e:
                print("Failed to send message:", e)

        elif choice == "2":
            check_connected_peers()

        elif choice == "3":
            connect_to_active_peers()

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3 or 0.")


main()
