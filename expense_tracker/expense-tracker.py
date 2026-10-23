import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path


DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["name", "amount", "category"]


@dataclass
class Expense:
	name: str
	amount: Decimal
	category: str


def load_expenses():
	"""Load saved expenses, or start with an empty list if no CSV exists."""
	if not DATA_FILE.exists():
		return []

	expenses = []
	try:
		with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
			for row in csv.DictReader(file):
				try:
					amount = Decimal(row["amount"])
					if amount.is_finite() and amount > 0:
						expenses.append(
							Expense(row["name"].strip(), amount, row["category"].strip())
						)
				except (KeyError, TypeError, InvalidOperation):
					continue
	except (OSError, csv.Error) as error:
		print(f"Could not read expenses: {error}")
	return expenses


def save_expenses(expenses):
	"""Write all current expenses to the CSV database."""
	try:
		with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
			writer = csv.DictWriter(file, fieldnames=FIELDS)
			writer.writeheader()
			for expense in expenses:
				writer.writerow(
					{
						"name": expense.name,
						"amount": str(expense.amount),
						"category": expense.category,
					}
				)
	except OSError as error:
		print(f"Could not save expenses: {error}")


def display_expenses(expenses):
	if not expenses:
		print("No expenses recorded.")
		return

	print("\n#   Name                         Amount       Category")
	print("-" * 62)
	for number, expense in enumerate(expenses, 1):
		print(f"{number:<4}{expense.name[:27]:<29}${expense.amount:>9.2f}   {expense.category}")
	total = sum((expense.amount for expense in expenses), Decimal("0"))
	print(f"\nTotal: ${total:.2f}")


def add_expense(expenses):
	name = input("Name: ").strip()
	if not name:
		print("Name cannot be empty.")
		return

	try:
		amount = Decimal(input("Amount: ").strip())
		if not amount.is_finite() or amount <= 0:
			raise InvalidOperation
	except InvalidOperation:
		print("Enter a valid amount greater than zero.")
		return

	category = input("Category: ").strip()
	if not category:
		print("Category cannot be empty.")
		return

	expenses.append(Expense(name, amount, category))
	save_expenses(expenses)
	print("Expense saved.")


def remove_expense(expenses):
	if not expenses:
		print("No expenses to remove.")
		return
	display_expenses(expenses)
	try:
		number = int(input("Expense number to remove (0 to cancel): "))
	except ValueError:
		print("Please enter a valid number.")
		return
	if number == 0:
		return
	if not 1 <= number <= len(expenses):
		print("That expense number does not exist.")
		return
	removed = expenses.pop(number - 1)
	save_expenses(expenses)
	print(f"Removed {removed.name}.")


def main():
	expenses = load_expenses()
	print("Expense Tracker")
	while True:
		print("\n1. Add expense\n2. View expenses\n3. Remove expense\n4. Exit")
		choice = input("Choose an option: ").strip()
		if choice == "1":
			add_expense(expenses)
		elif choice == "2":
			display_expenses(expenses)
		elif choice == "3":
			remove_expense(expenses)
		elif choice == "4":
			print("Goodbye!")
			break
		else:
			print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
	main()
