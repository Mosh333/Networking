#!/usr/bin/python3

"""
Echo Client and Server Classes

Lab 3 Online File Sharing Network Application
By Ankur and Moshiur
McMaster University

to create a Client: "python onlineFileShare.py -r client"
to create a Server: "python onlineFileShare.py -r server"

or you can import the module into another file, e.g.,
import EchoClientServer

"""
#Directory in cd C:\Users\howla_000\desktop\4dn4lab3demo
#             python onlineFileShare.py -r client
#             python onlineFileShare.py -r server

########################################################################

import socket
import argparse
import sys
import time
import os
import threading
import base64
import binascii
import atexit

########################################################################
# Echo Server class
########################################################################

class Server:

    HOSTNAME = "0.0.0.0"
    PORT = 3000
    SOCKET_ADDRESS = (HOSTNAME, PORT)
    MSG_ENCODING = "utf-8"
    BACKLOG = 10
    RECV_SIZE = 1024
    shared_path = "/Users/howla_000/Desktop/4dn4lab3demo/server_file/"
    os.chdir(shared_path) ##change working dir to be local dir
    EOM_BYTE = b"\0"

    def __init__(self):
        self.thread_list = []
        self.fileSize = 0
        self.SOCKET_ADDRESS = ("0.0.0.0",3000)
        self.BACKLOG = 10
        self.PORT = 3000
        self.shared_path = "/Users/howla_000/Desktop/4dn4lab3demo/server_file/"
        print('Current Available Server Files: '+str(os.listdir('/Users/howla_000/Desktop/4dn4lab3demo/server_file/')))
        #print('Creating listen socket')
        self.create_listen_socket()
        #print('Creating broadcast socket')
        self.create_broadcast_socket()
        #print('Processing Connections Forever')
        self.process_connections_forever()

    def create_listen_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.socket.bind(self.SOCKET_ADDRESS)

            self.socket.listen(self.BACKLOG)
            print("Listening for service discovery messages on SDP Port {}...".format(5000))
            print("Listening for file sharing connections on Port {}...".format(3000))

        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                new_client = self.socket.accept()

                new_thread = threading.Thread(target=self.connection_handler,
                                              args=(new_client,))

                self.thread_list.append(new_thread)

                print("Starting New Client Thread: ", new_thread.name)
                new_thread.daemon = True
                new_thread.start()

        except Exception as msg:
            print(msg)
        finally:
            print("Closing Server Socket...")
            self.socket.close()
            sys.exit(1)

    def connection_handler(self, client):
        connection, address_port = client
        print("-" * 72)
        print("Connection Received From {}.".format(address_port))

        while True:
            recvd_bytes = connection.recv(1024)

            recvd_str = recvd_bytes.decode('utf-8')
            print("Received: ", recvd_str)

            recvd = recvd_str.split(" ")

            if recvd[0] == "rlist":
                sendMsg = os.listdir(self.shared_path)
                sendMsg = " ".join(sendMsg)
                sendMsg = sendMsg.encode('utf-8')
                connection.sendall(sendMsg)

            elif recvd[0] == "put":
                #receiveFileFromClient
               filename = recvd[1]
               #filename = (self.shared_path)+filename
               ack_msg = 'ok'
               connection.send(ack_msg.encode('utf-8'))
               fileInServer = open(filename,'wb') #in binary write mode
               #myfilename, myfileReference
               atexit.register(self.deleteRemnants, myfilename = filename, myfileReference = fileInServer) #register deletion of remnants @ exit
               recvd_bytes_total = bytearray()
               print("Receiving File: "+filename)

               try:
                   while True:
                        recvd_bytes_total += connection.recv(Server.RECV_SIZE)
                        print('recvd_bytes_total is: ', len(recvd_bytes_total))
                        if(recvd_bytes_total[-1:] == Server.EOM_BYTE): #if end is a delimiter
                            recvd_msg_bytes = recvd_bytes_total[:-1] #strip off delimiter
                            print('Size of the file is ', len(recvd_msg_bytes))
                            #Decode since received all data
                            fileDataToWrite = base64.b64decode(recvd_msg_bytes) #.decode('utf-8')
                            print(len(fileDataToWrite))
                            #print(fileDataToWrite)
                            fileInServer.write(fileDataToWrite)
                            fileInServer.close()
                            print('Done Saving the File!')
                            break
               except KeyboardInterrupt:
                   print('Deleting remnants of '+filename)
                   os.remove(filename) #delete remnants
                   sys.exit(1)
               except socket.error:
                   print('Deleting remnants of '+filename)
                   os.remove(filename) #delete remnants
                   break
               print("Done Transmission.")

            elif recvd[0] == "get":
                #sendFileToClient
                #recvd[1] == cat.jpg !!!!!!!!!!!
                os.chdir(self.shared_path)
                command = recvd #put cat.jpg
                filename = recvd[1]
                print('fileName is: ', filename)
                with open(filename,"rb") as myFile:
                    f = myFile.read()
                    myByteArray = bytearray(f)
                #myfilename, myfileReference
                atexit.register(self.deleteRemnants, myfilename = filename, myfileReference = myFile)   #register deletion of remnants @ exit
                myFile.close()
                self.fileSize = os.stat(filename).st_size #in bytes
                print(self.fileSize)
                print(os.getcwd())
                base64FileCounter = 0
                begin = 0
                end = 1024
                base64FileData = base64.b64encode(myByteArray) + Server.EOM_BYTE #append b'\0'...
                base64FileSize = len(base64FileData)
                eof = base64FileSize #takes care of append b'\0'
                doneSending = False
                
                print("Sending File: "+filename+"of size "+ str(self.fileSize))
                
                try:
                    #given the file, we will take already byte encoded
                    #data array and send to server, 1024 bytes at a time
                    #note we take care of special case when last 1024 or less bytes
                    #of data with a special case handling if statement
                    while(base64FileCounter <= base64FileSize):
                        if(end != eof):
                            data_to_send = base64FileData[begin:end]
                            connection.send(data_to_send) #send 1024 bytes
                        else: # end == eof
                            data_to_send = base64FileData[begin:end]
                            connection.send(data_to_send) #send 1024 or less bytes
                            print('Transmitted file contents!')
                        if(doneSending == True):
                            break
                        elif(base64FileCounter + 1024 > eof):
                            base64FileCounter = eof
                            end = eof
                            begin += 1024
                            doneSending = True
                        else:
                            base64FileCounter += 1024
                            end += 1024
                            begin += 1024
                except KeyboardInterrupt:
                    print('Deleting remnants of '+filename)
                    os.remove(filename) #delete remnants
                    sys.exit(1)
                except socket.error:
                    #socket closed intermediately by the server
                    #break out, and close it on this end
                    print('Deleting remnants of '+filename)
                    os.remove(filename) #delete remnants
                    sys.exit(1)
                print('Done sending files to client!')
            elif recvd[0] == "purge":
                os.remove(Server.shared_path + recvd[1])
                message = 'Deleted '+recvd[1]+' from server!'
                message = message.encode('utf-8')
                connection.send(message)
            elif recvd[0] == "bye":
                print("Goodbye.")
                print("Connection Closed: {}.".format(address_port))
                #self.thread_list.remove(new_thread) #daemon do we need this?
                connection.close()
                self.process_connections_forever()
                break
            else:
                print("Command Not Known.")
                #connection.close()

    
    def create_broadcast_socket(self):
        HOSTNAME = "0.0.0.0"
        PORT_BROADCAST = 5000
        ADDR_PORT = (HOSTNAME,PORT_BROADCAST)

        try:
            self.broadcast_socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #test if reuse address socket option fixes issue
            self.broadcast_socket_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.broadcast_socket_recv.bind(ADDR_PORT)

            self.broadcast_socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.broadcast_socket_send.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
            print("Created new Thread")
            
            new_broadcast_thread = threading.Thread(target=self.process_broadcast_forever,
                                                    args=(self.broadcast_socket_recv,self.broadcast_socket_send))

            self.thread_list.append(new_broadcast_thread)
            print('size of thread list is ', len(self.thread_list))

            #print("Starting New Broadcast Thread: ", new_broadcast_thread.name)
            new_broadcast_thread.daemon = True
            new_broadcast_thread.start()

        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_broadcast_forever(self, client_recv,client_send):
        MESSAGE = "Ankur & Moshiur's File Sharing Service."
        MESSAGE = MESSAGE.encode('utf-8')
        while True:
            try:
                data, address = client_recv.recvfrom(1024)
                recvd_str = data.decode('utf-8')
                print("Broadcast Received: "+ recvd_str)
                if recvd_str == "SERVICE DISCOVERY": #checks for this UDP packet
                    client_send.sendto(MESSAGE,("255.255.255.255",5001))
                    print("Sending Reply To Broadcast...")
                    print('size of thread list is ', len(self.thread_list))
            except Exception as msg:
                print(msg)
                sys.exit(1)
                
    def deleteRemnants(self, myfilename, myfileReference):
        myfileReference.close() #make sure to close the file first!!!!!!!
        os.remove(myfilename)


########################################################################
# Echo Client class
########################################################################

class Client:

    # Set the server hostname to connect to. If the server and client
    # are running on the same machine, we can use the current
    # hostname.
    SERVER_HOSTNAME = socket.gethostname()
    IP_ADDRESS = "255.255.255.255"
    MSG_ENCODING = "utf-8"
    RECV_SIZE = 1024 #should be enough bits to transfer the data
    EOM_BYTE = b"\0"     # Use a zero byte to signal the end of the message. It is not a
                         # valid Base64 encoding output.
    shared_path = "/Users/howla_000/Desktop/4dn4lab3demo/client_file/"
    os.chdir(shared_path) ##change working dir to be shared local dir

    def __init__(self):
        ##Initialize Some Variables
        self.isConnected = False
        self.fileName = ""
        self.fileSize = 0
        self.shared_path = "/Users/howla_000/Desktop/4dn4lab3demo/client_file/"
        self.ServerIP = ""
        ##Call Class Functions as required
        self.get_console_input()

    def get_console_input(self):
        # In this version we keep prompting the user until
        # either a scan, connect, llist, rlist, put, get, or bye
        # are inputted.
        while True:

            self.input_text = input("Please input a command: ")
            self.input_text_split = self.input_text.split(" ")
            if(self.input_text_split[0]) == "scan":
                print("Command entered: <scan> ")
                self.scanServer()
            elif self.input_text_split[0] == "connect":
                if(self.isConnected == False):
                    ip_adr = str(self.input_text[1])
                    port = self.input_text[2]
                    #192.168.206.1
                    #192.168.2.159
                    ip_adr = "192.168.206.1"
                    port = 3000
                    print("Command entered: <connect> ")
                    print("ServerIp is:", self.ServerIP)
                    self.connectServer(ip_adr, port)
                    self.isConnected = True
                else:
                    print('Already Connected!')
            elif self.input_text_split[0] == "llist":
                print("Command entered: <llist> ")
                self.llist()
            elif self.input_text_split[0] == "rlist":
                if(self.isConnected == False):
                    print("Not connected to the server")
                else:
                    print("Command entered: <rlist> ")
                    self.rlist()
            elif self.input_text_split[0] == "put":
                print("Command entered: <put> ")
                self.fileName = self.input_text_split[1] #filename
                data_to_send = self.input_text ##entire command
                if(self.isConnected == False):
                    print("Not connected to the server")
                else:
                    self.put_fileToServer(data_to_send,self.fileName)
            elif self.input_text_split[0] == "get":
                print("Command entered: <get> ")
                self.fileName = self.input_text_split[1] #filename
                data_to_send = self.input_text ##entire command
                if(self.isConnected == False):
                    print("Not connected to the server")
                else:
                    
                    data_to_send = self.input_text
                    self.get_fileFromServer(data_to_send,self.fileName)
            elif self.input_text_split[0] == "delete":
                os.remove(self.input_text_split[1])
            elif self.input_text_split[0] == "purge":
                self.purge_server_file(self.input_text)
            elif self.input_text_split[0] == "bye":
                if(self.isConnected == False):
                    print("Bye")
                    sys.exit(0)
                else:
                    self.isConnected = False
                    message = "bye"
                    message = message.encode('utf-8')
                    self.tcp_connect.send(message)
                    self.tcp_connect.close()
                    print("Bye")
                    sys.exit(0)
            elif self.input_text != "": #any other text, prompt user
                print("Invalid Command! ")

    ####################FOR SCAN()#######################################
    def scanServer(self):
        MESSAGE = "SERVICE DISCOVERY"
        MESSAGE_ENC = MESSAGE.encode('utf-8')
        ADDR_PORT = ("255.255.255.255", 5000) #Pick 5000 for Broadcast Port
        ADDR_INFO = ("0.0.0.0", 5001)  #Pick 40001 for Address Info

        try:
            ##createSocket()
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            #self.socket.settimeout(5)
            
            ##sendBroadcast()
            self.socket.sendto(MESSAGE_ENC,ADDR_PORT)
            print('BROADCAST SENT...')
            
            ##getSocket() and listen for broadcast reply
            self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #self.broadcast_socket.settimeout(10)
            self.broadcast_socket.bind(ADDR_INFO)
            self.receive_server_resp()
            
        except Exception as msg:
            print(msg)
        except socket.timeout:
            print("No Service Found!")

    def receive_server_resp(self):
        print("Listening for Broadcast Reply from Server")
        while True:
            try:
              print('I am trying')
              data, address = self.broadcast_socket.recvfrom(1024)
              print("Data from server: "+data.decode('utf-8'))
              print("Server's IP Address: "+ address[0])
              self.ServerIP = address[0] #obtain server IP
              if len(data.decode('utf-8'))>0:
                  print('Breaking out of loop')
                  break;
            except Exception as msg:
                print(msg)
                sys.exit(1)
            except socket.timeout:
                print("No Service Found!")
    #####################################################################

    ####################FOR CONNECT()#######################################
    def connectServer(self, ip_adr, port):
        try:
            myPort = int(port)
            #use tcp_connect to send data to server
            self.tcp_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #"192.168.206.1" 3000
            # 192.168.2.159
            self.tcp_connect.connect((ip_adr, myPort))
            print('Connection Success!')
        except Exception as msg:
            print(msg)

    #####################################################################

    def llist(self):
        print(os.listdir(self.shared_path))

    def rlist(self):
        message = "rlist"
        message = message.encode('utf-8')
        self.tcp_connect.send(message)
        serverDir = self.tcp_connect.recv(1024)
        print(serverDir.decode('utf-8'))

    def put_fileToServer(self,datatosend, tempFileName):
        ####Upload
        command = datatosend
        filename = tempFileName #self.shared_path + 
        print('filename is ', str(filename))
        time.sleep(2)
        #given a file name, we generate the
        #byte array which will be later used to generate file at other end
        
        with open(filename,"rb") as myFile:
            f = myFile.read()
            myByteArray = bytearray(f)
        myFile.close()
        #register closing of file during abrupt close
        atexit.register(self.customCloseHandler, myfilename = filename, myfileReference = myFile, myData = myByteArray) 
        self.fileSize = os.stat(filename).st_size #in bytes
        base64FileCounter = 0
        begin = 0
        end = 1024
        print('size of file is: '+str(self.fileSize)+ ' bytes')
        print('length of myByteArray is: ', len(myByteArray))
        prebase64FileSize = len(base64.b64encode(myByteArray))        
        base64FileData = base64.b64encode(myByteArray) + Client.EOM_BYTE #append b'\0'...
        base64FileSize = len(base64FileData)
        print('base64 encoding len is: ', str(base64FileSize))
        eof = base64FileSize #do not need +1 for b'\0'...
        doneSending = False

        #check for server response
        self.tcp_connect.send(command.encode('utf-8')) #include path and file name
        response = self.tcp_connect.recv(1024)
        response = response.decode('utf-8')
        print('Response is: ', response)
        recvd_bytes_total = bytearray()
        if(response == "ok"):
            try:
                print('Starting Transmission!')
                print("progress : "+filename)
                #given the file, we will take already byte encoded
                #data array and send to server, 1024 bytes at a time
                #note we take care of special case when last 1024 or less bytes
                #of data with a special case handling if statement
                while(base64FileCounter <= base64FileSize):
                    progData = base64FileCounter/base64FileSize
                    time.sleep(0.5)
                    self.update_progress(progData)
                    if(end != eof):
                        data_to_send = base64FileData[begin:end]
                        self.tcp_connect.send(data_to_send) #send 1024 bytes
                    else: # end == eof
                        data_to_send = base64FileData[begin:end]
                        #data_to_send = temp_data_to_send + Client.EOM_BYTE   #this should be ok
                        self.tcp_connect.send(data_to_send) #send 1024 or less bytes
                        
                    if(doneSending == True):
                        print('Transmitted file contents!')
                        break
                    elif(base64FileCounter + 1024 > eof):
                        base64FileCounter = eof
                        end = eof
                        begin += 1024
                        doneSending = True
                    else:
                        base64FileCounter += 1024
                        end += 1024
                        begin += 1024


            except KeyboardInterrupt:
                print()
                sys.exit(1)
            except socket.error:
                #socket closed intermediately by the server
                #break out, and close it on this end
                sys.exit(1)
        print('Done uploading files')


    def get_fileFromServer(self,datatorecv, tempFileName):
        ###Download
        #datatorecv is 'C:\User\moshiur\...\server_file'
        #datatorecv wants to get a file from server
        command = datatorecv.encode('utf-8')
        self.tcp_connect.send(command) #sent to server get <filename>
        fileInClient = open(tempFileName,'wb') #in binary write mode
        recvd_bytes_total = bytearray()
        print("Receiving File: "+tempFileName)
        
        try:
            while True:
                recvd_bytes_total += self.tcp_connect.recv(1024)
                if(recvd_bytes_total[-1:] == Server.EOM_BYTE): #if end is a delimiter
                    recvd_msg_bytes = recvd_bytes_total[:-1] #strip off delimiter
                    #Decode since received all data
                    fileDataToWrite = base64.b64decode(recvd_msg_bytes)  #.decode('utf-8')
                    fileInClient.write(fileDataToWrite)
                    fileInClient.close()
                    print('Done Receiving the File!')
                    break
        except KeyboardInterrupt:
            print()
            sys.exit(1)
        except socket.error:
            #socket closed intermediately by the server
            #break out, and close it on this end
            sys.exit(1)
        
    def purge_server_file(self, purgeFile):
        message = purgeFile
        message = message.encode('utf-8')
        self.tcp_connect.send(message)
        recvMsg = self.tcp_connect.recv(1024)
        print(recvMsg.decode('utf-8'))
        
    def customCloseHandler(self, myfilename, myfileReference, myData):
        myFile = open(myfilename,"wb")
        myFile.write(myData)
        myFile.close()
        
    def update_progress(self, progress):
        barLength = 10 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float\r\n"
        if progress < 0:
            progress = 0
            status = "Halt...\r\n"
        if progress >= 1:
            progress = 1
            status = "Done...        \r\n"
        block = int(round(barLength*progress))
        text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
        sys.stdout.write(text)
        sys.stdout.flush()
        



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






