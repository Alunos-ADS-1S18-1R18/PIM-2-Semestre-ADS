
import random
import string
from src import FileService
from src import Headers
import time
import os
import json

USER_LOG = "userLog.json"
MATERIAS_JSON = "materias.json"


def set_teacher(subject, teacher_name):
    #Define um novo professor na materia
    data = FileService.FileService.json_load()
    if subject in data:
        
        if data[subject]["Professor"] is not None:
            if data[subject]["Professor"] is not "":
                print(f"Ja existe um professor nesta materia {data[subject]["Professor"]}\n")
                while True:
                    try:
                        print("="*25)
                        option = int(input("\n\nContinuar?\n[1]SIM\n[0]NAO: "))
                    except ValueError:
                        print("Entrada invalida, Por favor inserir um numero.")
                    match option:
                        case 1:
                            print(f"O professor {data[subject]["Professor"]} foi substituido por {teacher_name}")
                            data[subject]["Professor"] = teacher_name
                            break
                        case 0:
                            break
            else:
                print(f"O professor {teacher_name} foi adicionado a matéria {subject}")
                data[subject]["Professor"] = teacher_name
                
    else:
        data[subject] = {
            "Professor": teacher_name,
            "Alunos": []
        }  
        print(f"Professor {teacher_name} atribuido a matéria {subject}")
    FileService.FileService.write_json(data)

def verificar_codigo(codigo):
    # Etapa 1: Somar os valores ASCII dos caracteres
    soma_ascii = sum(ord(c) for c in codigo)

    # Etapa 2: Multiplicar pela posição do primeiro número encontrado
    pos_num = next((i for i, c in enumerate(codigo) if c.isdigit()), 1)
    resultado = soma_ascii * pos_num

    # Etapa 3: Subtrair o produto da quantidade de letras maiúsculas vezes 42
    letras_maiusculas = sum(1 for c in codigo if c.isupper())
    resultado -= letras_maiusculas * 42

    # Etapa 4: Adicionar o valor da última letra convertida para número (A=1, B=2, ..., Z=26)
    letras = [c for c in codigo if c.isalpha()]
    if letras:
        ultima_letra = letras[-1]
        resultado += ord(ultima_letra.upper()) - 64

    # Etapa 5: Aplicar módulo 97 e verificar se o resultado é igual a um valor fixo (ex: 73)
    return resultado % 97 == 73


def generete_aluno_code():
    while True:
        # Gera uma string aleatória de 8 caracteres (letras e números)
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if verificar_codigo(codigo):
            return codigo

def write_user_log(data):
    with open(USER_LOG, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def set_user_data(username, teacher_name, subject):
    
    if not os.path.exists(USER_LOG):
        print('\nArquivo não encontrado, criando um novo...\n')
        data = {}
        
        return data
        
    with open(USER_LOG, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("\nArquivo vazio ou corrompido, recriando...\n")
            data = {}
            write_user_log(data)
    data[username] = {"teacher": teacher_name, "subject": subject}
    write_user_log(data)
    return data[username]

def register_new_user():
    """Registra novo usuario professor"""
    users = FileService.FileService.load_users()
    username = input("Usuario: ").upper().strip(" ")
    if username in users:
        print("⚠️ Usuario ja existe.")
        return
    password = input("Senha: ")
    if username == "ADMIN":
            print("❌ O nome de usuario nao pode ser admin")
    else:
        FileService.FileService.save_user(username, password)
        print("\n✅ Usuario registrado com sucesso!\n")
        teacher_name = input("Nome do Professor: ")
        print("\nAtribuir uma materia para este usuario")
        subject_selected = Headers.subject_names()
        print()
        set_teacher(subject_selected, teacher_name)
        print()
        set_user_data(username, teacher_name, subject_selected)
        

def new_student():
    json_load = FileService.FileService.json_load()
    while True:
        print("="*25)                      
        student_name = input("Nome do Aluno: ").strip()
        student_class = input("Turma do Aluno: ").strip()
        print("="*25)
        if not student_name or not student_class:
            print("⚠️ Nome e Turma não podem estar vazios. Tente novamente.")
            continue
        else:
            new_student = {
                "Nome": student_name,
                "Turma": student_class, 
                "Nota": [0,0,0,0],
                "RA": generete_aluno_code()
                }
            for subject in json_load:
                json_load[subject]["Alunos"].append(new_student)
            
            request_continue = Headers.request_continue("Continuar inserindo alunos?[1-SIM/0-NAO]")

            if request_continue == 0:
                break

    FileService.FileService.write_json(json_load)
    print(f"Aluno {student_name} adicionado a todas as materias com sucesso!")


def menu():
    while True:
        print("="*25)
        print("1 - Area Professor\n2 - Area Aluno\n0 = Sair")
        print("="*25)
        try:
            option = int(input("Digite uma opcao: "))
        except ValueError:
            print(f"\nopcao ivalida! favor digitar um valor numerico\n")
            continue
        match option:
            case 1:
               
                print("="*25)
                print("   Criar novo usuario\n")
                register_new_user()
                time.sleep(2)
                Headers.clear_menu()
                print()
               
                  
            case 2:
                new_student()
                 
            case 0:
                break
            case _:
                print("Opcao nao encontrada favor inserir novamente")


