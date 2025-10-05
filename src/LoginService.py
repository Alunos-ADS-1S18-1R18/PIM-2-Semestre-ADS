#Sera incrementado aqui somente funcoes sobre Login.

import os.path
import time

def geraLog(text, file_name):
    if os.path.isfile('log.txt') is False:
        print("Arquivo criado")
    
    arquivo = open(file_name, 'a')

    now = time.localtime()
    now_formated = time.strftime('%d/%m/%y as %H:%M:%S', now)

    arquivo.write(f'\n{now_formated} -> {text}')

    arquivo.close()

geraLog("Login usuario", "log.txt")


