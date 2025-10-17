#Arquivo Principal onde o Codigo devera ser Rodado
from src import Headers
from users import Admin
from users import LoginService
import time


user_option = None

while True:
    
    Headers.main_menu()
    user_option = int(input("Opcao: "))
    if user_option == 1:
        Admin.register()
        time.sleep(2.3)
    elif user_option == 2:
        LoginService.LoginSevice.login()

        time.sleep(2.3)
    elif user_option == 3:
        print()
    elif user_option == 0:
        print("Encerrando o Programa")
        break
