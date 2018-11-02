#SERVER

import socket
import sys
import os

#--------------------------------------------------------------------------
#                              FUNCTIONS
#--------------------------------------------------------------------------

def upload(client_request_list):
    #format of request list: 
    print("upload")
def download(client_request_list):
    print("download")
def list_dir(client_request_list):
    print("list")

def invalid_request(error_type,optional_message):
    if(error_type == "empty"):
        return "error;Request could not be filled, recieved message was empty;"
    else:
        return "error;Request could not be filled, request type '" + str(client_request_list[0]) + "' is not recognized;"
    

#--------------------------------------------------------------------------
#                            end functions 
#--------------------------------------------------------------------------




#--------------------------------------------------------------------------
#           SERVER SCRIPT
#--------------------------------------------------------------------------

#CHECK THE CMD LINE CALL CONTAINS NECESSARY ARGUMENTS
if len(sys.argv) != 2:
    print("ERROR: Invalid cmd line arguments")
    exit()



#CREATE AND BIND THE SOCKET
try:
    #Initialize the server variables
    port = int(sys.argv[1])
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname)
    working_dir = os.path.dirname(os.path.abspath(__file__))
    hostAllAvailable = "0.0.0.0"

    #Create the socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Print status server details back to the user
    print("STATUS: Server created at:")
    print ("\tServer hostname: " + str(hostname))
    print ("\tServer IP: " + str(IPaddr))
    print ("\tServer Port: " + str(port))
    print ("\tServer Dir: " + working_dir)
    print ('\n')

    #Bind the socket
    serverSocket.bind((hostAllAvailable, port))
    print("STATUS: Server bind to port " + str(port) + " complete")

    #Set up a que of clients to handle 
    serverSocket.listen(5)
    print ("\nSTATUS: Server waiting for client connections\n")
except Exception as e:
    print("ERROR: Server creation process could not be completed (error details below)")
    print(e)
    #exit with a non-zero value to indicate error condition
    exit(1)



#CONNECT THE SOCKET
try:

    #Dequeue a connection request from the queue created by listen() earlier.
    #If no request is in the queue yet this will block until one comes in.

    #Returns a new socket to use to communicate with the connected client 
    #   plus the client-side socket's address (IP and port number). 
    cli_sock, cli_addr = serverSocket.accept()
    print("STATUS: Client " + str(cli_addr) + " connected...")

    #request message
    request = cli_sock.recv(4096)
    #remember to take this out later
    print(request)
    print("out of loop")
except Exception as e:
    print("ERROR: Server could not connect to client at " + str(cli_addr) + " (error details below)")
    print(e)
    cli_sock.close()
    #Should I have the program close if a client connection fails? Or should I go back to listening? Where will it resume if I don't?
    exit(1)


"""
HANDLE REQUEST MESSAGE
1 X decode the request 
2 - split the request into the right arguments
3 - call the right function? 

#  *handle checking the arg list is correct length and contents within the functions 
#  *pass the list of args to the functions 
PUT
    1 - get the file name and the file data, decode the data? 
    2 - check if the file exists and the data is valid 
    3 - return errors n stuff if file exists or stuff (sent back in response)
    4 - write the file 
    5 - make the response message
    6 - return the response message to send back 
GET 
    1 - get the file name from the request 
    2 - check if the file exists and the data is valid 
    3 - use code from client server to copy file data and send back to client 
    4 - make the response message
    5 - return the response message 
LIST 
    1 - figure out how to turn the directory contents into a string 
    2 - encode the string 
    3 - return the dir string as response 

4 - encode the response message 
5 - send the response message 
6 - close the server and stuff 


"""

#HANDLE THE REQUEST MESSAGE
#Decode the request message from bytes back to string form and convert to list of strings
client_request_message = request.decode("utf-8")
client_request_list = client_request_message.split(';') #splits string into list of strings
client_request_list = filter(None, client_request_list) #removes empty strings in list
#Call requested function (returns appropriate response message in string form)
if len(client_request_list) >=1 :
    request_type = client_request_list[0]
    #upload 
    if request_type == "put":
        response_message = upload(client_request_list)
    #download 
    elif request_type == "get":
        response_message = download(client_request_list)
    #list dir 
    elif request_type == "list":
        response_message = list_dir(client_request_list)
    #type unrecognized
    else:
        print("ERROR: Client request type '"+request_type+"' is not recognized")
        response_message = invalid_request("invalid", request_type)
else:
    print("ERROR: Client request message empty")
    response_message = invalid_request("empty", "empty")
    #Should I close the socket and/or program here? Or can I go back to listening? How does listening work? 

#TODO upload function
#TODO download function
#TODO list_dir function
#TODO invalid function

#DECODE AND PREP RESPONSE TO BE SENT
    
#SEND RESPONSE BACK    
#send message
#cli_sock.send()

#CLOSE OUT AND CLEAN UP
#   *don't exit the program in case the client wants to try again 
print("closing server")
cli_sock.close()