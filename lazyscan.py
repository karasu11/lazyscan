# Very basic portscanner created for my own education.
# Started from the tutorial here:
# https://resources.infosecinstitute.com/topic/write-a-port-scanner-in-python/
# Made some own tweaks and additions, most notably argument parsing with
# argparse and updating code to fit Python 3.x.
# Only filters by open and closed ports.
# DO NOT LAUNCH SCANS AGAINST TARGETS WITHOUT EXPLICIT PERMISSION.


import socket
import subprocess
import sys
from datetime import datetime
from argparse import ArgumentParser, Namespace


def scan_port(target_IP, port):
    '''Scan the given port of the given target. Filter as open or closed.'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((target_IP, port))
    if result == 0:
        print(f'Port {port}:'.ljust(32, ' '), end='')
        print('Open')
        sock.close()
        return 1  # For the counter that keeps track of open ports found. 
    else: 
        if args.verbose:
            print(f'Port {port}:'.ljust(30, ' '), end='')
            print('Closed')
        sock.close()
        return 0  # For the counter
 

parser = ArgumentParser()
parser.add_argument( 
    'hostname', 
    metavar='',  
    help='The hostname/IP-addr of the target.'
)
parser.add_argument(
    '-r',
    '--range',
    metavar='port',
    type=int,
    nargs=2,
    help='Range of ports to be scanned. Separate with a space.'
)
parser.add_argument(
    '-p',
    '--ports', 
    metavar='port', 
    type=int, 
    nargs='+',
    help='Individual ports to be scanned. Separate with spaces.'
)
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Output the state of all ports, closed as well as open.'
)

args: Namespace = parser.parse_args()
hostname = args.hostname
open_port_counter = 0

# NOTE: change 'cls' to 'clear' on Linux
subprocess.call('cls', shell=True)

try:
    target_IP = socket.gethostbyname(hostname)
except socket.gaierror:
    print(f'Host {hostname} could not be resolved. Quitting...')
    sys.exit()

print('_' * 36)
print(f'Scanning host {hostname}...')
print('_' * 36)

t1 = datetime.now()

try: 
    portrange = args.range
    ports = args.ports
    
    if portrange != None:
        for port in range(portrange[0], portrange[1] + 1):
            open_port_counter += scan_port(target_IP, port)
    if ports != None:
        for port in ports:
            open_port_counter += scan_port(target_IP, port)
    if portrange == None and ports == None:
        print('\nNo ports selected. Quitting...')

except KeyboardInterrupt:
    print('Ctrl+C entered. Quitting...')
    sys.exit()

except socket.gaierror:
    print('Hostname could not be resolved. Quitting...')
    sys.exit()

except socket.error:
    print('Could not connect to remote host. Quitting...')
    sys.exit()

t2 = datetime.now()
time_elapsed = t2 - t1

if args.verbose:
    print(f'\nScan completed in: {time_elapsed.seconds} seconds and '
          f'{time_elapsed.microseconds} microseconds.')
    print(f'{open_port_counter} open ports were found.')
else:
    print(f'\nScan completed in: {time_elapsed.seconds} seconds.')
    