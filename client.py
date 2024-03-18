import socket
import tts

current_text = ""

def start_client(host, port) -> tuple:
    ''' Starts client and connects'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    return server

# send_message originally output -> str
def send_message(conn, message: str, voice: tts.Speech) -> tuple:
    if message != "your turn":
        exit()
    try:
        voice.tts_script()
        conn.sendall(bytes(message, "ascii"))
        return "", message
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
        token, current_line = send_message(conn, token, voice) # if incorrect, remove , current_line
        current_text = current_line

if __name__ == "__main__":
    main()
