import socket
import tts

def start_client(host, port) -> tuple:
    ''' Starts client and connects'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    return server

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
    HOST = "192.168.43.248"
    PORT = 12345
    token = ""
    socket.setdefaulttimeout(30)

    voice = tts.Speech()
    voice.set_script("Project_4_Client_Script.txt")

    conn = start_client(HOST, PORT)

    while True:
        token = recv_message(conn, token)
        token = send_message(conn, token, voice)

if __name__ == "__main__":
    main()