class Call:
    def __init__(self, seconds):
        self.seconds = seconds


class PhoneBill:
    def __init__(self, pricePerSecond):
        self.pricePerSecond = pricePerSecond
        self.calls = []

    def addCall(self, seconds):
        self.calls.append(Call(seconds))

    def changePrice(self, newPrice):
        self.pricePerSecond = newPrice

    def getBalance(self):
        total = 0

        for call in self.calls:
            total += call.seconds * self.pricePerSecond

        return total

    def printMovements(self):
        for index, call in enumerate(self.calls, start=1):
            print(
                f"Llamada {index}: "
                f"{call.seconds} segundos"
            )


# User 

bill = PhoneBill(0.5)

bill.addCall(60)
bill.addCall(120)

bill.printMovements()

print(bill.getBalance())
