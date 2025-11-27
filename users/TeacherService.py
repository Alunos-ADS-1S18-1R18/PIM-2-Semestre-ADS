#classe estudante onde tudo relacionado ao professor sera inserido
from users import LoginService
import json
from src import Headers
from src import FileService


USER_LOG = "userLog.json"
MATERIAS_JSON = "materias.json"


def request_continue_edit_grade():
    while True:
        try:
            option = int(input("\nO que deseja fazer?\n[1-Editar outro Bimestre deste aluno]\n[2-Trocar de Aluno]\n[0-Voltar ao menu]\nOpcao:"))
            if option in [1, 2, 0]:  
                return option
            print("❌ Valor inválido. Digite 1, 2 ou 0.")
        except ValueError:
            print("❌ Valor digitado invalido")

            
def get_student_by_ra(username):
    while True:
        student_RA = ""
        while not student_RA:    
            student_RA = input("\nDigite o RA do aluno: ").strip()
            if not student_RA:
                print("\n❌ O RA não pode estar em branco. Tente novamente.")
       
        subject_selected = get_subject_userLog(username)
        user = get_name_userLog(username) 

        try:
            show_student_data_by_studentRA(subject_selected, user, student_RA)
            
            return student_RA, subject_selected, user
        except ValueError:
            
             print("Aluno não encontrado, tente novamente.")

def edit_grade_by_bimester(username):
    
    while True:
        
        student_RA, subject_selected, user = get_student_by_ra(username)
        
        while True:
            print(f"\n--- Editando Aluno RA: {student_RA} ---")
            print("Qual bimestre você deseja alterar [1º, 2º, 3º, 4º]?")
            
            try:
                
                new_list = request_student_grade(subject_selected, user, student_RA)
                print(f"Notas Atuais: {new_list}")

                selected_bimester = int(input("\nBimestre: "))
                
                if selected_bimester in [1, 2, 3, 4]:  
                    request_grade_str = input("Digite a nova Nota: ").replace(",", ".")
                    request_grade = float(request_grade_str)
                   
                    new_list[selected_bimester - 1] = request_grade
                  
                    edit_grades(subject_selected, user, student_RA, new_list)
                    print("\n✅ Nota atualizada com sucesso!")

                    show_student_data_by_studentRA(subject_selected, user, student_RA)
                    
                    decisao = request_continue_edit_grade()
                    
                    if decisao == 1:
                        continue 
                        
                    elif decisao == 2:
                        break 
                        
                    elif decisao == 0:          
                        teacher_menu(username)
                        return 
                else:
                    print("\n❌ Bimestre inválido! Escolha entre 1 e 4.")

            except ValueError:
                print("\n❌ Valor inválido inserido.")
            except Exception as e:
                print(f"\n❌ Ocorreu um erro: {e}")
def teacher_choice():
    while True:
        teacher_choice = None
        Headers.teacher_menu()
        try:
            teacher_choice = int(input("\nDigite a opcao: "))
        except ValueError:
            print("\n\nValor invalido, Favor inserir um valor Valido!\n\n")
        return teacher_choice
    
def teacher_menu(username):
    
    while True:
        teacher_option = teacher_choice()
        match teacher_option:
            case 1:
                
                edit_grade_by_bimester(username)     
            case 2:
                user = get_name_userLog(username)
                subject = get_subject_userLog(username)
                show_grades(subject, user)
            case 0:
                break
            case _ :
                continue
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
            print("-"*30)
            for key, values in student.items():
                print(f" {key}: {values}")
            print("-"*30)

def edit_grades(subject, teacher_login, student_RA, new_grade):
    json_load = FileService.FileService.json_load()

    if json_load[subject]["Professor"] != teacher_login:
        raise PermissionError("\n❌ Acesso negado! Voce não pode editar essa máteria.\n")
    
    for student in json_load[subject]["Alunos"]:
        if student["RA"] == student_RA:
            student["Nota"] = new_grade
            break
    else:
        raise ValueError("\n⚠️ Aluno nao foi encontrado\n")

    FileService.FileService.write_json(json_load)


def show_grades(subject, teacher_login):
    json_load = FileService.FileService.json_load()

    if json_load[subject]["Professor"] != teacher_login:
        raise PermissionError("\n❌ Acesso negado! Voce não pode ver essa máteria.\n")
    
    for aluno in json_load[subject]["Alunos"]: 
        print()
        print("-"*30)
        print(f"| Nome:  {aluno['Nome']}")
        print(f"| Turma: {aluno['Turma']}")
        print(f"| RA:    {aluno['RA']}")
        print(f"| Nota:  {aluno['Nota']}")
        print("-"*30) 

    print("\n--- Fim do Relatório ---")


