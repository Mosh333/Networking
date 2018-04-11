#!/usr/bin/python3

"""
Echo Client and Server Classes

Lab 4 Online Group Chatting Network Application
By Ankur and Moshiur
McMaster University

to create a Client: "python onlineFileShare.py -r client"
to create a Server: "python onlineFileShare.py -r server"

or you can import the module into another file, e.g.,
import EchoClientServer

"""
#Directory in cd C:\Users\howla_000\desktop\4dn4lab4demo
#             python onlineFileShare.py -r client
#             python onlineFileShare.py -r server

########################################################################

import socket
import argparse
import sys
import time
import os
import struct
import threading
import atexit


#from onlineGroupChat_Client import Client#only class is the Client class

########################################################################
# Echo Server class
########################################################################
class Server:

    HOSTNAME = socket.gethostbyname(socket.gethostname()) #"0.0.0.0"
    PORT = 50000        #the CRDP port
    MULTICAST_ADDRESS = "239.0.0.10"
    
    
    RECV_SIZE = 1024
    BACKLOG = 10
    
    MSG_ENCODING = "utf-8"
    chat_room_list = []        #chat list
    multicast_socket_list = [] #chat's corresponding UDP multicast socket
    replay_list = []
    # [["Moshiur: test1", "Ankur: test2", "Moshiur: test3", "Ankur: test4", "Moshiur: test5", "Ankur: test6", 
                    # "Moshiur: test7", "Ankur: test8", "Moshiur: test9", "Ankur: test10", "Moshiur: test11","Ankur: test12"],
                    # ["Barney: test1", "Elmo: test2", "Barney: test3", "Elmo: test4", "Barney: test5", "Elmo: test6", 
                    # "Barney: test7", "Elmo: test8", "Barney: test9", "Elmo: test10"],
                    # ["Thode: test1", "Mill: test2", "Thode: test3", "Mill: test4", "Thode: test5", "Mill: test6", 
                    # "Thode: test7", "Mill: test8"]] 

    def __init__(self):
        self.str_to_send = ""
        #new [["chat1","239.0.0.0","50000"], ["chat2","239.0.0.1","50001"], ["chat3","239.0.0.2","50002"],["chat4","239.0.0.3","50003"]]
        #scrap this [["chat1","239.0.0.0","50000",""], ["chat2","239.0.0.1","50001",""], ["chat3","239.0.0.2","50002",""],["chat4","239.0.0.3","50003","В"]]
        #[ [my chat history1], [my chat history2], [my chat history3], [my chat history4] ]
        #our implementation will use "В" as the delimiter
        #so that client knows when it's done receiving the data
        self.thread_list = []   #to handle multi thread TCP connections
        self.multicast_thread_list = [] #to handle multi thread UDP connections
        self.create_listen_socket()
        self.process_connections_forever()
        print("We are done") #We never leave the self.process_connections_forever()

    def create_listen_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Get socket layer socket options.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket to socket address, i.e., IP address and port.
            self.socket.bind( (Server.HOSTNAME, Server.PORT) )

            # Set socket to listen state.
            self.socket.listen(Server.BACKLOG)
            print("Listening on CRDP port {} ...".format(Server.PORT))

        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                new_client = self.socket.accept()

                # A new client has connected. Create a new thread and
                # have it process the client using the connection
                # handler function.
                new_thread = threading.Thread(target=self.connection_handler,
                                              args=(new_client,))

                # Record the new thread.
                self.thread_list.append(new_thread)

                # Start the new thread running.
                print("Starting serving thread: ", new_thread.name)
                new_thread.daemon = True
                new_thread.start()

        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()
        finally:
            print("Closing server socket ...")
            self.socket.close()
            sys.exit(1)

    def connection_handler(self, client):
        connection, address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(address_port))

        while True:
            recvd_bytes = connection.recv(Server.RECV_SIZE)
            recvd_str = recvd_bytes.decode('utf-8')
            recvd_str = recvd_str.split(" ")


            if recvd_str[0] == "list":
                print("Sending the chat room list to all connections!")
                print("Begin list command, Server.chat_room_list size is: ", len(Server.chat_room_list))
                if(len(Server.chat_room_list)!=0):
                    for i in range(len(Server.chat_room_list)):
                        #print("Printing delimiter of each entry: ", Server.chat_room_list[i][0])
                        for j in range(len(Server.chat_room_list[i])):
                            #print(Server.chat_room_list[i][j])
                            time.sleep(0.2) #this is so ии????
                            if(j==len(Server.chat_room_list[i])-1):
                                self.str_to_send = self.str_to_send + " " + Server.chat_room_list[i][j]
                                print("List method will send, ", self.str_to_send)
                                connection.sendall((self.str_to_send).encode("utf-8"))
                                self.str_to_send = ""
                            elif(j==0):
                                self.str_to_send = Server.chat_room_list[i][j]
                            else:
                                self.str_to_send = self.str_to_send + " " + Server.chat_room_list[i][j]
                                
                            if(i == len(Server.chat_room_list)-1):
                                if(j == len(Server.chat_room_list[0])-1): #any sublist, they are all same size
                                    connection.sendall(("В").encode("utf-8"))
                elif(len(Server.chat_room_list)==0):
                    #time.sleep(0.2)
                    connection.sendall(("List is empty, try again!").encode("utf-8"))
                    connection.sendall(("В").encode("utf-8"))
                print("End list command")
                # message = "list"
                # print(message)
                # message.encode('utf-8')
                # connection.sendall(message.encode('utf-8'))

            elif recvd_str[0] == "create":
                #We will create a chat room given
                # create <chat room name> <address> <port>
                self.new_chat_room_name = recvd_str[1]
                self.new_chat_address = recvd_str[2]
                self.new_chat_port = recvd_str[3]
                isUnique = 1
                #Check if the address and the port are unique
                if(len(Server.chat_room_list)!=0):
                    for i in range(len(Server.chat_room_list)):
                       if(Server.chat_room_list[i][1]==self.new_chat_address): #check second entry (1+1 is 2)
                           isUnique = 0
                           break
                       if(Server.chat_room_list[i][2]==self.new_chat_port): #check third entry (2+1 is 3)    
                           isUnique = -1
                           break
                       if(Server.chat_room_list[i][0]==self.new_chat_room_name): #check third entry (2+1 is 3)
                           isUnique = -2
                elif(len(Server.chat_room_list)==0):
                    isUnique = 1
                if(isUnique == 1):
                    self.create_room_thread()
                    print("Server creating: ", recvd_bytes.decode('utf-8'))
                    connection.sendall(recvd_bytes)
                elif(isUnique == 0):
                    connection.sendall("Try again! Given chat IP address is already being used.".encode('utf-8'))
                elif(isUnique == -1):
                    connection.sendall("Try again! Given chat port is already being used.".encode('utf-8'))
                elif(isUnique == -2):
                    connection.sendall("Try again! Given chat room name is already being used.".encode('utf-8'))
                connection.sendall("В".encode('utf-8')) #make sure to send the delimiter
                
            elif recvd_str[0] == "delete":
                print("Deleting chat room ", recvd_str[1])
                self.delete_chat_room(recvd_str[1],connection) #delete the chat room from server
                #connection.sendall(recvd_bytes)     #for eg "delete bobby69"
                connection.sendall("В".encode('utf-8'))
            elif recvd_str[0] == "replay":
                print("Replaying chat from ", recvd_str[1])
                self.replay_chat(recvd_str[1], connection)
                connection.sendall("В".encode('utf-8'))
            elif recvd_str[0] == "bye":
                #close TCP connection with that client
                #iterate through the thread list, find that connection 
                #and manually close that connection
                #self.thread_list
                print("Closing socket connection")
                sys.exit(0)
            else:
                #print("command not found!!")
                connection.sendall("command not found!!".encode('utf-8'))
  
    def create_room_thread(self):
        new_chat_thread = threading.Thread(target=self.create_room)
        self.multicast_thread_list.append(new_chat_thread)
        new_chat_thread.daemon = True
        new_chat_thread.start()
        
    def create_room(self):
        try:
            print("In create_room")
            # Server.chat_room_list = []        #chat list
            # Server.multicast_socket_list = [] #chat's corresponding UDP multicast socket
            #UDP packet
            #Only listening
            my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)            
            multicast_group_bytes = socket.inet_aton(self.new_chat_address)
            multicast_if_bytes = socket.inet_aton(Server.HOSTNAME)
            multicast_request = multicast_group_bytes + multicast_if_bytes
            my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_request)
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.bind((Server.HOSTNAME,int(self.new_chat_port))) #should this be unique? yes but udp lets you be reuseable
            
            print(self.new_chat_address,int(self.new_chat_port))
            
            
            Server.multicast_socket_list.append(my_socket) #store UDP Socket
            print("I am here")
            
            new_list = []
            new_list.append(self.new_chat_room_name)
            new_list.append(self.new_chat_address)
            new_list.append(self.new_chat_port)
            print(new_list)
            Server.chat_room_list.append(new_list)
            Server.replay_list.append([])
            track_this_chat_room = self.new_chat_room_name #we create once, so this is assigned once and this room will be kept track of
            print("Just before entering create while True:")
            while True:
                try:
                    #keep track of the conversation in this create_room thread
                    alpha_data, beta_adr = my_socket.recvfrom(1024)
                    #print("Received: ", alpha_data.decode('utf-8'), "\n", "Address:", beta_adr[0], " Port: ", beta_adr[1])
                    self.save_chat_replay(alpha_data.decode('utf-8'), track_this_chat_room)
                except Exception as msg:
                    print(str(msg))
                    print(len(msg))
                    if(str(msg)=="[WinError 10038] An operation was attempted on something that is not a socket"):
                        print("Closing room: ", track_this_chat_room)
                    print(msg)
                    break
                except KeyboardInterrupt:
                    print()                  
        except Exception as msg:
            pass
            #print(msg)
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print()        
    
    def delete_chat_room(self, chat_room_to_del, connection):
        index_to_del = 0
        if(len(Server.chat_room_list)==0):
            connection.sendall("There are no existing chat rooms.".encode('utf-8'))     #for eg "delete bobby69"
        else:
            for i in range(len(Server.chat_room_list)):
                #search and delete
                print("value of i is:", i)
                if(Server.chat_room_list[i][0] == chat_room_to_del): #search
                    #index_to_del = i
                    del Server.chat_room_list[i]
                    del Server.replay_list[i]
                    Server.multicast_socket_list[i].close() #close the multicasting UDP socket for that chat room
                    del Server.multicast_socket_list[i] #after closing socket, remove from list
                    break
                #search and delete      
                
    def replay_chat(self, chat_room_replay, connection):
        print("Replaying recent chat from room: ", chat_room_replay)
        index_to_replay = 0
        print(Server.replay_list)
        if(len(Server.chat_room_list)==0):
            connection.sendall("There are no existing chat rooms.".encode('utf-8'))     #for eg "delete bobby69"
        else:
            for i in range(len(Server.chat_room_list)):
                if(Server.chat_room_list[i][0] == chat_room_replay):
                    index_to_replay = i
                    break
            #Now extract the correct replay sublist, printing last 5 entries
            str_msg = ""
            my_str_list = []
            counter = 0
            for i in reversed(Server.replay_list[index_to_replay]):
                my_str_list.append(i)
                counter = counter + 1
                if(counter == len(Server.replay_list[index_to_replay])):
                    break
                if(counter>4):
                    break
            for i in reversed(my_str_list):
                str_msg = i
                time.sleep(0.1)
                connection.sendall(str_msg.encode('utf-8'))   
                
    def save_chat_replay(self, replay_msg, chat_room_replay):
        #this function will store the message that was send over the multicasted UDP socket for the given chat room
        #chat_room_index
        index_to_store_replay = 0
        missing_num_replay_list = 0
        #search the replay_list and find if there is an existing conversation list for the chat_room_replay

        for i in range(len(Server.chat_room_list)):
            if(Server.chat_room_list[i][0] == chat_room_replay):
                index_to_store_replay = i
                break
        Server.replay_list[i].append(replay_msg)
        
########################################################################
# Echo Client class
########################################################################

class Client:
    # Set the server hostname to connect to. If the server and client
    # are running on the same machine, we can use the current
    # hostname.
    HOSTNAME = socket.gethostbyname(socket.gethostname()) #"0.0.0.0"
    Port = 50000 #the CRDP port
    RECV_BUFFER_SIZE = 1024
    MSG_ENCODING = "utf-8"
    

    


    def __init__(self):
        self.msg_to_send_to_chat = ""
        self.current_name = "NewUser" # temporary name
        self.chat_room_name = ""      #current chat room name
        self.chat_mode_thread_list = []
        self.get_socket()
        self.main_menu_forever()

    def get_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            sys.exit(1)
    
    def main_menu_forever(self):
        #note this main menu implies that this client is not connected to the CRDS through TCP
        #if we call "chat <room name>" we will connect to the multicast UDP
        try:
            while True:
                print("Welcome to the client chat, "+self.current_name+"!")
                input_str = input("Options: connect,name <chat name>,chat <chat room name>\n>>")
                input_str_split = input_str.split(" ")
                
                if(input_str_split[0] == "connect"):
                    self.crds_connection() #this function takes care of when "bye" is entered
                elif(input_str_split[0] == "name"):
                    if(input_str=="name"):
                        print("Please specify a username.")
                    elif(input_str=="name "):
                        print("Please specify a username.")
                    elif(input_str!="name"):
                        self.current_name = input_str_split[1]
                        print("Your new username is: ", self.current_name)
                elif(input_str_split[0] == "chat"):
                    #initiate chat with specific multicast udp server/address
                    if(input_str=="chat"):
                        print("Please specify a chat room.")
                    elif(input_str=="chat "):
                        print("Please specify a chat room.")
                    elif(len(input_str_split)==2):
                        my_chat_room = input_str_split[1]
                        self.chat_mode(my_chat_room)
                elif(input_str_split[0] == "exit"):
                    sys.exit(1)
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def crds_connection(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((Client.HOSTNAME, 50000))  #50000
            print("Connected to CRDS!")
            while True: # do always
                self.get_console_input()
                myInput = self.input_text.split(" ")
                if(myInput[0] == "list"):
                    print("Obtaining current chat room directory.")
                    self.connection_send(self.input_text)
                    self.connection_receive()
                elif(myInput[0] == "create"):
                    if(len(myInput)<4):
                        print("Not enough arguments")
                    else:
                        print("Creating chat room", myInput[1], "in address", myInput[2], "and port ", myInput[3])
                        self.connection_send(self.input_text)
                        self.connection_receive()
                elif(myInput[0] == "delete"):
                    if(self.input_text=="delete"):
                        print("Please specify a chat room.")
                    elif(self.input_text=="delete "):
                        print("Please specify a chat room.")
                    elif(self.input_text!="delete"):    #"delete bob's_sketch_room
                        print("Deleting chat room: ", myInput[1])
                        self.connection_send(self.input_text)
                        self.connection_receive()
                        
                elif(myInput[0] == "replay"):
                    if(self.input_text=="replay"):
                        print("Please specify a chat room.")
                    elif(self.input_text=="replay "):
                        print("Please specify a chat room.")
                    elif(self.input_text!="replay"):    #"replay bob's_sketch_room
                        print("Replaying chat room: ", myInput[1])
                        self.connection_send(self.input_text)
                        self.connection_receive()
                elif(myInput[0] == "bye"):
                    # exit loop
                    print("Disconnecting from CRDS!")
                    #text_to_send = self.input_text + self.socket.sock.getsockname()[0] + str(sock.getsockname()[1])
                    self.connection_send(self.input_text)
                    # close socket
                    time.sleep(2)
                    self.socket.close()                    
                    break
                else:
                    print("Invalid command, try again!")

            #While loop upto here

                
        except Exception as msg:
            print(msg)
            sys.exit(1)
            
    def chat_mode(self, my_chat_room):
        try:
            #Main Chatting functionality here
            #first use a similar functionality to "list" to obtain <address> and <port>
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((Client.HOSTNAME, 50000))  #50000
            self.connection_send("list")
            self.my_local_list = []
            self.my_chat_room = my_chat_room
            while True:
                # Receive and print out text. The received bytes objects
                # must be decoded into string objects.
                recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)
                self.my_local_list.append(recvd_bytes.decode("utf-8"))
                    
                if(recvd_bytes.decode("utf-8")=="В"):
                    break
                    
            print("Obtaining current chat room directory.")
            print(self.my_local_list) #just do not touch this until this line completes
            #just access like this self.my_local_list[0]
            #self.my_local_list[0] = 'bob1 239.0.0.0 60000'
            tempArray = self.my_local_list
            for i in range(len(tempArray)):
                if(tempArray[i][0:len(self.my_chat_room)] == self.my_chat_room):
                    break

            data_list = tempArray[i].split(" ")            
            ip_adr_chat = str(data_list[1])
            port_chat = int(data_list[2])
            tuple_data = (ip_adr_chat, port_chat)
            print(ip_adr_chat, port_chat)
            ###############################################################################
            #Maybe we do not need to close it?
            self.connection_send("bye") #"chat" is problem here? yes server side calls sys.exit() after "bye" we need a work around
            #workaround will be this, if command is "bye" and 
            self.socket.close()
            
            #UDP multicast
            #Set to sending and listening
            self.my_chat_UDP_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            ttl = struct.pack('B', 1)
            self.my_chat_UDP_socket .setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL, ttl)
            multicast_group_bytes = socket.inet_aton(tuple_data[0])
            multicast_if_bytes = socket.inet_aton(Client.HOSTNAME)
            multicast_request = multicast_group_bytes + multicast_if_bytes
            self.my_chat_UDP_socket.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP, multicast_request)
            self.my_chat_UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.my_chat_UDP_socket.bind((Client.HOSTNAME, tuple_data[1]))
            #create thread for receiving and sending packets
            send_thread = threading.Thread(target=self.send_multi_UDP_chat,
                                              args=(tuple_data,my_chat_room,)) #tuple_data
            recv_thread = threading.Thread(target=self.recv_multi_UDP_chat,
                                              args=(tuple_data,my_chat_room,))
            # Record the new thread.
            self.chat_mode_thread_list.append(send_thread)
            self.chat_mode_thread_list.append(recv_thread)

            # Start the new thread running.
            send_thread.daemon = True
            recv_thread.daemon = True
            send_thread.start()
            recv_thread.start()
            
            while True:
                if(self.msg_to_send_to_chat=='<ctrl>]'):
                    #print("Breaking now")
                    break
                else:
                    pass
            #print("Entering Chat Mode") #without while True above, iterates the thread functions once then  exits
            #   The two targeted threaded applications are being ran concurrently, one for sending to chat, one for receiving from chat
            #   We should listen/receive for UDP socket multicasts as well as also prompting the user to send
            print()
            print("breaking out of chatting")

        except Exception as msg:
            print(msg)
            #sys.exit(1)
    def send_multi_UDP_chat(self, tuple_data, my_chat_room):
        #while true into try seems to put in infinite loop
        #try into while true loop seems to iterate once

        while True:
            try:
                #prompt and send
                self.msg_to_send_to_chat = input(self.current_name+": ") #prompt first
                if(self.msg_to_send_to_chat == '<ctrl>]'): #<ctrl>]
                    #print("Breaking now!")
                    break
                else:
                    self.msg_to_send_to_chat = self.current_name +": "+ self.msg_to_send_to_chat # Moshiur: hello guys
                    self.msg_to_send_to_chat = self.msg_to_send_to_chat.encode('utf-8')
                    self.my_chat_UDP_socket.sendto(self.msg_to_send_to_chat, tuple_data)
                time.sleep(0.05)
            except Exception as msg:
                print(msg)
            except KeyboardInterrupt:
                print(); exit()
                #sys.exit(0)
    def recv_multi_UDP_chat(self, tuple_data, my_chat_room):
        #receives directly from the multicast port not from server
        while True:
            try:
                #receive and output
                msg_to_output_terminal, msg_addr_terminal = self.my_chat_UDP_socket.recvfrom(1024) #self.socket is the TCP socket we just close b4 reaching here...
                msg_to_output_terminal = msg_to_output_terminal.decode('utf-8')
                if(self.current_name + ": " != msg_to_output_terminal[0:(len(self.current_name)+2)]): #not the same self sending
                    if("Welcome to the client chat, "+self.current_name !=msg_to_output_terminal):
                        msg_to_output_terminal = ">>" + msg_to_output_terminal + "\n" + self.current_name + ": "
                        print()
                        print(msg_to_output_terminal, end='')
                else:
                    msg_to_output_terminal = ">>" + msg_to_output_terminal
                    #print()
                    print(msg_to_output_terminal)
                time.sleep(0.05)
            except Exception as msg:
                print(msg)
            except KeyboardInterrupt:
                print(); exit()
            #sys.exit(0) #or exit()

    def get_console_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered.
        while True:
            self.input_text = input("Options: list, create <room> <adr> <port>, delete <room>, replay <room>, bye\n>>")
            
            if self.input_text != "":
                break
                
    def connection_send(self, myInput): #*arg
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.socket.sendall(myInput.encode("utf-8"))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        #This keeps receiving until it detects "В"
        #All our bookeeping with be based around this
        try:
            while True:
                # Receive and print out text. The received bytes objects
                # must be decoded into string objects.
                recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

                # recv will block if nothing is available. If we receive
                # zero bytes, the connection has been closed from the
                # other end. In that case, close the connection on this
                # end and exit.
                if len(recvd_bytes) == 0:
                    print("Closing server connection ... ")
                    self.socket.close()
                    sys.exit(1)
                if(recvd_bytes.decode("utf-8")[-1:]!="В"):
                    print(recvd_bytes.decode("utf-8"))
                else:
                    break

        except Exception as msg:
            print(msg)
            sys.exit(1)


########################################################################
# Process command line arguments if this module is run directly.
########################################################################

# When the python interpreter runs this module directly (rather than
# importing it into another file) it sets the __name__ variable to a
# value of "__main__". If this file is imported from another module,
# then __name__ will be set to that module's name.

if __name__ == '__main__':
    roles = {'client': Client,'server': Server}
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--role',
                        choices=roles,
                        help='server or client role',
                        required=True, type=str)

    args = parser.parse_args()
    roles[args.role]()

########################################################################
