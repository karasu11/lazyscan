# lazyscan
Basic port scanner made in Python 3 for educational purposes.
Based on the script in this tutorial: https://resources.infosecinstitute.com/topic/write-a-port-scanner-in-python/, but expanded with argument parsing and some other details, refactored, and updated to Python 3.
Supports CLI arguments to specify target, individual ports to scan and/or a range of ports to scan, and verbosity.
Only filters results as open / closed. 
Do not scan any targets, locally or on the internet, without explicit permission.

Usage:
- If on Linux, change 'cls' to 'clear' in the line "subprocess.call('cls', shell=True)"
- Run the script and supply a hostname or IP address to scan. Do not supply a full URL. Add any individual ports you want to scan after the -p or --ports flag. For example "-p 80 443". You can also add a range of ports to scan after the -r or --range flag. For example "-r 20 30". Only spaces can be used as delimiters with both flags. -r and -p can be used together. Add -v or --verbose to see the results for all ports scanned, not only the open ones, as well as a highly precise estimate of how long the scan took to complete.
- Run lazyscan.py --help to see a summary of usage. 
