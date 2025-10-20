#classe estudante onde tudo relacionado ao professor sera inserido

'''4. Menu do Professor
 Exibir menu com opções:
1-Inserir notas dos alunos
2-Ver notas dos alunos
3-Editar notas
4-Novo aluno

'''
from src import Headers, FileService
from users.LoginService import geraLog
MATERIAS_JSON = "materias.json"

while True:
    teacher_choice = None

    Headers.teacher_menu()
    try:
        teacher_choice = int(input("Digite a opcao desejada: "))
    except ValueError:
        print("\n\nValor invalido, Favor inserir um valor Valido!\n\n")

    if teacher_choice == 1:
        #TODO Inserir notas dos alunos. #TIP Tem que acessar o json pela materia
        print()
        geraLog("Inseriu nota", 'log.txt')
    elif teacher_choice == 2:
        #TODO Ver notas dos alunos. #TIP um print pela materia ja funciona porem, tem meios mais elegantes.
        print()
    elif teacher_choice == 3:
        #TODO Editar notas dos alunos. #TIP usar o RA do aluno como meio de busca para edicao.
        print()
    elif teacher_choice == 0:
        break
    else:
        print(f"\nNenhuma opcao corresponde com {teacher_choice}\n")
   

def edit_grades(subject, teacher_login, student_name, new_grade):
    json_load = FileService.FileService.json_load(MATERIAS_JSON)

    #verifica se o professor tem permissao.
    if json_load[subject]["professor"] != teacher_login:
        raise PermissionError("Acesso negado! Voce não pode editar essa máteria.")

    #Atualiza a nota do aluno
    for student in json_load[subject]["aluno"]:
        if student["nome"] == student_name:
            student["nota"] = new_grade
            break
    else:
        raise ValueError("Aluno nao foi encontrado")

    #Salva as alteracoes
    FileService.FileService.write_json(MATERIAS_JSON, json_load)


def add_student():