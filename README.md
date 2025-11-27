# PIM - 2º Semestre (ADS) — SmartClass (Python)

Descrição
--------
Aplicação em Python para gerenciamento de boletins (professores / alunos). Lê e grava dados em arquivos JSON/texto:
- materias.json — dados das matérias, professores e alunos
- users.txt — credenciais (usuario:sha256_hash)
- userLog.json — mapeamento login -> { teacher, subject } usado para área do professor

Requisitos
---------
- Python 3.8+
- Git
- (Opcional) compilador C para testar MainBoletim.c separadamente

Instalação (macOS / Linux)
---------
1. Clonar repositório:
   ```
   git clone https://github.com/Alunos-ADS-1S18-1R18/PIM-2-Semestre-ADS
   cd PIM-2-Semestre-ADS
   ```
2. Criar e ativar ambiente virtual:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instalar dependências (se existir requirements.txt):
   ```
   pip install -r requirements.txt
   ```
   Observação: o projeto usa apenas a biblioteca padrão do Python por enquanto.

Arquivos importantes
-------------------
- src/FileService.py — leitura/escrita de materias.json e users.txt
- users/LoginService.py — fluxo de login (Admin / Professor) e geração de hash de senha
- users/Admin.py — criação de professores, alunos e atribuições
- users/TeacherService.py — menu e edição de notas para professores
- materias.json — arquivo de dados (criado automaticamente se inexistente)
- users.txt — arquivo de credenciais (formato: username:sha256hash)
- userLog.json — associações de login a professor e matéria

Exemplo mínimo de materias.json
-------------------------------
```json
{
  "Matematica": {
    "Professor": "PROF1",
    "Alunos": [
      {
        "Nome": "Aluno Exemplo",
        "Turma": "1A",
        "RA": "ABC12345",
        "Nota": [6, 7, 8, 9]
      }
    ]
  }
}
```

Criar usuário ADMIN (hash)
--------------------------
Gere o hash SHA-256 da senha e adicione a linha em users.txt (ex: ADMIN:<hash>).

Exemplo para gerar hash no terminal:
```
python - <<'PY'
import hashlib
print(hashlib.sha256(b'minha_senha').hexdigest())
PY
```
Em seguida, edite (ou crie) users.txt e adicione:
```
ADMIN:<hash_gerado>
```

Executando a aplicação (modo rápido)
-----------------------------------
O projeto não possui um único main.py por padrão. Para iniciar o fluxo de login diretamente pelo interpretador:
```
python -c "from users.LoginService import System; System().login()"
```
Isso abre prompt para usuário/senha e direciona para as áreas Admin ou Professor conforme credenciais.

Rodando o utilitário C (opcional)
--------------------------------
Existe um utilitário em C (MainBoletim.c) que consome o mesmo formato de materias.json. Para compilar e executar:
```
gcc MainBoletim.c -o MainBoletim
./MainBoletim
```

Boas práticas
------------
- Faça backup dos arquivos materias.json, users.txt e userLog.json antes de alterações manuais.
- Prefira usar a interface Python (LoginService / Admin / TeacherService) para manipular dados — ela já faz validações.
- Use nomes de usuário em maiúsculas (o login converte input para upper()).

Contribuição
-----------
- Abra issues para bugs e melhorias.
- Use branches feature/* e envie PRs para revisão.

Contato
-------
Responsável/Equipe: GitHub: https://github.com/Alunos-ADS-UNIP