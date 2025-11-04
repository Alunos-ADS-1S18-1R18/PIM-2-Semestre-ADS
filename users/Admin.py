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
        data[subject] = {
            "Professor": teacher_name,
            "Alunos": []
        }  
        print(f"Professor {teacher_name} atribuido a materia {subject}")
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
        

def add_subject(subject_name):
    """Adiciona uma nova matéria se ela ainda não existir."""
    data = FileService.json_load()
    if subject_name not in data:
        data[subject_name] = []
        FileService.write_json(data)
        print(f"Matéria '{subject_name}' criada com sucesso!")
    else:
        print(f"Matéria '{subject_name}' já existe.")


def add_student(subject_name, ra, nota=None, media=None):
    """Adiciona um aluno a uma matéria existente."""
    data = FileService.FileService.json_load()
    # adiciona o aluno
    aluno = {"RA": ra, "Nota": nota, "Média": media}
    data[subject_name].append(aluno)

    FileService.FileService.write_json(data)
    print(f"Aluno RA {ra} adicionado à matéria '{subject_name}' com sucesso!")


def new_student(student_name, grade, student_class):
    json_load = FileService.FileService.json_load()

    new_student = {"Nome": student_name,"Turma": student_class, "Nota": grade, "RA": generete_aluno_code()}

    for subject in json_load:
        json_load[subject]["Alunos"].append(new_student)

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
                #TODO trazer/fazer funcoes relacionada com prefessor
               
                print("="*25)
                print("   Criar novo usuario\n")
                register_new_user()
                time.sleep(2)
                Headers.clear_menu()
                print()
                #editar professor   
            case 2:
                while True:
                    try:
                        print("="*25)
                        student_name = str(input("Nome do Aluno: "))
                        student_class = str(input("Turma do Aluno: "))
                        print("="*25)
                    except ValueError:
                        print("Nome ou Turma invalido!")
                        return
                    new_student(student_name, None, student_class)
                #TODO trazer/fazer funcoes relacionada com aluno
                
            case 0:
                break
            case _:
                print("Opcao nao encontrada favor inserir novamente")


