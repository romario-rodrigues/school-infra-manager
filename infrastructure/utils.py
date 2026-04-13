import os
import platform
import subprocess

def ping_host(ip):
    """
    Retorna True se o host responder ao ping, False caso contrário.
    """
    if not ip:
        return False
        
    # Define o parâmetro de contagem baseado no sistema operacional
    # No Docker (Linux), o parâmetro é '-c'
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', '1', ip] # -W 1 é o timeout de 1 segundo

    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
