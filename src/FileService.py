import json
import os
from users import LoginService

#TODO conversao do arquivo json para csv aparentemente e melhor para se ler em C



class FileService:
    GRADE_FILE = "materias.json"
    USER_FILE = "users.txt"


    @staticmethod
    def json_load():
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

    @staticmethod
    def load_users():
        '''Carrega os usuarios que possui login'''
        users = {}
        try:
            with open(FileService.USER_FILE, 'r') as file:
                for line in file:
                    line = line.strip()
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) == 2:
                            username, stored_hash = parts
                            users[username] = stored_hash
        except FileNotFoundError:
            pass
        return users
        
    @staticmethod
    def save_user(username, password):
        """Salva o nome de usuario e sua senha hash"""
        hashed = LoginService.System.hash_password(password)
        with open(FileService.USER_FILE, "a") as file:
            file.write(f"{username}:{hashed}\n")
            
def set_teacher(subject, teacher_name):
    data = FileService.json_load(FileService.GRADE_FILE)

    if subject in data:
        data[subject]["Professor"] = teacher_name

    else:
        data[subject] = {
            "Professor": teacher_name,
            "Alunos": []
        }
    FileService.write_json()
    print(f"Professor {teacher_name} atribuido a materia {subject}")

