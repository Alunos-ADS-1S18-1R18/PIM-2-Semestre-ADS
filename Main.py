#TODO O programa devera ter cores!
#TODO Melhorar vizual do Programa!

from src import Headers
from users import LoginService
from src import FileService
import time
system = LoginService.System()

user_option = None
teste = "backup.json"
while True:
    FileService.FileService.convert_json_to_csv(teste)
    Headers.clear_menu()
    Headers.main_menu()
    try:
        user_option = int(input("Opcao: "))
    except ValueError:
        print("❌ Entrada invalida, favor digitar um numero")
        time.sleep(0.5)
    match user_option:
        case 1:
            system.login()
            time.sleep(0.5)
            Headers.clear_menu()
        case 0:
            print("Encerrando o Programa")
            break



