from simple_database import SimpleDatabase, Security

db = SimpleDatabase("my_db", "/path/to/db")

# Criando um usuário com senha
Security.add_user("admin", "password123")

# Verificando se a senha é válida
if Security.authenticate_user("admin", "password123"):
    # Acesso permitido
    data = {"name": "John", "age": 30}
    db.set("user_data", data)
else:
    # Acesso negado
    print("Senha incorreta.")
