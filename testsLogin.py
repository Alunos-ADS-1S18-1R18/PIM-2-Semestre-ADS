import hashlib



USER_FILE = "users.txt"


def hash_password(password):
    '''Create the hash SHA-256 of password'''
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    users = {}
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    username, stored_hash = parts
                    users[username] = stored_hash

    except FileNotFoundError:
        pass
    return users

def save_user(username, password):
    "Stores the username and hashed password"
    hashed = hash_password(password)
    with open(USER_FILE, "a") as file:
        file.write(f"{username}:{hashed}\n")

def register():
    users = load_users()
    username = input("Novo nome: ")
    if username in users:
        print("⚠️ Usuario ja existe.")
        return
    password = input("Password: ")
    save_user(username, password)
    print("✅ Usuario registrado com sucesso!")

def login():

    users = load_users()
    username = input("Usuario: ")
    password = input("Senha: ")

    hashed_input = hash_password(password)
    
    if username in users and users[username] == hashed_input:
        print("✅ Login autorizado!")
    else:
        print("❌ Nome de usuario ou senha invalidos.")

register()
login()

#TODO verificacao de arquivo vazio