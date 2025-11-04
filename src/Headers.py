import os
import platform

def teacher_menu():
    print('='*25)
    print("1 - Inserir notas")
    print("2 - Ver notas")
    print("3 - Editar notas")
    print("0 - Sair")
    print('='*25)

def save_grade():
    save_data = ''
    while save_data not in ['S', 'N']:
        print("Salvar ? S/N")
        save_data = input("Selecione: ").upper()
        clear_menu()

def main_menu():
    clear_menu()
    print('='*25)
    print('1 - Login')
    print('0 - Finalizar programa')
    print('='*25)

def clear_menu():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear') 

def subject_names():
    subjects = ["Matemática", "Biologia", "Fisica",
                 "Portugues", "Ingles", "Filosofia", 
                 "Sociologia", "Quimica", "Geografia", 
                 "Educacao Fisica", "Historia"]
    print("="*25)
    for index, subject in enumerate(subjects):   
        print(f"[{index}] - {subject}")

    while True:
        try:
            print("="*25)    
            choice = int(input("Opcao: "))
            if 0 <= choice < len(subjects):
                print(f"\nVoce escolheu {subjects[choice]}\n")
                return subjects[choice]
            else:
                print("❌ Valor invalido. Tente novamente.")
        except ValueError:
            print("❌ Entrada invalida. Digite um numero.")
    
def request_continue():
    
    while True:
        print("Continuar inserindo alunos?[1-SIM/0-NAO]")
        try:
            option = int(input("Selecione uma opcao: "))
            while option not in [1, 0]:
                return option
        except ValueError:
            print("❌ Valor digitado invalido")

        return option
