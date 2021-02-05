import argparse, socket
from datetime import datetime

MAX_BYTES = 65555 
# UDP Maximum packet size is 65 kilo bites
# So we are making sure the packet size that is transmiting in the network is less than that maximum size  


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #AF_INET = IPV4
    # SOCK_DIAGRAM = To look
    sock.bind(('127.0.0.1', port))
    # We are binding to local host 127.0.0.1 and the port is coming into the function
    print("Server is Listening at {}".format(sock.getsockname()))
    # We are starting the server which is basically continously running
    # Hence True
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        text = 'The data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data, address)
def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = 'The time at my side is {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1',port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print('The server at this location {} replied {!r}'.format(address, text))
    

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    # Server Port Default - 1060
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
