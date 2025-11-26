
from src import FileService
import os.path
import time
import hashlib
from users import Admin
from src import Headers
from users import TeacherService
class System:
    
    LOG_FILE = 'log.txt'
    
    def __init__(self):
        self.username = None
    
    def get_user(self):
        return self.username

    def geraLog(self, text):
        if not os.path.isfile(System.LOG_FILE) is False:
            pass

        with open (System.LOG_FILE, 'a') as file:
            now = time.localtime()
            now_formated = time.strftime('%d/%m/%y as %H:%M:%S', now)
            file.write(f'\n{now_formated} -> {self.username} - {text}')
        file.close()


    @staticmethod
    def hash_password(password):
        '''Cria um endereco hash SHA-256 da senha do usuario'''
        return hashlib.sha256(password.encode()).hexdigest()
    

    @staticmethod
    def permission_verification(username, password):
        users = FileService.FileService.load_users()
        if username == "ADMIN" and username in users and users[username] == password:
            print("\n✅ Login administrador autorizado!\n")
            
            return True
        else:
            return False
        

    def login(self):

        users = FileService.FileService.load_users()

        username = input("Usuario: ").upper().strip(" ")
        password = input("Senha: ")

        hashed_input = System.hash_password(password)
        #verificacao de login admin
        admin_permission = System.permission_verification(username, hashed_input)
        
        if admin_permission == True:
            self.username = username
            self.geraLog("Login")
            time.sleep(1)
            Headers.clear_menu()
            Admin.menu()
            
        else:
            #verificacao de login professor
            if username in users and users[username] == hashed_input:
                print("\n✅ Login autorizado!\n")
                self.username = username
                self.geraLog("Login")
                Headers.clear_menu()
                TeacherService.menu(self.username)
            else:
                print("\n❌ Nome de usuario ou senha invalidos.\n")
                Headers.clear_menu()
        
   