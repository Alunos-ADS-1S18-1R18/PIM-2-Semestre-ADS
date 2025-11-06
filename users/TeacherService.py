#classe estudante onde tudo relacionado ao professor sera inserido

import json
from src import Headers
from src import FileService
from users import LoginService
import time

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
                student_RA = ""
                while not student_RA:
                    try:
                        request_confirm = Headers.request_continue("Deseja voltar?[1-SIM/0-NAO]")
                        if request_confirm == 1:
                            break
                    except ValueError:
                        print("❌ O valor nao pode ser vazio")
                   
                    student_RA = input("Digite o RA do aluno: ").strip()
                    if not student_RA:
                        print("❌ O RA não pode estar em branco. Tente novamente.")
                              
                subject_selected = get_subject_userLog(username)
                user = get_name_userLog(username)
                show_student_data_by_studentRA(subject_selected,user,student_RA)
                try:
                    print("1 - Continuar\n" \
                    "0 - Voltar ao Menu\n")
                    user_request = int(input("\nOpcao: "))
                    match user_request:
                        case 1:
                            
                            while True:
                                try:
                                    print("\nDigite o numero correspondente do Bismestre a ser alterado.\n")
                                    print("Qual bimestre você deseja alterar [1º, 2º, 3º, 4º]?\n\n")
                                    new_list = request_student_grade(subject_selected,user, student_RA)
                                    print(f"Notas: {new_list}")
                                    selected_bimester = int(input("Bimestre: "))
                                    if selected_bimester in [1, 2, 3, 4]:  
                                        request_grade_str = input("Digite a nova Nota: ").replace(",", ".")
                                        request_grade = float(request_grade_str)
                                        new_list[selected_bimester - 1] = request_grade
                                        print(new_list)
                                        edit_grades(subject_selected, user, student_RA, new_list)
                                        show_student_data_by_studentRA(subject_selected,user,student_RA)
                                        try:
                                            request_confirm = Headers.request_continue("Deseja editar a nota de outro bimestre?[1-SIM/0-NAO]")
                                        except ValueError:
                                            print("❌ O valor nao pode ser vazio")
                                        if request_confirm == 0:
                                            break
                                    else:
                                        print("❌ Bimestre nao encontrado!")
                                except ValueError:
                                    print("❌ Valor digtido invalido por favor inserir apenas numeros!")
                        case 0:
                            continue

                except ValueError:
                    print("❌ Valor inserido incorreto! tentar novamente")
                
            case 2:
                user = get_name_userLog(username)
                subject = get_subject_userLog(username)
                show_grades(subject, user)
                
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
        
def request_student_grade(subject, teacher_login, student_RA):
    json_load = FileService.FileService.json_load()

    if json_load[subject]["Professor"] != teacher_login:
        raise PermissionError("\n❌ Acesso negado! Voce não pode editar essa máteria.\n")
    
    for student in json_load[subject]["Alunos"]:
        if student["RA"] == student_RA:
            new_list = student["Nota"].copy() 
            break
    else:
        raise ValueError("\n⚠️ Aluno nao foi encontrado\n")
    return new_list
            
def show_student_data_by_studentRA(subject, teacher_login, student_RA):
    json_load = FileService.FileService.json_load()

    if json_load[subject]["Professor"] != teacher_login:
        raise PermissionError("\n❌ Acesso negado! Voce não pode editar essa máteria.\n")
    
    for student in json_load[subject]["Alunos"]:
        if student["RA"] == student_RA:
            print("-"*25)
            for key, values in student.items():
                print(f"    {key}: {values}")
            print("-"*25)

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


def show_grades(subject, teacher_login):
    json_load = FileService.FileService.json_load()

    if json_load[subject]["Professor"] != teacher_login:
        raise PermissionError("\n❌ Acesso negado! Voce não pode ver essa máteria.\n")
    
    for aluno in json_load[subject]["Alunos"]:  
        print(f"|  Nome:  {aluno['Nome']}")
        print(f"|  Turma: {aluno['Turma']}")
        print(f"|  RA:    {aluno['RA']}")
        print(f"|  Nota:  {aluno['Nota']}")
        print("-"*20) 

    print("\n--- Fim do Relatório ---")


