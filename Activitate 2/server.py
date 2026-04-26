import socket

HOST        = '127.0.0.1'
PORT        = 9999
BUFFER_SIZE = 1024

clienti_conectati = {}
mesaje = {}
mesaj_id_counter = 1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"server pornit pe adresa {HOST}:{PORT}")
print("astept clienti...")

while True:
    try:
        date_brute, adresa_client = server_socket.recvfrom(BUFFER_SIZE)
        mesaj_primit = date_brute.decode('utf-8').strip()

        parti = mesaj_primit.split(' ', 1)
        comanda = parti[0].upper()
        argumente = parti[1] if len(parti) > 1 else ''

        print(f"\n[primit] de la {adresa_client}: '{mesaj_primit}'")

        if comanda == 'CONNECT':
            if adresa_client in clienti_conectati:
                raspuns = "eroare: esti deja conectat."
            else:
                clienti_conectati[adresa_client] = True
                nr_clienti = len(clienti_conectati)
                raspuns = f"ok: te-ai conectat cu succes. clienti activi: {nr_clienti}"
                print(f"[server] s-a conectat un client nou: {adresa_client}")

        elif comanda == 'DISCONNECT':
            if adresa_client in clienti_conectati:
                del clienti_conectati[adresa_client]
                raspuns = "ok: te-ai deconectat. ne auzim!"
                print(f"[server] s-a deconectat clientul: {adresa_client}")
            else:
                raspuns = "eroare: nu esti conectat inca."

        elif comanda in ['PUBLISH', 'DELETE', 'LIST']:
            if adresa_client not in clienti_conectati:
                raspuns = "eroare: nu te-ai conectat la server."
            elif comanda == 'PUBLISH':
                if not argumente:
                    raspuns = "eroare: mesajul nu poate sa fie gol."
                else:
                    mesaje[mesaj_id_counter] = {'text': argumente, 'autor': adresa_client}
                    raspuns = f"ok: am publicat mesajul (id={mesaj_id_counter})"
                    mesaj_id_counter += 1
            elif comanda == 'DELETE':
                if not argumente.isdigit():
                    raspuns = "eroare: id-ul trebuie sa fie un numar intreg."
                else:
                    msg_id = int(argumente)
                    if msg_id not in mesaje:
                        raspuns = f"eroare: nu am gasit niciun mesaj cu id-ul {msg_id}."
                    elif mesaje[msg_id]['autor'] != adresa_client:
                        raspuns = "eroare: nu poti sterge mesajul altcuiva."
                    else:
                        del mesaje[msg_id]
                        raspuns = "ok: am sters mesajul."
            elif comanda == 'LIST':
                if not mesaje:
                    raspuns = "nu exista mesaje publicate momentan."
                else:
                    linii = ["mesaje publicate:"]
                    for msg_id, msg_data in mesaje.items():
                        linii.append(f" id={msg_id}: {msg_data['text']}")
                    raspuns = "\n".join(linii)

        else:
            raspuns = f"eroare: nu recunosc comanda '{comanda}'. incearca: CONNECT, DISCONNECT, PUBLISH, DELETE, LIST"

        server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
        print(f"[trimis] catre {adresa_client}: '{raspuns}'")

    except KeyboardInterrupt:
        print("\n[server] se inchide serverul...")
        break
    except Exception as e:
        print(f"[eroare] a aparut o problema: {e}")

server_socket.close()
print("socket inchis.")
