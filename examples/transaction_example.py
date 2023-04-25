from simple_database import SimpleDatabase
from transaction import transactional, transaction_manager


class Bank:
    def __init__(self):
        self.db = SimpleDatabase("bank")

    @transactional
    def transfer(self, source: str, destination: str, amount: float) -> None:
        self.db.decrement(source, amount)
        self.db.increment(destination, amount)

    def balance(self, account: str) -> float:
        return self.db.get(account, default=0)

    def begin_transaction(self):
        transaction_manager.begin_transaction()

    def commit_transaction(self):
        transaction_manager.commit_transaction()

    def rollback_transaction(self):
        transaction_manager.rollback_transaction()


bank = Bank()
bank.db.put("John", 1000.0)
bank.db.put("Mary", 500.0)
print(bank.balance("John"))  # Saída: 1000.0
print(bank.balance("Mary"))  # Saída: 500.0

bank.begin_transaction()
bank.transfer("John", "Mary", 300.0)
print(bank.balance("John"))  # Saída: 700.0
print(bank.balance("Mary"))  # Saída: 800.0
bank.rollback_transaction()
print(bank.balance("John"))  # Saída: 1000.0
print(bank.balance("Mary"))  # Saída: 500.0

bank.begin_transaction()
bank.transfer("John", "Mary", 300.0)
print(bank.balance("John"))  # Saída: 700.0
print(bank.balance("Mary"))  # Saída: 800.0
bank.commit_transaction()
print(bank.balance("John"))  # Saída: 700.0
print(bank.balance("Mary"))  # Saída: 800.0
