class BankAccount:

    def __init__(self, cbu, balance=0):
        self.cbu = cbu
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            print("El monto debe ser positivo")

    def withdraw(self, amount):
        if amount > 0:
            self.balance -= amount
        else:
            print("El monto debe ser positivo")

    def getBalance(self):
        return self.balance

    def getCBU(self):
        return self.cbu


account = BankAccount("123456789")

account.deposit(1000)
account.withdraw(300)

print("CBU:", account.getCBU())
print("Balance:", account.getBalance())