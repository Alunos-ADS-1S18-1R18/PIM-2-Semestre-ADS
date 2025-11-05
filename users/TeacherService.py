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
                #TODO inserir 4 notas referente a cada bimestre.
                #new_grade = None
                student_RA = ""
                while not student_RA:
                    student_RA = input("Digite o RA do aluno: ").strip()
                    if not student_RA:
                        print("❌ O RA não pode estar em branco. Tente novamente.")              
                subject_selected = get_subject_userLog(username)
                user = get_name_userLog(username)
                show_student_data_by_studentRA(subject_selected,user,student_RA)
                #TODO confirmar aluno
                try:
                    print("1 - Continuar\n" \
                    "2 - Selecionar outro aluno\n" \
                    "0 - Voltar ao Menu\n")
                    user_request = int(input("\nOpcao: "))
                    match user_request:
                        case 1:
                            selected_bimester = None
                            while selected_bimester not in [1, 2, 3, 4]:
                                try:
                                    print("\nDigite o numero correspondente do Bismestre a ser alterado.\n")
                                    print("Qual bimentre você deseja alterar [1º, 2º, 3º, 4º]?\n\n")
                                    new_list = request_student_grade(subject_selected,user, student_RA)
                                    print(f"Notas: {new_list}")
                                    selected_bimester = int(input("Bimestre: "))
                                    new_list[selected_bimester - 1] = float(input("Digite a nova Nota: "))
                                    print(new_list)
                                    edit_grades(subject_selected, user, student_RA, new_list)
                                    show_student_data_by_studentRA(subject_selected,user,student_RA)
                                except ValueError:
                                    print("❌ Valor digtido invalido por favor inserir apenas numeros!")

                            #TODO acessar o indice da lista
                            #TODO alterar o valor do indice
                            #TODO print
                            #TODO confirmacao
                            #TODO salvar
                            pass
                        case 2:
                            pass
                        case 0:
                            continue

                except ValueError:
                    print("❌ Valor inserido incorreto! tentar novamente")
                    
                
                    
                '''while new_grade is None:
                    grade_str = input("Nota do aluno: ")
                    try:                    
                        new_grade = float(grade_str.replace(',', '.'))
                        if not (0.0 <= new_grade <= 10.0):
                            print(f"❌ Nota inválida ({new_grade}). A nota deve estar entre 0 e 10.")
                            new_grade = None 
                        
                    except ValueError:
                        print("❌ Valor inserido inválido. Digite um número (ex: 7.5).")'''

                #LoginService.System.geraLog(f"Edicao de Notas")
        
                
                #edit_grades(subject, user, student_RA, new_grade)
                #Headers.clear_menu()
                
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


