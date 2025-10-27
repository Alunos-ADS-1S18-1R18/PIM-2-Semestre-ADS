import os
import platform

def teacher_menu():
    print('='*20)
    print("1- Inserir notas")
    print("2- Ver notas")
    print("3- Editar notas")
    print("4- Novo aluno")
    print("0- Sair")
    print('='*20)

def save_grade():
    save_data = ''
    while save_data not in ['S', 'N']:
        print("Salvar ? S/N")
        save_data = input("Selecione: ").upper()
        clear_menu()

def main_menu():
    clear_menu()
    print('='*20)
    print('1 - Login')
    print('0 - Finalizar programa')
    print('='*20)

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
    for index, subject in enumerate(subjects):   
        print(f"[{index}] - {subject}")

    while True:
        try:    
            choice = int(input("Opcao: "))
            if 0 <= choice < len(subjects):
                print(f"Voce escolheu {subjects[choice]}")
                return subjects[choice]
            else:
                print("Valor invalido. Tente novamente.")
        except ValueError:
            print("Entrada invalida. Digite um numero.")
    
