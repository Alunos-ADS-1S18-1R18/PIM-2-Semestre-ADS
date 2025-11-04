#classe estudante onde tudo relacionado ao professor sera inserido

import json
from src import Headers
from src import FileService
from users import LoginService


USER_LOG = "userLog.json"
MATERIAS_JSON = "materias.json"



def menu(username):
    while True:
        teacher_choice = None
        Headers.teacher_menu()
        try:
            teacher_choice = int(input("Digite a opcao: "))
        except ValueError:
            print("\n\nValor invalido, Favor inserir um valor Valido!\n\n")

        match teacher_choice:
            case 1:
                try:
                    student_RA = str(input("Digite o RA do aluno: "))
                except ValueError:
                    print("❌ Valor inserido invalido, favor digitar novamente")
                try:
                    new_grade = float(input("Nota do aluno: "))
                except ValueError:
                    print("❌ Valor inserido invalido, favor digitar novamente")
                get_subject = get_subject_userLog(username)
                user = get_name_userLog(username)
                edit_grades(get_subject, user, student_RA, new_grade)
                Headers.clear_menu()
                
            case 2:
                #TODO Ver notas dos alunos.
                pass
            case 3:
                #TODO Editar notas dos alunos. 
                LoginService.System.geraLog(f"Edicao de Notas")
                pass
            case 0:
                break

def load_userLog():
    with open(USER_LOG, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

def get_name_userLog(login_user):

    data = load_userLog()
    for user in data:
        if login_user == user:
            return data[user]["teacher"]
            
def get_subject_userLog(login_user):
    
    data = load_userLog()
    for user in data:
        if login_user == user:
            return data[user]["subject"]

            
 

def edit_grades(subject, teacher_login, student_RA, new_grade):
    json_load = FileService.FileService.json_load()

    #verifica se o professor tem permissao.
    if json_load[subject]["Professor"] != teacher_login:
        raise PermissionError("\n❌ Acesso negado! Voce não pode editar essa máteria.\n")

    #Atualiza a nota do aluno
    for student in json_load[subject]["Alunos"]:
        if student["RA"] == student_RA:
            student["Nota"] = new_grade
            break
    else:
        raise ValueError("\n⚠️ Aluno nao foi encontrado\n")

    #Salva as alteracoes
    FileService.FileService.write_json(json_load)

