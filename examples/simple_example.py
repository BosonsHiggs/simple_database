from simple_database import SimpleDatabase

db = SimpleDatabase("my_db")

# Adiciona um registro
db.put("my_key", {"foo": "bar"})

# Recupera um registro
record = db.get("my_key")
print(record)  # Saída: {"foo": "bar"}

# Remove um registro
db.delete("my_key")

# Backup do banco de dados
db.backup("my_backup.db")

# Restaura o banco de dados a partir de um backup
db.restore("my_backup.db")
