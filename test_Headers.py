def menu():
    while True:
        print("="*25)
        print("1 - Area Professor")
        print("2 - Area Aluno")
        print("0 = Sair")
        try:
            option = int(input("Digite uma opcao: "))
        except ValueError:
            print(f"opcao ivalida! favor digitar um valor numerico")
            continue
        match option:
            case 1:
                #TODO trazer/fazer funcoes relacionada com prefessor
                pass
            case 2:
                #TODO trazer/fazer funcoes relacionada com aluno
                pass
            case 0:
                break
            case _:
                print("Opcao nao encontrada favor inserir novamente")


menu()