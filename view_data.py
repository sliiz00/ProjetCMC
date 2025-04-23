import json
import os

def view_data():
    data_file = 'management_data.json'
    
    if not os.path.exists(data_file):
        print("No data file found. Please run the management system first to generate data.")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n=== CUSTOMERS ===")
    for customer_id, customer in data['customers'].items():
        print(f"\nCustomer ID: {customer_id}")
        print(f"Name: {customer['name']}")
        print(f"Email: {customer['email']}")
        print(f"Phone: {customer['phone']}")
        print(f"Address: {customer['address']}")
        print(f"City: Beni Mellal")
        
        print("\nRequests:")
        for request in customer['requests']:
            print(f"- {request['type']}: {request['description']} (Status: {request['status']})")
        
        print("\nEvaluations:")
        for eval in customer['evaluations']:
            print(f"- Rating: {eval['rating']}/5 - {eval['comment']}")
    
    print("\n=== EMPLOYEES ===")
    for employee_id, employee in data['employees'].items():
        print(f"\nEmployee ID: {employee_id}")
        print(f"Name: {employee['name']}")
        print(f"Position: {employee['position']}")
        print(f"Email: {employee['email']}")
        print(f"Phone: {employee['phone']}")
        print(f"Location: Beni Mellal")
        
        print("\nSalary History:")
        for salary in employee['salary_history']:
            print(f"- {salary['amount']} on {salary['date']}")
        
        print("\nPerformance Reviews:")
        for review in employee['performance_reviews']:
            print(f"- Rating: {review['rating']}/5 - {review['comments']}")
    
    print("\n=== TRANSACTIONS ===")
    for trans_id, transaction in data['transactions'].items():
        print(f"\nTransaction ID: {trans_id}")
        print(f"Customer ID: {transaction['customer_id']}")
        print(f"Amount: {transaction['amount']}")
        print(f"Type: {transaction['transaction_type']}")
        print(f"Description: {transaction['description']}")
        print(f"Date: {transaction['date']}")
        print(f"Location: Beni Mellal")

if __name__ == "__main__":
    view_data() 