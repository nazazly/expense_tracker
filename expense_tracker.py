from expense import Expense
import datetime
import calendar

def main():
    print(f"⭐ Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    #set budget for this program
    budget = 1200

    # Get user inpuit for expense
    expense = get_user_expense()

    # Write their expense to a file
    save_expense_to_file(expense, expense_file_path)

    # Read and summarise expenses
    summarise_expense(expense_file_path, budget)

def get_user_expense():
    print(f"✔️  Getting User Expense")
    expense_date = input("Enter date of receipt: ")
    expense_name = input("Enter item: ")
    expense_amount = float(input("Enter amount: "))
    expense_categories = [
        "🍔 Food",
        "💸 Bills",
        "🚗 Transport",
        "🛍️  Shopping",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")

        # List the categories with an index
        for i, category_name in enumerate(expense_categories):

            # Since it starts at 0, using (i + 1) makes the starting number to 1, making it clearer to the user
            print(f"    {i + 1}. {category_name}")

        # Showcases what numbers can be selected
        value_range = f"[1 - {len(expense_categories)}]"

        # -1 due to the line 38. If user selects "1", they mean index 0
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        # Using len() instead of range(), just in case of any changes to the number of expense_categories
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index] 
            new_expense = Expense(
                date=expense_date, name=expense_name, category=selected_category, amount=expense_amount
                )
            return new_expense
        else:
            print("❌ Invalid category. PLease try again!")

# Storing inputs from user to a file, csv file will be printed after first input
def save_expense_to_file(expense, expense_file_path):
    print(f"✔️  Saving User Expense : {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding='utf-8') as f:
        f.write(f"{expense.date}, {expense.name}, {expense.amount}, {expense.category}\n")
    
# Reading out the inputs from the file
def summarise_expense(expense_file_path, budget):
    print(f"✔️  Summarising User Expense")
    expenses = []

    # Added encoding due to emojis used
    with open(expense_file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            expense_date, expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                date=expense_date, name=expense_name, amount=float(expense_amount), category=expense_category
                )
            expenses.append(line_expense)

    # Collates the expenses by category and displaying in dictionary format
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("⭐ Expense By Category: ")
    for key, amount in amount_by_category.items():
        print(f"    {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total spent ${total_spent:.2f} this month!")

    # Keep track of budget
    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining ${remaining_budget:.2f}")

    # Get the current date
    now = datetime.datetime.now()

    # Get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]

    # Calculate the remaining number of days in the current month
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(f"👉 Budget Per Day : ${daily_budget}")


if __name__ == "__main__":
    main()