from simple_database.simple_database import SimpleDatabase

# Cria uma nova instância do banco de dados
db = SimpleDatabase("example.db")

# Adiciona alguns dados
db.set("key1", "value1")
db.set("key2", "value2")
db.set("key3", "value3")

# Cria um backup do banco de dados
db.create_backup("example_backup.db")

# Modifica alguns dados
db.set("key1", "new_value1")
db.set("key2", "new_value2")

# Restaura o backup
db.restore_backup("example_backup.db")

# Verifica se os dados foram restaurados corretamente
print(db.get("key1")) # Saída: "value1"
print(db.get("key2")) # Saída: "value2"
print(db.get("key3")) # Saída: "value3"
