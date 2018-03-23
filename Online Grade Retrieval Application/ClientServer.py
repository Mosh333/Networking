#!/usr/bin/python3

"""
Echo Client and Server Classes

Lab 2 Grade Retrieval Application
By Ankur and Moshiur
McMaster University

to create a Client: "python EchoClientServer.py -r client" 
to create a Server: "python EchoClientServer.py -r server" 

or you can import the module into another file, e.g., 
import EchoClientServer

"""
#Directory in cd C:\Users\howla_000\desktop\4dn4lab2demo
#             python ClientServer.py -r client
#             python ClientServer.py -r server

########################################################################

import socket
import argparse
import sys
import csv
import getpass
import hashlib

########################################################################
# Echo Server class
########################################################################

class Server:

    # Set the server hostname used to define the server socket address
    # binding. Note that 0.0.0.0 or "" serves as INADDR_ANY. i.e.,
    # bind to all local network interface addresses.
    HOSTNAME = "0.0.0.0"

    # Set the server port to bind the listen socket to.
    PORT = 50000

    RECV_BUFFER_SIZE = 1024
    MAX_CONNECTION_BACKLOG = 10
    
    MSG_ENCODING = "utf-8"
    GET_AVERAGES_CMD = "GAC"

    # Create server socket address. It is a tuple containing
    # address/hostname and port.
    SOCKET_ADDRESS = (HOSTNAME, PORT)

    def __init__(self):
        self.msg_to_client = ""
        self.last_row_csv_string = ""
        self.authenticated_flag = 0
        self.printcsvfile() #on server startup, print csv once
        self.create_listen_socket()
        self.process_connections_forever()

    def create_listen_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set socket layer socket options. This allows us to reuse
            # the socket without waiting for any timeouts.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket to socket address, i.e., IP address and port.
            self.socket.bind(Server.SOCKET_ADDRESS)

            # Set socket to listen state.
            self.socket.listen(Server.MAX_CONNECTION_BACKLOG)
            print("Listening on port {} ...".format(Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                # Block while waiting for accepting incoming
                # connections. When one is accepted, pass the new
                # (cloned) socket reference to the connection handler
                # function.
                self.connection_handler(self.socket.accept())
        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()

    def connection_handler(self, client):
        #handle dehashing/decrypting logic here (hide username and password from hackers)
        #handle GAC here
        connection, address_port = client
        print("-" * 72)
        print("Connection received from {}.".format(address_port)) #need change here?
        #connection received here

        while True:
            try:
                # Receive bytes over the TCP connection. This will block
                # until "at least 1 byte or more" is available.
                recvd_bytes = connection.recv(Server.RECV_BUFFER_SIZE)
            
                # If recv returns with zero bytes, the other end of the
                # TCP connection has closed (The other end is probably in
                # FIN WAIT 2 and we are in CLOSE WAIT.). If so, close the
                # server end of the connection and get the next client
                # connection.
##                if len(recvd_bytes) == 0:
##                    print("Closing client connection ... ")
##                    connection.close()
##                    break
                
                # Decode the received bytes back into strings. Then output
                # them. First decode through sha256 algorithm.
                
                
                recvd_str = recvd_bytes.decode(Server.MSG_ENCODING)
                print("Received: ", recvd_str)
                self.handle_hash_key(recvd_str)
                # Send the received bytes back to the client.
                #convert self.msg_to_client into byte object
                connection.sendall(self.msg_to_client.encode('utf-8'))#connection.sendall(recvd_bytes)
                print("Sent: ", self.msg_to_client) #recvd_str

            except KeyboardInterrupt:
                print()
                print("Closing client connection ... ")
                connection.close()
                break

    def handle_hash_key(self, key):
        #handle GAC command or authenticate hash key and handle as needed
        #you cannot decrypt hash functions, whole premise of a hash function like sha256
        #loop through the csv
        #generate the hash key for the student ID and password
        #compare, and return flag which indicates whether autenticated or not
        #handle rest as required
        self.authenticated_flag = 0
        if(key == "GAC"):
            print("Received GAC from client")
            self.generate_lastrowcsvfile_string()
            self.msg_to_client = self.last_row_csv_string
        else:
            print("Received ID/Password hash "+key+" from client")
            with open('course_grades_2018.csv','r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    csv_id = str(row[0]) #typecast first entry of row to string
                    csv_pass = str(row[1])
                    #must encode or convert to byte objects
                    temp_key = (csv_id+csv_pass).encode('utf-8')
                    if(hashlib.sha256(temp_key).hexdigest() == key):
                        self.msg_to_client = ', '.join(row)
                        print("Correct password, record found")
                        self.authenticated_flag = 1

            if(self.authenticated_flag==0):
                self.msg_to_client = "Password Failure"
                print(self.msg_to_client)
        

    def printcsvfile(self):
        print("Grade Database from CSV: ")
        with open('course_grades_2018.csv','r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')

            for row in reader:
                print(', '.join(row))
                #print(row)
                
    def generate_lastrowcsvfile_string(self):
        i = 0
        with open('course_grades_2018.csv','r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reversed(list(reader)):
                if(i==0):
                    self.last_row_csv_string = ', '.join(row)
                    #print(', '.join(row))
                    i=i+1                                    

########################################################################
# Echo Client class
########################################################################

class Client:

    # Set the server hostname to connect to. If the server and client
    # are running on the same machine, we can use the current
    # hostname.
    SERVER_HOSTNAME = socket.gethostname()
    GET_AVERAGES_CMD = "GAC"

    RECV_BUFFER_SIZE = 1024 #should be enough bits to transfer the data

    def __init__(self):
        #do we need all of this?
        self.get_socket()
        self.connect_to_server()
        self.get_console_input()
        #self.send_console_input_to_server() #not sending console input always/forever

    def get_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connect_to_server(self):
        try:
            # Connect to the server using its socket address tuple.
            self.socket.connect((Client.SERVER_HOSTNAME, Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def get_console_input(self):
        # In this version we keep prompting the user until a GAC command
        # or their credentials are inputted.
        while True:
            ###############################################################
            #################TO DO HERE####################################
            #Implement the hashing/encryption here before passing to server
            #Take care of steps 4 and 5



            self.input_text = input("Please input a command: ")     
            if(self.input_text) == "GAC":
                print("Command entered: <GAC> ")
                print("Fetching grade averages: ")
                #Obtain Grades from the Server
                #encrypt the GAC command here
                data_to_send_is_GAC = "GAC"
                #should not need below 
##                data_to_send_is_GAC_temp = "GAC"
##                data_to_send_is_GAC_temp = data_to_send_is_GAC_temp.encode('utf-8')
##                data_to_send_is_GAC = hashlib.sha256(data_to_send_is_GAC_temp).hexdigest()
                self.send_console_input_to_server(data_to_send_is_GAC) #call function once
                #self.retrieve_grade_average()
            elif self.input_text != "": #any other text, prompt user
                self.username = getpass.getpass(prompt='<Student ID: >')
                self.password = getpass.getpass(prompt='<Password: >')
                print("ID number "+self.username+" and password "+self.password+" received ")

                self.user_pass = self.username + self.password
                self.user_pass = self.user_pass.encode('utf-8')
                
                hashed_data_to_send = hashlib.sha256(self.user_pass).hexdigest()
                print("ID/password hash "+hashed_data_to_send+" sent to server")
                self.send_console_input_to_server(hashed_data_to_send) #call function once
    
    def send_console_input_to_server(self,data_to_send): #only send if under above two conditions
        #while True:
        try:
            self.connection_send(data_to_send)
            self.connection_receive()
        except (KeyboardInterrupt, EOFError):
            print()
            print("Closing server connection ...")
            self.socket.close()
            sys.exit(1)
                
    def connection_send(self, data_to_send):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.socket.sendall(data_to_send.encode(Server.MSG_ENCODING)) #.encode('utf-8'))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes_from_server = self.socket.recv(Client.RECV_BUFFER_SIZE) #size of 1024 bits

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
##            if len(recvd_bytes) == 0:
##                print("Closing server connection ... ")
##                self.socket.close()
##                sys.exit(1)

            print("message from server: ")
            print(recvd_bytes_from_server.decode(Server.MSG_ENCODING)) #.decode('utf-8'))
            #self.socket.close()
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






