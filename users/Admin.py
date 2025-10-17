import random
import string
from src import FileService

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


def gerar_codigo_valido():
    while True:
        # Gera uma string aleatória de 8 caracteres (letras e números)
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if verificar_codigo(codigo):
            return codigo


def register():
    users = FileService.FileService.load_users()
    username = input("Nome: ")
    if username in users:
        print("⚠️ Usuario ja existe.")
        return
    password = input("Senha: ")
    FileService.FileService.save_user(username, password)
    print("✅ Usuario registrado com sucesso!")



"""codigo_valido = gerar_codigo_valido()
print("Código válido gerado:", codigo_valido)"""


