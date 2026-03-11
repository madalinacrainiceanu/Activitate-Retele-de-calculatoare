import socket

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 1024


def receive_full_message(sock):
    try:
        raw = b""
        while b" " not in raw:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                return None
            raw += chunk

        first_space = raw.index(b" ")
        header = raw[:first_space].decode('utf-8')

        if not header.isdigit():
            return "ERROR: invalid response format"

        message_length = int(header)
        body = raw[first_space + 1:]

        while len(body) < message_length:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                return None
            body += chunk

        return body[:message_length].decode('utf-8')
    except Exception as e:
        return f"ERROR: {e}"


def print_help():
    print("""
Available commands:
  ADD <key> <value>     - add an element
  GET <key>             - get value
  REMOVE <key>          - remove element
  LIST                  - list all elements
  COUNT                 - number of elements
  CLEAR                 - delete all
  UPDATE <key> <value>  - update value
  POP <key>             - return and delete element
  QUIT                  - close connection
  help                  - show this list
""")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server {HOST}:{PORT}. Type 'help' for commands.")

        while True:
            try:
                command = input('client> ').strip()
            except (EOFError, KeyboardInterrupt):
                print("\nClosing client.")
                break

            if not command:
                continue

            if command.lower() == 'help':
                print_help()
                continue

            s.sendall(command.encode('utf-8'))
            response = receive_full_message(s)

            if response is None:
                print("Connection closed.")
                break

            print(f"Server: {response}")

            if command.upper() == 'QUIT':
                break


if __name__ == "__main__":
    main()
