import socket
import threading
#welcome to server 
print ( f"Hello From Server :) " )
print (f"Use the Command in your chat App" )
print (f"who's is online => to Know online users")
print (f"to => to send private message")
print (f"group => to send message to group of user") 
print(f"send file => to send file user ")
# Connection Data
host = '127.0.0.1'
port = 5566

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
# Sending Messages To All Connected Clients

def broadcast(message):
    for client in clients:
        client.send(message)
        
# Handling Messages From Clients
def handle(client):
    while True:
     
            message = client.recv(1024)
            msg = message.decode('utf-8')
            print(f"  {msg}")
            
            if "who is online" in message.decode('utf-8'):
                nicknames_splited ="," .join(nicknames)   # takes all items in an iterable and joins them into one string والفاصلة الموجودة عشان تفصل بينهم 
                client.send (f' the client are conntected are  {nicknames_splited } \n'.encode("utf-8"))  #هاي الرسالة رح تنطبع بس عند server
           
            elif "send file " in message.decode("utf-8"):
                path = message.decode("utf-8").split("file ")[1]
                file = open (path , "rb" )
                data = file.read (1024)
                if data : 
                    print ("Sending Data ")
                    broadcast(data)
                    print ("Data Send Successfully ")
                    
                    break
            
                else:
                     print ("failed to send data ")
                     break
            
                  #txt = " hey to: nada "
            elif " to: " in message.decode("utf-8"):
                text = message.decode("utf-8").split("to:") #stote the name of the sender , name of receiver
                Sender_nikenames= text[0].split(":")[0].strip()   # text[0] => sender:message =>[0] sender
                actual_message = text[0].split(":")[1].strip()
                receiver_nickname= text[1].split(":")[0].strip() #text[1] reciever
                resiver_index =nicknames.index(receiver_nickname)
                client.send (f'{(Sender_nikenames)} To: ({receiver_nickname}) ({actual_message}) '.encode("utf-8"))
                resiver = clients[resiver_index]
                resiver.send (f'(praivate) from ({Sender_nikenames}) :({actual_message}) '.encode("utf-8"))

         #   s message group: r1, r2
            elif " group: " in message.decode("utf-8"):
                text = message.decode("utf-8").split("group:")
                actual_message = text[0].split(":")[1].strip()
                Sender_nikenames= text[0].split(":")[0].strip()
                rec=text[1].split(":")  #list consist from 1 element have all reciever
                rec_sting=''.join(rec) #make it as string insted of list
                rec_string_split=rec_sting.split(",") #contain array from all reciever
                rec_string_split_length =len(rec_string_split)
                receiver_nickname=[]
                resiver_index=[]
                for i in range(rec_string_split_length):
                    y=text[1].split(",")[i].strip()
                    receiver_nickname.append(y)
                    resiver_index.append(nicknames.index(receiver_nickname[i]))
                    resiver1 = clients[resiver_index[i]]
                    resiver1.send (f'(group) from ({Sender_nikenames}) :({actual_message}) '.encode("utf-8"))
                           
            else:
             broadcast(message) 
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()
#print (clients)
