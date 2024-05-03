# UML Diagram and test case s codes

# UML Diagram Code

class Employee:
    def __init__(self, name, employee_id, department, job_title, basic_salary, age, date_of_birth, passport_details):
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.date_of_birth = date_of_birth
        self.passport_details = passport_details
        self.managed_employees = []

    def add_managed_employee(self, employee):
        self.managed_employees.append(employee)


class Event:
    def __init__(self, event_id, event_type, theme, date, time, duration, venue_address, client_id, guest_list,
                 catering_company, cleaning_company, decorations_company, entertainment_company, furniture_supply_company,
                 invoice):
        self.event_id = event_id
        self.event_type = event_type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue_address = venue_address
        self.client_id = client_id
        self.guest_list = guest_list
        self.catering_company = catering_company
        self.cleaning_company = cleaning_company
        self.decorations_company = decorations_company
        self.entertainment_company = entertainment_company
        self.furniture_supply_company = furniture_supply_company
        self.invoice = invoice


class Client:
    def __init__(self, client_id, name, address, contact_details, budget):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget


class Guest:
    def __init__(self, guest_id, name, address, contact_details):
        self.guest_id = guest_id
        self.name = name
        self.address = address
        self.contact_details = contact_details


class Supplier:
    def __init__(self, supplier_id, name, address, contact_details):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.contact_details = contact_details


# Test Cases Code

# Create some employees
employee1 = Employee("Susan Meyers", 47899, "Sales", "Manager", 37500, 45, "1979-05-15", "ABC12345")
employee2 = Employee("Shyam Sundar", 11234, "Sales", "Salesperson", 20000, 35, "1989-08-25", "DEF67890")
employee3 = Employee("Salma J Sam", 98637, "Sales", "Salesperson", 20000, 30, "1994-02-10", "GHI12345")

# Add managed employees to manager
employee1.add_managed_employee(employee2)
employee1.add_managed_employee(employee3)

# Create an event
event1 = Event(1, "Conference", "Tech", "2023-10-05", "09:00", 3, "Convention Center", 1, ["Guest1", "Guest2"], "Catering Co", "Cleaning Co", "Decorations Co", "Entertainment Co", "Furniture Supply Co", 5000)

# Create clients
client1 = Client(1, "Alice Johnson", "123 Elm St", "555-1234", 5000)
client2 = Client(2, "Bob Smith", "456 Oak St", "555-5678", 3000)

# Create guests
guest1 = Guest(1, "Laura", "789 Guest Lane", "234-567-8901")
guest2 = Guest(2, "Anabelle", "321 Main Road", "890-123-4567")

# Create suppliers
supplier1 = Supplier(1, "WholeTraders", "13 Supplier St", "133-436-7390")
supplier2 = Supplier(2, "Whole Market", "456 Supplier Ave", "987-654-3210")






















































