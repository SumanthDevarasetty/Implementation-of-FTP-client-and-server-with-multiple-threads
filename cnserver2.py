import socket
import os.path
import threading

PORT = int(input("Enter port number: ")) 
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket created successfully.")

server.bind((SERVER, PORT))

def handle_client(con, addr):

    print(f"[NEW CONNECTIOIN]{addr} connected.")
    connected = True
    while connected:

        Action = con.recv(1024)
        Action = Action.decode()

        if Action == 'Download':
            Filename = con.recv(1024)
            Filename = Filename.decode()
            if os.path.isfile(Filename) == True:
                filemsg = "yes"
                con.send(filemsg.encode())
                filesize = os.path.getsize(Filename)
                lastline = filesize%1024
                print(lastline)
                numlines = filesize//1024
                con.send(str(numlines).encode())
                file = open(Filename, 'rb')

                for i in range(0,numlines):
                    line = file.read(1024)
                    con.send(line)
                line = file.read(lastline)
                print(line)
                con.send(line)
                file.close()
                print('File has been transferred successfully.')
            else:
                filemsg = "no"
                con.send(filemsg.encode())
                print(f"Client {addr} asked for a non existing file.")  

        if Action == 'Upload':
            Filename = con.recv(1024)
            Filename = Filename.decode()
            filemsg = con.recv(1024)
            filemsg = filemsg.decode()
            if filemsg == 'yes':
                print(filemsg)
                file = open("new"+Filename, 'wb')
                line = con.recv(1024)
                while(line):
                    file.write(line)
                    line = con.recv(1024)
                file.close()
                print('File has been received successfully.')
                #con.close()
            if filemsg == 'no':
                print(filemsg)
                print(f"Client {addr} does not have the file.")    

        if Action == '!DISCONNECT':
            print(f"Client {addr} diconnected.")
            connected = False
            
    con.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        con, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (con, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] server is starting...")
start()