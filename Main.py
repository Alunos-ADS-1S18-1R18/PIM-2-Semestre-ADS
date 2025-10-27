#Arquivo Principal onde o Codigo devera ser Rodado
from src import Headers
from users import LoginService
from users import Admin
import time


user_option = None

while True:
    
    Headers.main_menu()
    try:
        user_option = int(input("Opcao: "))
    except ValueError:
        print("❌ Entrada invalida, favor digitar um numero")
        time.sleep(1.5)
    match user_option:
        case 1:
            LoginService.LoginSevice.login()
            time.sleep(1.5)
        case 2:
            Admin.register_new_user()
        case 0:
            print("Encerrando o Programa")
            break



#TODO adicionar aluno