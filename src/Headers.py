import os
import platform

def teacher_menu():
    print('='*30)
    print("1 - Inserir notas")
    print("2 - Ver notas")
    print("0 - Sair")
    print('='*30)

def save_grade():
    save_data = ''
    while save_data not in ['S', 'N']:
        print("Salvar ? S/N")
        save_data = input("Selecione: ").upper()
        clear_menu()

def main_menu():
    clear_menu()
    print('='*30)
    print("Bem Vindo ao SmartClass")
    print('='*30)
    print('1 - Login')
    print('0 - Finalizar programa')
    print('='*30)

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
    print("="*30)
    for index, subject in enumerate(subjects):   
        print(f"[{index}] - {subject}")

    while True:
        try:
            print("="*30)    
            choice = int(input("Opcao: "))
            if 0 <= choice < len(subjects):
                print(f"\nVoce escolheu {subjects[choice]}\n")
                return subjects[choice]
            else:
                print("❌ Valor invalido. Tente novamente.")
        except ValueError:
            print("❌ Entrada invalida. Digite um numero.")
    
def request_continue(text):
    
    while True:
        print(text)
        try:
            option = int(input("Selecione uma opcao: "))
            if option in [1, 0]:  
                return option
            print("❌ Valor inválido. Digite 1 ou 0.")
        except ValueError:
            print("❌ Valor digitado invalido")
        