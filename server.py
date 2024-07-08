import socket
import threading
import time

clients = {}
rooms = {}
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"Connected to {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break

        message = data.decode().strip()

        if message.startswith("CREATE"):
            room_code = message.split()[1]
            with lock:
                if room_code not in rooms:
                    rooms[room_code] = {'clients': [], 'start': False, 'timings': {}}
                rooms[room_code]['clients'].append(conn)
                clients[conn] = room_code
            print(f"Room {room_code} created")
            conn.sendall(f"Room {room_code} created. Waiting for start signal.".encode())

        elif message.startswith("JOIN"):
            room_code = message.split()[1]
            with lock:
                if room_code in rooms:
                    rooms[room_code]['clients'].append(conn)
                    clients[conn] = room_code
                    print(f"Joined room {room_code}. Waiting for start signal.")
                    conn.sendall(f"Joined room {room_code}. Waiting for start signal.".encode())
                else:
                    conn.sendall(f"Room {room_code} does not exist.".encode())
                    conn.close()
                    return

        elif message.startswith("START"):
            room_code = clients.get(conn)
            if room_code:
                with lock:
                    rooms[room_code]['start'] = True
                print(f"Room {room_code} has started.")
                broadcast(room_code, f"Room {room_code} has started.")

        elif message.startswith("FINISH"):
            room_code = clients.get(conn)
            print("FINISH received")
            if room_code:
                print("room code found")
                temp = message.split('-')
                Name = temp[1]
                Time = temp[2]
                with lock:
                    print(f"timings modified{Name}")
                    rooms[room_code]['timings'][Name] = Time
                    #print(rooms)

                # Check if all clients have finished
                runn=True
                while runn:
                    time.sleep(2)
                    print(len(rooms[room_code]['timings']),len(rooms[room_code]['clients']))
                    with lock:
                        # print(len(rooms[room_code]['timings']))
                        if len(rooms[room_code]['timings']) == len(rooms[room_code]['clients']):
                            timings = rooms[room_code]['timings']
                            sorted_timings = {k: v for k, v in sorted(timings.items(), key=lambda item: item[1])}
                            response = ""
                            for key, value in sorted_timings.items():
                                response += f"{key} {value}-"
                            print(f"broadcasting to {Name}")
                            broadcast(room_code, response)
                            return
            print("exited")

def broadcast(room_code, message):
    print(message)
    print(f"the no of clients are{len(rooms[room_code]['clients'])}")
    # runn=True
    # while runn:
    time.sleep(2)
    # with lock:
    for client in rooms[room_code]['clients']:
        print("a")
        #print(message,client)
        try:
            client.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to client: {e}")
    return

def main():
    host = '127.0.0.1'
    port = 8888

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Serving on {host}:{port}")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
