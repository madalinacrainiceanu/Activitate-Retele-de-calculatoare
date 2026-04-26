import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
BUFFER_SIZE = 1024
TIMEOUT     = 5

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

este_conectat = False

def trimite_comanda(mesaj: str) -> str:
    try:
        client_socket.sendto(mesaj.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        date_brute, _ = client_socket.recvfrom(BUFFER_SIZE)
        return date_brute.decode('utf-8')
    except socket.timeout:
        return "eroare: serverul nu a raspuns (timeout)"
    except Exception as e:
        return f"eroare la trimitere: {e}"


print("client udp")
print("comenzi disponibile: CONNECT, DISCONNECT, PUBLISH <mesaj>, DELETE <id>, LIST, EXIT\n")

while True:
    try:
        intrare = input(">> ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\ninchid clientul...")
        break

    if not intrare:
        continue

    parti = intrare.split(' ', 1)
    comanda = parti[0].upper()

    if comanda == 'EXIT':
        print("inchid clientul...")
        break

    elif comanda == 'CONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.lower().startswith("ok"):
            este_conectat = True

    elif comanda == 'DISCONNECT':
        raspuns = trimite_comanda(intrare)
        print(raspuns)
        if raspuns.lower().startswith("ok"):
            este_conectat = False

    elif comanda == 'PUBLISH':
        if not este_conectat:
            print("eroare: nu esti conectat. da CONNECT intai.")
            continue
        if len(parti) < 2 or not parti[1].strip():
            print("eroare: nu ai scris nimic dupa PUBLISH.")
            continue
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    elif comanda == 'DELETE':
        if not este_conectat:
            print("eroare: nu esti conectat. da CONNECT intai.")
            continue
        if len(parti) < 2 or not parti[1].strip().isdigit():
            print("eroare: pune un id de tip numar intreg (ex: DELETE 1).")
            continue
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    elif comanda == 'LIST':
        if not este_conectat:
            print("eroare: nu esti conectat. da CONNECT intai.")
            continue
        raspuns = trimite_comanda(intrare)
        print(raspuns)

    else:
        print(f"comanda '{comanda}' nu exista. incearca CONNECT, PUBLISH, LIST etc.")

client_socket.close()
print("am închis socket-ul. pa!")
