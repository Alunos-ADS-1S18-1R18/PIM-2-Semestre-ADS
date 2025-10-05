"""
Armazena logins e senhas sem DB:
- Senhas são hasheadas com PBKDF2-HMAC-SHA256 + salt (200k iterações)
- O JSON contendo os registros é criptografado com Fernet (chave derivada da master_password via PBKDF2)
- Arquivo: credentials.bin (conteúdo criptografado)
- Arquivo metadata (não secreto): contains salts necessários (ex.: salt para derivar a chave do ficheiro)
"""

import os
import json
import base64
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

CREDENTIALS_FILE = "credentials.bin"
META_FILE = "credentials.meta.json"

# configurações
HASH_ITERS = 200_000
KDF_ITERS = 200_000
SALT_SIZE = 16  # bytes

backend = default_backend()

def _b64(x: bytes) -> str:
    return base64.urlsafe_b64encode(x).decode()

def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s.encode())

# Deriva uma chave (32 bytes) para Fernet a partir de uma master_password e um salt
def derive_fernet_key(master_password: str, salt: bytes, iters: int = KDF_ITERS) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iters,
        backend=backend
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)  # Fernet expects base64 key

# Hash da senha do usuário (para verificação). Retorna salt e hash (bytes)
def hash_password(password: str, salt: bytes = None, iters: int = HASH_ITERS):
    if salt is None:
        salt = os.urandom(SALT_SIZE)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iters)
    return salt, dk

# Carrega meta (salt para KDF etc.) ou cria novo
def load_or_create_meta():
    if os.path.exists(META_FILE):
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # criar meta novo
    meta = {
        "file_salt": _b64(os.urandom(SALT_SIZE)),
        "kdf_iters": KDF_ITERS,
        "hash_iters": HASH_ITERS
    }
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        os.chmod(META_FILE, 0o600)
    return meta

# Lê o ficheiro de credenciais (descriptografa com master_password)
def load_credentials(master_password: str):
    meta = load_or_create_meta()
    file_salt = _unb64(meta["file_salt"])
    key = derive_fernet_key(master_password, file_salt, meta.get("kdf_iters", KDF_ITERS))
    f = Fernet(key)
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE, "rb") as fh:
        token = fh.read()
    try:
        data = f.decrypt(token)
    except Exception as e:
        raise ValueError("Falha ao descriptografar o ficheiro. Master password incorreta?") from e
    return json.loads(data.decode())

# Salva credenciais (criptografa)
def save_credentials(creds: dict, master_password: str):
    meta = load_or_create_meta()
    file_salt = _unb64(meta["file_salt"])
    key = derive_fernet_key(master_password, file_salt, meta.get("kdf_iters", KDF_ITERS))
    f = Fernet(key)
    raw = json.dumps(creds).encode()
    token = f.encrypt(raw)
    with open(CREDENTIALS_FILE, "wb") as fh:
        fh.write(token)
    os.chmod(CREDENTIALS_FILE, 0o600)

# Adiciona usuário (armazena salt+hash em base64)
def add_user(login: str, password: str, master_password: str):
    creds = load_credentials(master_password)
    if login in creds:
        raise ValueError("Login já existe")
    salt, hashed = hash_password(password)
    creds[login] = {
        "salt": _b64(salt),
        "hash": _b64(hashed),
        "iters": HASH_ITERS
    }
    save_credentials(creds, master_password)
    print(f"Usuário '{login}' adicionado.")

# Verifica usuário
def verify_user(login: str, password: str, master_password: str) -> bool:
    creds = load_credentials(master_password)
    entry = creds.get(login)
    if not entry:
        return False
    salt = _unb64(entry["salt"])
    expected = _unb64(entry["hash"])
    iters = entry.get("iters", HASH_ITERS)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iters)
    return hashlib.compare_digest(dk, expected)

# Exemplo de uso
if __name__ == "__main__":
    master = input("Master password (mantê-la segura): ").strip()
    while True:
        action = input("A(Adicionar) / V(Verificar) / S(Sair): ").strip().upper()
        if action == "A":
            user = input("Login: ").strip()
            pwd = input("Senha: ").strip()
            add_user(user, pwd, master)
        elif action == "V":
            user = input("Login: ").strip()
            pwd = input("Senha: ").strip()
            ok = verify_user(user, pwd, master)
            print("Autenticado." if ok else "Credenciais inválidas.")
        elif action == "S":
            break
        else:
            print("Opção inválida.")
