from simple_database import SimpleDatabase, Master, Slave

# Cria um banco de dados
db = SimpleDatabase()

# Adiciona um dado no banco de dados
db.set("nome", "João")

# Cria um servidor Master na porta 8000
master = Master(db, "localhost", 8000)

# Cria dois servidores Slave que se conectam ao Master na porta 8000
slave1 = Slave(db, "localhost", 8000)
slave2 = Slave(db, "localhost", 8000)

# Imprime o dado do banco de dados em cada servidor
print("Master:", master.get_data("nome"))
print("Slave 1:", slave1.get_data("nome"))
print("Slave 2:", slave2.get_data("nome"))

# Modifica o dado no banco de dados
db.set("nome", "Maria")

# Imprime o dado do banco de dados em cada servidor novamente
print("Master:", master.get_data("nome"))
print("Slave 1:", slave1.get_data("nome"))
print("Slave 2:", slave2.get_data("nome"))
