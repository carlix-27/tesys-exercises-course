class BankAccount:
    def __init__(self, code):
        self.code = code
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True

        return False

    def getBalance(self):
        return self.balance
    


class Bank:
    def __init__(self):
        self.accounts = []

    def addAccount(self, account):
        self.accounts.append(account)

    def findAccount(self, code):
        for account in self.accounts:
            if account.code == code:
                return account

        return None

    def transfer(self, sourceCode, targetCode, amount):

        source = self.findAccount(sourceCode)
        target = self.findAccount(targetCode)

        if source is None or target is None:
            return False

        if source.withdraw(amount):
            target.deposit(amount)
            return True

        return False


# User
bank = Bank()

acc1 = BankAccount("001")
acc2 = BankAccount("002")

bank.addAccount(acc1)
bank.addAccount(acc2)

acc1.deposit(1000)

bank.transfer("001", "002", 300)

print(acc1.getBalance())
print(acc2.getBalance())
