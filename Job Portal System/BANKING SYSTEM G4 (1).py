import heapq
import datetime
from collections import deque

# ---------------- NODE AND LINKED LIST (Singly Linked List) ---------------- #
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display(self):
        current = self.head
        if not current:
            print("No transaction history found.")
            return
        while current:
            transaction = current.data
            print(f"To: {transaction['recipient_name']} - Amount: ${transaction['amount']} - Date: {transaction['date']}")
            current = current.next
    def get_transactions_list(self):
        transactions = []
        current = self.head
        while current:
            transactions.append(current.data)
            current = current.next
        return transactions
# ---------------- CUSTOMER ACCOUNT SYSTEM ---------------- #
class Customer:
    def __init__(self, customer_id, name, phone, account_number, has_atm=False, has_cbe_birr=False, priority=5):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.account_number = account_number
        self.account_balance = 500
        self.transactions = LinkedList()
        self.transaction_stack = []
        self.has_atm = has_atm
        self.has_cbe_birr = has_cbe_birr
        self.priority = priority

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.transaction_stack.append(transaction)

    def undo_last_transaction(self):
        if not self.transaction_stack:
            print("No transaction to undo.")
            return
        
        last_transaction = self.transaction_stack.pop()
        self.account_balance += last_transaction['amount']
        
        print(f"Undo successful. Reversed transaction of ${last_transaction['amount']}.")

    def receive_sms(self, transaction):
        print(f"SMS to {self.phone}: Transaction of ${transaction['amount']} to {transaction['recipient_name']} completed.")
    
    def send_recommendation(self):
        if self.has_atm or self.has_cbe_birr:
            return f"Thank you for using our banking services, {self.name}. For a better experience, continue using your bank's ATM or CBE Birr services."
        else:
            return f"Recommendation: {self.name}, you do not have ATM or CBE Birr services. Please visit the bank to activate them."

    def display_transactions(self):
        self.transactions.display()

    def generate_receipt(self):
        receipt = f"""
        --- Receipt ---
        Customer ID: {self.customer_id}
        Name: {self.name}
        Account Number: {self.account_number}
        Current Balance: ${self.account_balance}
        
        --- Transaction History ---
        """
        transactions = self.transactions.get_transactions_list()
        if not transactions:
            receipt += "No transaction history found.\n"
        else:
            for transaction in transactions:
                receipt += f"To: {transaction['recipient_name']} - Amount: ${transaction['amount']} - Date: {transaction['date']}\n"
        
        receipt += f"""
        --- Recommendation ---
        {self.send_recommendation()}
        --- End of Receipt ---
        """
        return receipt

# ---------------- TRANSACTION MANAGEMENT ---------------- #
class TransactionSystem:
    def __init__(self):
        self.vip_queue = []  # Priority queue
        self.standard_queue = deque()
        self.customers = {}  # Store customers by ID for easy access

    def add_customer(self, customer):
        self.customers[customer.customer_id] = customer  # Store the customer
        if customer.priority < 3:
            heapq.heappush(self.vip_queue, (customer.priority, customer.customer_id))
        else:
            self.standard_queue.append(customer.customer_id)

    def process_next_customer(self):
        if self.vip_queue:
            _, customer_id = heapq.heappop(self.vip_queue)
        elif self.standard_queue:
            customer_id = self.standard_queue.popleft()
        else:
            print("No customers to process.")
            return None
        return self.customers[customer_id]

    def display_transactions(self, customer):
        customer.display_transactions()

# ---------------- USER INPUT WITH ERROR HANDLING ---------------- #
def get_valid_integer(prompt, length=None):
    while True:
        try:
            value = int(input(prompt))
            if length and len(str(value)) != length:
                print(f"Input must be exactly {length} digits.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 50:
                print("Amount must be at least 50 Birr.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_string(prompt):
    while True:
        value = input(prompt).strip()
        if value.isalpha():
            return value
        print("Invalid input. Please enter a valid name.")

def get_valid_phone(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and len(value) == 10 and value.startswith("09"):
            return value
        print("Invalid phone number. It must start with '09' and be 10 digits long.")

def get_yes_no(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ["yes", "no"]:
            return value == "yes"
        print("Invalid input. Please enter 'yes' or 'no'.")

def is_within_working_hours():
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(12, 18)
    end_time = datetime.time(20, 10)
    return start_time <= current_time <= end_time

def main():
    if not is_within_working_hours():
        print("The banking system is currently closed. Please try again between 2 PM and 11 PM.")
        return
    
    transaction_system = TransactionSystem()
    while True:
        print("\nEnter customer details (or type 'start' to begin transactions):")
        user_input = input("Type 'start' to begin transactions or press Enter to add a customer: ").strip().lower()
        if user_input == "start":
            break
        
        customer_id = get_valid_integer("Enter Customer ID: ")
        name = get_valid_string("Enter Customer Name: ")
        phone = get_valid_phone("Enter Customer Phone Number: ")
        account_number = get_valid_integer("Enter Account Number: ", 10)
        has_atm = get_yes_no("Do you have an ATM card? (yes/no): ")
        has_cbe_birr = get_yes_no("Do you have CBE Birr? (yes/no): ")
        priority = get_valid_integer("Enter Priority (1-5, 1 is highest): ")
        
        customer = Customer(customer_id, name, phone, account_number, has_atm, has_cbe_birr, priority)
        transaction_system.add_customer(customer)
    
    while True:
        print("\n1. Perform Transaction\n2. Display Transactions\n3. Undo Last Transaction\n4. Generate Receipt\n5. Exit")
        choice = get_valid_integer("Select an option: ")
        
        if choice == 1:
            customer = transaction_system.process_next_customer()
            if customer:
                recipient_name = get_valid_string("Enter Recipient Name: ")
                amount = get_valid_float("Enter Transaction Amount: ")
                
                transaction = {
                    'recipient_name': recipient_name,
                    'amount': amount,
                    'date': datetime.date.today().strftime("%Y-%m-%d")
                }
                
                customer.add_transaction(transaction)
                customer.account_balance -= amount
                customer.receive_sms(transaction)
                print(customer.send_recommendation())  # Print recommendation after transaction
            
        elif choice == 2:
            customer_id = get_valid_integer("Enter Customer ID to display transactions: ")
            if customer_id in transaction_system.customers:
                transaction_system.display_transactions(transaction_system.customers[customer_id])
            else:
                print("Customer not found.")
                
        elif choice == 3:
            customer_id = get_valid_integer("Enter Customer ID to undo last transaction: ")
            if customer_id in transaction_system.customers:
                transaction_system.customers[customer_id].undo_last_transaction()
            else:
                print("Customer not found.")
        
        elif choice == 4:
            customer_id = get_valid_integer("Enter Customer ID to generate receipt: ")
            if customer_id in transaction_system.customers:
                receipt = transaction_system.customers[customer_id].generate_receipt()
                print(receipt)
            else:
                print("Customer not found.")

        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()