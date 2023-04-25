import functools
from typing import Any, Callable, List


def transactional(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.begin_transaction()
        try:
            result = func(self, *args, **kwargs)
            self.commit_transaction()
            return result
        except Exception as e:
            self.rollback_transaction()
            raise e

    return wrapper


class TransactionManager:
    def __init__(self) -> None:
        self.transactions: List[List[Callable[..., Any]]] = []

    def begin_transaction(self) -> None:
        self.transactions.append([])

    def commit_transaction(self) -> None:
        self.transactions.pop()

    def rollback_transaction(self) -> None:
        transaction = self.transactions.pop()
        while transaction:
            func = transaction.pop()
            func()


transaction_manager = TransactionManager()
