import socket
import tts
    
def start_server(host, port) -> tuple:
    ''' Starts server and waits for a connection'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    try:
        server.listen()
        conn, addr = server.accept()
        return conn, addr
    except TimeoutError:
        server.close()
        exit()

def send_message(conn, message: str, voice: tts.Speech) -> str:
    if message != "your turn":
        exit()
    try:
        voice.tts_script()
        conn.sendall(bytes(message, "ascii"))
        return ""
    except IndexError:
        conn.close()
        exit()
    
def recv_message(conn, message) -> str:
    if message != "":
        exit()
    else:
        conn.recv(1024)
        return "your turn"

def main() -> None:
    HOST = "172.20.10.3"
    PORT = 12345
    token = "your turn"
    socket.setdefaulttimeout(30)

    voice = tts.Speech()
    voice.set_script("Spring24Robotics\\Project_4_Server_Script.txt")

    conn, addr = start_server(HOST, PORT)
    while True:
        token = send_message(conn, token, voice)
        token = recv_message(conn, token)
        
if __name__ == "__main__":
    main()