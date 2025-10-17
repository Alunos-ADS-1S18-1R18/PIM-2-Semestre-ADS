#Sera incrementado aqui somente funcoes sobre Login.
from src import FileService
import os.path
import time
import hashlib

class LoginSevice:
    LOG_FILE = 'log.txt'

    @staticmethod
    def hash_password(password):
        '''Cria um endereco hash SHA-256 da senha do usuario'''
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def geraLog(text, file_name):
        if os.path.isfile(LoginSevice.LOG_FILE) is False:
            print("Arquivo criado")
        
        arquivo = open(file_name, 'a')

        now = time.localtime()
        now_formated = time.strftime('%d/%m/%y as %H:%M:%S', now)

        arquivo.write(f'\n{now_formated} -> {text}')

        arquivo.close()


    @staticmethod
    def login():

        users = FileService.FileService.load_users()

        username = input("Nome: ")
        password = input("Senha: ")

        hashed_input = LoginSevice.hash_password(password)
        if username in users and users[username] == hashed_input:
            print("✅ Login autorizado!")
            LoginSevice.geraLog(f"Login: {username}", LoginSevice.LOG_FILE)
        else:
            print("❌ Nome de usuario ou senha invalidos.")
