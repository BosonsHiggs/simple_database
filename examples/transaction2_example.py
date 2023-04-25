from simple_database.simple_database import SimpleDatabase
from simple_database.transaction import Transaction

# Cria uma nova instância do banco de dados
db = SimpleDatabase("example.db")

# Adiciona alguns dados
db.set("key1", 10)
db.set("key2", 5)

# Cria uma transação
with Transaction(db) as tx:
    # Realiza algumas operações na transação
    tx.set("key1", tx.get("key1") + 1)
    tx.set("key2", tx.get("key2") - 1)

    # Verifica os valores dentro da transação
    print(tx.get("key1")) # Saída: 11
    print(tx.get("key2")) # Saída: 4

# Verifica os valores fora da transação (devem ser os mesmos)
print(db.get("key1")) # Saída: 11
print(db.get("key2")) # Saída: 4
