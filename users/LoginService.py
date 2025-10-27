#Sera incrementado aqui somente funcoes sobre Login.
from src import FileService
import os.path
import time
import hashlib
from users import Admin

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
    def permission_verification(username, password):
        users = FileService.FileService.load_users()
        if username == "ADMIN" and username in users and users[username] == password:
            print("✅ Login administrador autorizado!")
            LoginSevice.geraLog(f"Login ADMIN: {username}", LoginSevice.LOG_FILE)
            return True
        else:
            return False

    @staticmethod
    def login():

        users = FileService.FileService.load_users()

        username = input("Nome: ").upper().strip(" ")
        password = input("Senha: ")

        hashed_input = LoginSevice.hash_password(password)
        #verificacao de login admin
        admin_permission = LoginSevice.permission_verification(username, hashed_input)
        
        if admin_permission == True:
            time.sleep(1)
            Admin.menu()   
        else:
            #verificacao de login professor
   
            if username in users and users[username] == hashed_input:
                print("✅ Login autorizado!")
                LoginSevice.geraLog(f"Login: {username}", LoginSevice.LOG_FILE)
            else:
                print("❌ Nome de usuario ou senha invalidos.")
        