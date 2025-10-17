import json
import os
from users import LoginService


class FileService:
    GRADE_FILE = 'materias.json'
    USER_FILE = "users.txt"



    @staticmethod
    def open_json():
        """Abre o JSON, cria um novo se não existir, e retorna o dicionário."""
        if not os.path.exists(FileService.GRADE_FILE):
            print('Arquivo não encontrado, criando um novo...')
            data = {}
            FileService.write_json(data)
            return data

        with open(FileService.GRADE_FILE, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("Arquivo vazio ou corrompido, recriando...")
                data = {}
                FileService.write_json(data)
        return data

    @staticmethod
    def write_json(data):
        """Grava o dicionário completo no arquivo JSON."""
        with open(FileService.GRADE_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    #trocar o locar da funcao.
    @staticmethod
    def add_subject(subject_name):
        """Adiciona uma nova matéria se ela ainda não existir."""
        data = FileService.open_json()
        if subject_name not in data:
            data[subject_name] = []
            FileService.write_json(data)
            print(f"Matéria '{subject_name}' criada com sucesso!")
        else:
            print(f"Matéria '{subject_name}' já existe.")

    @staticmethod
    def add_student(subject_name, ra, nota, media):
        """Adiciona um aluno a uma matéria existente."""
        data = FileService.open_json()
        # adiciona o aluno
        aluno = {"RA": ra, "Nota": nota, "Média": media}
        data[subject_name].append(aluno)

        FileService.write_json(data)
        print(f"Aluno RA {ra} adicionado à matéria '{subject_name}' com sucesso!")

    @staticmethod
    def load_users():
        '''Carrega os usuarios que possui login'''
        users = {}
        try:
            with open(FileService.USER_FILE, 'r') as file:
                for line in file:
                    username, stored_hash = line.strip().split(":")
                    users[username] = stored_hash
        except FileNotFoundError:
            pass
        return users
        
    @staticmethod
    def save_user(username, password):
        """Salva o nome de usuario e sua senha hash"""
        hashed = LoginService.LoginSevice.hash_password(password)
        with open(FileService.USER_FILE, "a") as file:
            file.write(f"{username}:{hashed}\n")
            
# --- Exemplo de uso ---

"""FileService.add_subject("Matemática")
FileService.add_subject("Biologia")
FileService.add_subject("Fisica")
FileService.add_subject("Portugues")
FileService.add_subject("Ingles")
FileService.add_subject("Filosofia")
FileService.add_subject("Sociologia")
FileService.add_subject("Quimica")
FileService.add_subject("Geografia")
FileService.add_subject("Educaçao Fisica")


FileService.add_subject("História")


print(json.dumps(FileService.open_json(), indent=4, ensure_ascii=False))
"""
