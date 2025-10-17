#classe estudante onde tudo relacionado ao professor sera inserido

'''4. Menu do Professor
 Exibir menu com opções:
1-Inserir notas dos alunos
2-Ver notas dos alunos
3-Editar notas
4-Novo aluno

'''
import Headers

from users.LoginService import geraLog


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
   

