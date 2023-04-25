from simple_database.simple_database import SimpleDatabase
from simple_database.replication import Master, Slave

# Cria uma nova instância do banco de dados
db = SimpleDatabase("example.db")

# Cria uma instância do mestre e adiciona alguns dados
master = Master(db, "localhost", 5000)
master.set_data("key1", "value1")
master.set_data("key2", "value2")

# Cria uma instância do escravo e sincroniza os dados
slave = Slave(db, "localhost", 5000)
print(slave.get_data("key1")) # Saída: "value1"
print(slave.get_data("key2")) # Saída: "value2"

# Modifica alguns dados no mestre
master.set_data("key1", "new_value1")
master.set_data("key2", "new_value2")

# Verifica se os dados foram sincronizados corretamente no escravo
print(slave.get_data("key1")) # Saída: "new_value1"
print(slave.get_data("key2")) # Saída: "new_value2"
