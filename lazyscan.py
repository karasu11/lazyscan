# Very basic portscanner created for my own education.
# Started from the tutorial here:
# https://resources.infosecinstitute.com/topic/write-a-port-scanner-in-python/
# Made some own tweaks and additions, most notably argument parsing with
# argparse, refactoring, and updating code to fit Python 3.x.
# Only filters by open and closed ports.
# DO NOT LAUNCH SCANS AGAINST TARGETS WITHOUT EXPLICIT PERMISSION.


import socket
import subprocess
import sys
from datetime import datetime
from argparse import ArgumentParser, Namespace


def resolve_target_ip(hostname):
    '''Attempt to resolve the provided hostname to an IP address.'''
    try:
        target_IP = socket.gethostbyname(hostname)
        return target_IP
    except socket.gaierror:
        print(f'Host {hostname} could not be resolved. Quitting...')
        return None


def scan_target(args, target_IP):
    '''Scan the target and return number of open ports, or None if error.'''
    counter = 0
    try: 
        portrange = args.range
        ports = args.ports
        
        if portrange != None:
            for port in range(portrange[0], portrange[1] + 1):
                counter += scan_port(target_IP, port)
        if ports != None:
            for port in ports:
                counter += scan_port(target_IP, port)
        if portrange == None and ports == None:
            print('\nNo ports selected. Quitting...')
            return None
        return counter
    except KeyboardInterrupt:
        print('Ctrl+C entered. Quitting...')
        return None
    except socket.gaierror:
        print('Hostname could not be resolved. Quitting...')
        return None
    except socket.error:
        print('Could not connect to remote host. Quitting...')
        return None


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
 

def get_final_output(args, time_elapsed, open_ports):
    '''Return a summary string after scanning. Verbose if -v/--verbose flag.'''
    if args.verbose:
        output = (f'\nScan completed in: {time_elapsed.seconds} seconds and '
                  f'{time_elapsed.microseconds} microseconds.\n{open_ports} '
                  'open ports were found.')
    else:
        if open_ports == 0:
            print('No open ports were found.')
        output = f'\nScan completed in: {time_elapsed.seconds} seconds.'
    return output


if __name__ == '__main__':
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
    open_ports = 0

    # NOTE: change 'cls' to 'clear' on Linux
    subprocess.call('cls', shell=True)

    target_ip = resolve_target_ip(hostname)
    if target_ip:
        print('_' * 36)
        print(f'Scanning host {hostname}...')
        print('_' * 36)

        t1 = datetime.now()
        
        open_ports = scan_target(args, target_ip)
    else:
        sys.exit()

    t2 = datetime.now()
    time_elapsed = t2 - t1

    final_output = get_final_output(args, time_elapsed, open_ports)
    print(final_output)