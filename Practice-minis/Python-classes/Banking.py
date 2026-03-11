class Character:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def greet(self):
        print(f"wassup bro, I am {self.name}")

    def check_balance(self):
        print(f"balance: {self.balance}")

    def withdraw_from_bank(self, bank):
        ammount = float(input("Enter amount: "))
        self.balance += ammount
        bank.balance -= ammount

    def deposit_to_bank(self, bank):
        ammount = float(input("Enter amount: "))
        self.balance -= ammount
        bank.balance += ammount

class Bank:
    def __init__(self, balance):
        self.balance = balance



def main():
    player = Character("player", 100)
    central_bank = Bank(1000)
    eastern_bank = Bank(1000)
    western_bank = Bank(1000)
    banks = {
            "central": central_bank,
            "eastern": eastern_bank,
            "western": western_bank,
        }

    while True:
        selected_bank = input("which bank? ")
        if selected_bank == "q":
          break
        bank = banks.get(selected_bank)
        if bank is None:
            print("invalid bank")
            continue

        action = input("w or d? ")
        if action == "w":
            player.withdraw_from_bank(bank)
        elif action == "d":
            player.deposit_to_bank(bank)
        
        print(f"""
        Player balance: {player.balance}
        Central: {central_bank.balance}
        Eastern: {eastern_bank.balance}
        Western: {western_bank.balance}
        """)
        
main()