#CLIENT
#cmd call: py client.py <hostname> <port> <put filename|get filename|list>
#cmd sys.argv: [0]=script [1]=hostname [2]=port [3]=request_type [4]=filename

import socket
import sys
import os

#--------------------------------------------------------------------------
#                              FUNCTIONS
#--------------------------------------------------------------------------
def check_filename_validity(client_file_name):
    #TODO check that file contains only permitted characters
    # filtered characters: * . ” / \ [ ] : ; | = ,
    for(ch in client_file_name):
        illegal_chars = ['\*','\"','\/','\\','\[','\]',':',';','|','=',',']
        if illegal_chars.contains(ch):
            print("hello")

def put_request(client_file_name):
    #check file to upload exists
    exists = os.path.isfile(client_file_name)
    if not exists:
        print ("ERROR: 'put' file does not exist")
        exit()

    #open and read file as binary data
    with open(client_file_name, "rb") as client_file:
        file_binary = client_file.read()   #file contents as binary
        file_contents = file_binary.encode("utf-8")   #file binary converted to string for request string

    #formulate string request message
    request_message = "put;" + client_file_name + ";" + file_contents + ";"
    print("REQUESTING: Upload '" + client_file_name + "' to server")

    return request_message

def get_request(server_file_name):

    #formulate string request message
    request_message = "get;" + server_file_name + ";"
    print("REQUESTING: Download '" + server_file_name + "' from server")

    return request_message

def list_request():

    #formulate string request message
    request_message = "list;"
    print("REQUESTING: List server directory contents")

    return request_message

#--------------------------------------------------------------------------
#                       end functions section
#--------------------------------------------------------------------------





#--------------------------------------------------------------------------
#                               SCRIPT
#--------------------------------------------------------------------------

#check the command line args are appropriate
if len(sys.argv) < 4 or len(sys.argv) > 5:
    print("ERROR: invalid cmd line arguments, please try again")
    exit(1)

#get the server details from the command line args
server_host_addr = sys.argv[1]
server_port = int(sys.argv[2])

#get the working directory for the client
client_dir = os.path.dirname(os.path.abspath(__file__))

#define variables for formulating request
client_request_type = sys.argv[3]
if(len(sys.argv>4)):
    client_request_file = sys.argv[4]

#formulate request message with request functions
try:
    if client_request_type == "put":
        request_message = put_request(client_request_file)

    else if client_request_type == "get":
        request_message = get_request(client_request_file)

    else if client_request_type == "list":
        request_message = list_request()
    else:
        print("ERROR: Request type unrecognized")
        exit(1)

except Exception as e:
    print(e)
    exit(1)

try:
    #create a socket and connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("STATUS: Client socket created")
    client_socket.connect((server_host_addr, server_port))
    print("STATUS: Connected to server at IP=" + server_host_addr + ", PORT=" + str(server_port) )

    #convert string request message into byte object to send to server
    request_message_inBytes = request_message.encode("utf-8")

    #send request message to server
    client_socket.sendall(request_message_inBytes)
    print("STATUS: Request sent")

    #client_socket.recv()
    client_socket.close()

except Exception as e:
    print("EXCEPTION ERROR: " + e)
    client_socket.close()
    exit()
