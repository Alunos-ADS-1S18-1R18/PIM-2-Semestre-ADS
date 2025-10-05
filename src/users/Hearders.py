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
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear') #mac e linux

