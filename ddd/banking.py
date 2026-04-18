class Account:
    def __init__(self, clock=None, printer=None):
        self._clock = clock or _SystemClock()
        self._printer = printer or _ConsolePrinter()
        self._transactions = []

    def deposit(self, amount):
        self._transactions.append((self._clock.today(), amount))

    def withdraw(self, amount):
        self._transactions.append((self._clock.today(), -amount))

    def print_statement(self):
        self._printer.print("DATE | AMOUNT | BALANCE")
        running_balance = 0
        statement_lines = []

        for date, amount in self._transactions:
            running_balance += amount
            statement_lines.append((date, amount, running_balance))

        for date, amount, balance in reversed(statement_lines):
            self._printer.print(f"{date} | {amount:.2f} | {balance:.2f}")


class _SystemClock:
    def today(self):
        raise NotImplementedError("A clock dependency must provide today().")


class _ConsolePrinter:
    def print(self, line):
        print(line)
