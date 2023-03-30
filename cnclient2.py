import socket
import os.path

PORT = int(input("Enter port number: ")) 
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket created succesfully.")
client.connect((SERVER, PORT))
print('Connection established with the server')

#connections are done

while True:
    
    Action = input("Enter the Action: ")
    client.send(Action.encode())
    
#    if Action != '!DISCONNECT':
#        Filename=input("Enter abcd file name: ")
#        outputfilename="new"+Filename
#        client.send(Filename.encode())

    if Action == 'Download':
        Filename=input("Enter file name: ")
        client.send(Filename.encode())
        filemsg = client.recv(1024).decode()
        
        if filemsg == 'yes':
            outputfilename="new"+Filename
            numlines = int(client.recv(1024).decode())
            print(numlines)
            file = open(outputfilename, 'wb')

            for j in range(0,numlines):
                line = client.recv(1024)
                file.write(line)
            line = client.recv(1024)
            print(line)
            file.write(line)
            file.close()
            print('File has been downloaded succesfully')

        elif filemsg == 'no':
            print(filemsg)
            print("Server does not have the requested file.")

    elif Action == 'Upload':
        Filename=input("Enter file name: ")
        client.send(Filename.encode())
        if os.path.isfile(Filename) == True:
            filemsg = 'yes'
            client.send(filemsg.encode())
            file = open(Filename, 'rb')
            line = file.read(1024)
            while(line):
                client.send(line)
                line = file.read(1024)          
            file.close()
            print('File has been uploaded succesfully!')
            #client.close()
        if os.path.isfile(Filename) == False:
            filemsg = 'no'
            client.send(filemsg.encode())
            print('File not found!')
            #break
    elif Action == "!DISCONNECT":
        client.close()
        break


#    if Action == '!Disconnect':
#        client.close()
#        break     
