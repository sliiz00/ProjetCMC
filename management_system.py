from datetime import datetime
from typing import List, Dict, Optional
import json
import os

class Customer:
    def __init__(self, customer_id: str, name: str, email: str, phone: str, address: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.requests: List[Dict] = []
        self.evaluations: List[Dict] = []

    def add_request(self, request_type: str, description: str, date: datetime = None):
        if date is None:
            date = datetime.now()
        self.requests.append({
            'type': request_type,
            'description': description,
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Pending'
        })

    def add_evaluation(self, rating: int, comment: str, date: datetime = None):
        if date is None:
            date = datetime.now()
        self.evaluations.append({
            'rating': rating,
            'comment': comment,
            'date': date.strftime('%Y-%m-%d %H:%M:%S')
        })

class Employee:
    def __init__(self, employee_id: str, name: str, position: str, email: str, phone: str):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.email = email
        self.phone = phone
        self.salary_history: List[Dict] = []
        self.performance_reviews: List[Dict] = []

    def add_salary_record(self, amount: float, date: datetime = None):
        if date is None:
            date = datetime.now()
        self.salary_history.append({
            'amount': amount,
            'date': date.strftime('%Y-%m-%d %H:%M:%S')
        })

    def add_performance_review(self, rating: int, comments: str, date: datetime = None):
        if date is None:
            date = datetime.now()
        self.performance_reviews.append({
            'rating': rating,
            'comments': comments,
            'date': date.strftime('%Y-%m-%d %H:%M:%S')
        })

class Transaction:
    def __init__(self, transaction_id: str, customer_id: str, amount: float, 
                 transaction_type: str, description: str, date: datetime = None):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.date = date if date else datetime.now()

class ManagementSystem:
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.employees: Dict[str, Employee] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.data_file = 'management_data.json'

    def add_customer(self, customer: Customer):
        self.customers[customer.customer_id] = customer

    def add_employee(self, employee: Employee):
        self.employees[employee.employee_id] = employee

    def add_transaction(self, transaction: Transaction):
        self.transactions[transaction.transaction_id] = transaction

    def get_customer_requests(self, customer_id: str) -> List[Dict]:
        if customer_id in self.customers:
            return self.customers[customer_id].requests
        return []

    def get_customer_evaluations(self, customer_id: str) -> List[Dict]:
        if customer_id in self.customers:
            return self.customers[customer_id].evaluations
        return []

    def get_employee_performance(self, employee_id: str) -> List[Dict]:
        if employee_id in self.employees:
            return self.employees[employee_id].performance_reviews
        return []

    def get_financial_summary(self) -> Dict:
        total_income = sum(t.amount for t in self.transactions.values() if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in self.transactions.values() if t.transaction_type == 'expense')
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': total_income - total_expenses
        }

    def save_data(self):
        data = {
            'customers': {cid: self._customer_to_dict(c) for cid, c in self.customers.items()},
            'employees': {eid: self._employee_to_dict(e) for eid, e in self.employees.items()},
            'transactions': {tid: self._transaction_to_dict(t) for tid, t in self.transactions.items()}
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.customers = {cid: self._dict_to_customer(c) for cid, c in data['customers'].items()}
                self.employees = {eid: self._dict_to_employee(e) for eid, e in data['employees'].items()}
                self.transactions = {tid: self._dict_to_transaction(t) for tid, t in data['transactions'].items()}

    def _customer_to_dict(self, customer: Customer) -> Dict:
        return {
            'customer_id': customer.customer_id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'requests': customer.requests,
            'evaluations': customer.evaluations
        }

    def _employee_to_dict(self, employee: Employee) -> Dict:
        return {
            'employee_id': employee.employee_id,
            'name': employee.name,
            'position': employee.position,
            'email': employee.email,
            'phone': employee.phone,
            'salary_history': employee.salary_history,
            'performance_reviews': employee.performance_reviews
        }

    def _transaction_to_dict(self, transaction: Transaction) -> Dict:
        return {
            'transaction_id': transaction.transaction_id,
            'customer_id': transaction.customer_id,
            'amount': transaction.amount,
            'transaction_type': transaction.transaction_type,
            'description': transaction.description,
            'date': transaction.date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def _dict_to_customer(self, data: Dict) -> Customer:
        customer = Customer(
            data['customer_id'],
            data['name'],
            data['email'],
            data['phone'],
            data['address']
        )
        customer.requests = data['requests']
        customer.evaluations = data['evaluations']
        return customer

    def _dict_to_employee(self, data: Dict) -> Employee:
        employee = Employee(
            data['employee_id'],
            data['name'],
            data['position'],
            data['email'],
            data['phone']
        )
        employee.salary_history = data['salary_history']
        employee.performance_reviews = data['performance_reviews']
        return employee

    def _dict_to_transaction(self, data: Dict) -> Transaction:
        return Transaction(
            data['transaction_id'],
            data['customer_id'],
            data['amount'],
            data['transaction_type'],
            data['description'],
            datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        )

# Example usage:
if __name__ == "__main__":
    # Initialize the management system
    system = ManagementSystem()
    
    # Create a customer from Beni Mellal
    customer = Customer(
        customer_id="C001",
        name="Ahmed Benali",
        email="ahmed@example.com",
        phone="+212 600 000 000",
        address="123 Rue Hassan II, Beni Mellal"
    )
    
    # Add a request from the customer
    customer.add_request(
        request_type="Plumbing Service",
        description="Need plumbing service in Beni Mellal"
    )
    
    # Add an evaluation from the customer
    customer.add_evaluation(
        rating=5,
        comment="Excellent service in Beni Mellal!"
    )
    
    # Add the customer to the system
    system.add_customer(customer)
    
    # Create an employee from Beni Mellal
    employee = Employee(
        employee_id="E001",
        name="Mohammed Alami",
        position="Plumber",
        email="mohammed@example.com",
        phone="+212 600 000 001"
    )
    
    # Add salary record for employee
    employee.add_salary_record(5000.00)
    
    # Add performance review
    employee.add_performance_review(
        rating=4,
        comments="Good work performance in Beni Mellal region"
    )
    
    # Add the employee to the system
    system.add_employee(employee)
    
    # Create a transaction
    transaction = Transaction(
        transaction_id="T001",
        customer_id="C001",
        amount=200.00,
        transaction_type="income",
        description="Plumbing service payment in Beni Mellal"
    )
    
    # Add the transaction to the system
    system.add_transaction(transaction)
    
    # Save all data
    system.save_data()
    
    # Load data (example of loading saved data)
    system.load_data()
    
    # Get financial summary
    financial_summary = system.get_financial_summary()
    print("Financial Summary:", financial_summary) 