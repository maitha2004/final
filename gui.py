import pickle
import tkinter as tk
from tkinter import messagebox,ttk

#
# PUBLIC VARIABLES
#

# Base Variables
root = tk.Tk()
notebook = ttk.Notebook(root)
style = ttk.Style()

# Frames
employee_frame = ttk.Frame(notebook)
event_frame = ttk.Frame(notebook)
client_frame = ttk.Frame(notebook)
venue_frame = ttk.Frame(notebook)
guest_frame = ttk.Frame(notebook)
supplier_frame = ttk.Frame(notebook)

# Class Variables

# Employee
input_frame = tk.Frame(employee_frame, padx=3, pady=12)
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
list_frame = tk.Frame(employee_frame, padx=12, pady=12)
list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Department", "Title", "Salary"), show="headings")
entries = []

# Event
event_input_frame = tk.Frame(event_frame, padx=3, pady=12)
event_input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
event_list_frame = tk.Frame(event_frame, padx=12, pady=12)
event_list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
event_tree = ttk.Treeview(event_list_frame, columns=("ID", "Type", "Theme", "Date", "Time"), show="headings")
event_entries = []

# Client
client_input_frame = tk.Frame(client_frame, padx=3, pady=12)
client_input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
client_list_frame = tk.Frame(client_frame, padx=12, pady=12)
client_list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
client_tree = ttk.Treeview(client_list_frame, columns=("ID", "Name", "Address", "Contact Details", "Budget"), show="headings")
client_entries = []

# Supplier
supplier_input_frame = tk.Frame(supplier_frame, padx=3, pady=12)
supplier_input_frame.grid(row=0, column=0, sticky="nsew")
supplier_list_frame = tk.Frame(supplier_frame, padx=12, pady=12)
supplier_list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
supplier_tree = ttk.Treeview(supplier_list_frame, columns=("ID", "Name", "Address", "Contact Details"), show="headings")
supplier_entries = []

# Venue
guest_input_frame = tk.Frame(guest_frame, padx=3, pady=12)
guest_input_frame.grid(row=0, column=0, sticky="nsew")
guest_list_frame = tk.Frame(guest_frame, padx=12, pady=12)
guest_list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
guest_tree = ttk.Treeview(guest_list_frame, columns=("ID", "Name", "Address", "Contact Details"), show="headings")
guest_entries = []

# Guests
venue_input_frame = tk.Frame(venue_frame, padx=3, pady=12)
venue_input_frame.grid(row=0, column=0, sticky="nsew")
venue_list_frame = tk.Frame(venue_frame, padx=12, pady=12)
venue_list_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
venue_tree = ttk.Treeview(venue_list_frame,columns=("ID", "Name", "Address", "Contact Details", "Min Guests", "Max Guests"), show="headings")
venue_entries = []


#
# Class for management of data and files
#


class DataManagement:
    @staticmethod
    def save_data(obj, filename):
        with open(filename, 'wb') as file:
            pickle.dump(obj, file)

    @staticmethod
    def load_data(filename):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None  # Return None if the file does not exist

    @staticmethod
    def generic_save(obj, filename):
        data = DataManagement.load_data(filename) or []
        data.append(obj)
        DataManagement.save_data(data, filename)

    @staticmethod
    def generic_load(filename):
        return DataManagement.load_data(filename)

    @staticmethod
    def generic_delete(identifier, id_field, filename):
        data = DataManagement.load_data(filename) or []
        data = [item for item in data if getattr(item, id_field) != identifier]
        DataManagement.save_data(data, filename)

    @staticmethod
    def generic_update(identifier, id_field, updates, filename):
        data = DataManagement.load_data(filename) or []
        for item in data:
            if getattr(item, id_field) == identifier:
                item.__dict__.update(updates)
                break
        DataManagement.save_data(data, filename)

    @staticmethod
    def clear_entries():
        MainApp.name_entry.delete(0, tk.END)
        MainApp.id_entry.delete(0, tk.END)
        MainApp.department_entry.delete(0, tk.END)
        MainApp.title_entry.delete(0, tk.END)
        MainApp.salary_entry.delete(0, tk.END)
        MainApp.manager_id_entry.delete(0, tk.END)

#
# Classes for Object Types
#


class Employee:
    def __init__(self, name, employee_id, department, job_title, basic_salary, age, dob, passport_details, manager_id=None):
        if not name or not isinstance(name, str):
            raise ValueError("Invalid name")
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.dob = dob
        self.passport_details = passport_details
        self.manager_id = manager_id
        self.subordinates = []

    def add_subordinate(self, employee):
        self.subordinates.append(employee)

    def remove_subordinate(self, employee_id):
        self.subordinates = [sub for sub in self.subordinates if sub.employee_id != employee_id]

    def get_subordinates(self):
        return self.subordinates
    @staticmethod
    def save(employee, filename="employees.pkl"):
        employees = Employee.load_all(filename) or []
        employees.append(employee)
        DataManagement.save_data(employees, filename)

    @staticmethod
    def load_all(filename="employees.pkl"):
        return DataManagement.load_data(filename)

    @staticmethod
    def update(employee_id, updates, filename="employees.pkl"):
        employees = Employee.load_all(filename) or []
        for emp in employees:
            if emp.employee_id == employee_id:
                emp.__dict__.update(updates)
                break
        DataManagement.save_data(employees, filename)

    @staticmethod
    def delete(employee_id, filename="employees.pkl"):
        employees = Employee.load_all(filename) or []
        employees = [emp for emp in employees if emp.employee_id != employee_id]
        DataManagement.save_data(employees, filename)

class Event:
    def __init__(self, event_id, event_type, theme, date, time, duration, venue, client, suppliers):
        self.event_id = event_id
        self.event_type = event_type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue = venue
        self.client = client
        self.suppliers = suppliers
        self.guest_list = []

    def add_guest(self, guest):
        self.guest_list.append(guest)

    def remove_guest(self, guest_id):
        self.guest_list = [guest for guest in self.guest_list if guest.guest_id != guest_id]

    def get_guest_list(self):
        return self.guest_list

    @staticmethod
    def save(event, filename="events.pkl"):
        events = Event.load_all(filename) or []
        events.append(event)
        DataManagement.save_data(events, filename)

    @staticmethod
    def load_all(filename="events.pkl"):
        return DataManagement.load_data(filename)

    @staticmethod
    def update(event_id, updates, filename="events.pkl"):
        events = Event.load_all(filename) or []
        for evt in events:
            if evt.event_id == event_id:
                evt.__dict__.update(updates)
                break
        DataManagement.save_data(events, filename)

    @staticmethod
    def delete(event_id, filename="events.pkl"):
        events = Event.load_all(filename) or []
        events = [evt for evt in events if evt.event_id != event_id]
        DataManagement.save_data(events, filename)

class Client:
    def __init__(self, client_id, name, address, contact_details, budget):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget

    FILENAME = "clients.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, client_id):
        DataManagement.generic_delete(client_id, 'client_id', cls.FILENAME)

    @classmethod
    def update(cls, client_id, updates):
        DataManagement.generic_update(client_id, 'client_id', updates, cls.FILENAME)

class Supplier:
    def __init__(self, supplier_id, name, address, contact_details):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
    FILENAME = "suppliers.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, supplier_id):
        DataManagement.generic_delete(supplier_id, 'supplier_id', cls.FILENAME)

    @classmethod
    def update(cls, supplier_id, updates):
        DataManagement.generic_update(supplier_id, 'supplier_id', updates, cls.FILENAME)

class Guest:
    def __init__(self, guest_id, name, address, contact_details):
        self.guest_id = guest_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
    FILENAME = "guests.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, guest_id):
        DataManagement.generic_delete(guest_id, 'guest_id', cls.FILENAME)

    @classmethod
    def update(cls, guest_id, updates):
        DataManagement.generic_update(guest_id, 'guest_id', updates, cls.FILENAME)

class Venue:
    def __init__(self, venue_id, name, address, contact_details, min_guests, max_guests):
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.min_guests = min_guests
        self.max_guests = max_guests
    FILENAME = "venues.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, venue_id):
        DataManagement.generic_delete(venue_id, 'venue_id', cls.FILENAME)

    @classmethod
    def update(cls, venue_id, updates):
        DataManagement.generic_update(venue_id, 'venue_id', updates, cls.FILENAME)

class Event:
    def __init__(self, event_id, event_type, theme, date, time, duration, venue, client, suppliers):
        self.event_id = event_id
        self.event_type = event_type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue = venue
        self.client = client
        self.suppliers = suppliers
        self.guest_list = []

    def add_guest(self, guest):
        self.guest_list.append(guest)

    def remove_guest(self, guest_id):
        self.guest_list = [guest for guest in self.guest_list if guest.guest_id != guest_id]

    def get_guest_list(self):
        return self.guest_list

    @staticmethod
    def save(event, filename="events.pkl"):
        events = Event.load_all(filename) or []
        events.append(event)
        DataManagement.save_data(events, filename)

    @staticmethod
    def load_all(filename="events.pkl"):
        return DataManagement.load_data(filename)

    @staticmethod
    def update(event_id, updates, filename="events.pkl"):
        events = Event.load_all(filename) or []
        for evt in events:
            if evt.event_id == event_id:
                evt.__dict__.update(updates)
                break
        DataManagement.save_data(events, filename)

    @staticmethod
    def delete(event_id, filename="events.pkl"):
        events = Event.load_all(filename) or []
        events = [evt for evt in events if evt.event_id != event_id]
        DataManagement.save_data(events, filename)

class Client:
    def __init__(self, client_id, name, address, contact_details, budget):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget

    FILENAME = "clients.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, client_id):
        DataManagement.generic_delete(client_id, 'client_id', cls.FILENAME)

    @classmethod
    def update(cls, client_id, updates):
        DataManagement.generic_update(client_id, 'client_id', updates, cls.FILENAME)

class Supplier:
    def __init__(self, supplier_id, name, address, contact_details):
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
    FILENAME = "suppliers.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, supplier_id):
        DataManagement.generic_delete(supplier_id, 'supplier_id', cls.FILENAME)

    @classmethod
    def update(cls, supplier_id, updates):
        DataManagement.generic_update(supplier_id, 'supplier_id', updates, cls.FILENAME)

class Guest:
    def __init__(self, guest_id, name, address, contact_details):
        self.guest_id = guest_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
    FILENAME = "guests.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, guest_id):
        DataManagement.generic_delete(guest_id, 'guest_id', cls.FILENAME)

    @classmethod
    def update(cls, guest_id, updates):
        DataManagement.generic_update(guest_id, 'guest_id', updates, cls.FILENAME)

class Venue:
    def __init__(self, venue_id, name, address, contact_details, min_guests, max_guests):
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.min_guests = min_guests
        self.max_guests = max_guests
    FILENAME = "venues.pkl"

    def save(self):
        DataManagement.generic_save(self, self.FILENAME)

    @classmethod
    def load_all(cls):
        return DataManagement.generic_load(cls.FILENAME)

    @classmethod
    def delete(cls, venue_id):
        DataManagement.generic_delete(venue_id, 'venue_id', cls.FILENAME)

    @classmethod
    def update(cls, venue_id, updates):
        DataManagement.generic_update(venue_id, 'venue_id', updates, cls.FILENAME)

# CODE FOR UI ACTIONS

#
# Employee UI Class
#

class EmployeeForm:
    @staticmethod
    def add_employee(name_entry, id_entry, department_entry, title_entry, salary_entry, manager_id_entry, tree):
        MainApp.add_employee(name_entry, id_entry, department_entry, title_entry, salary_entry, manager_id_entry, tree)

    @staticmethod
    def update_employee(name_entry, department_entry, title_entry, salary_entry, manager_id_entry, tree):
        MainApp.update_employee(name_entry, department_entry, title_entry, salary_entry, manager_id_entry, tree)

    @staticmethod
    def delete_employee(tree):
        MainApp.delete_employee(tree)

    @staticmethod
    def refresh_employee_view(tree):
        MainApp.refresh_employee_view(tree)


#
# Event UI Class
#

class EventForm:

    @staticmethod
    def refresh_event_view(tree):
        for item in tree.get_children():
            tree.delete(item)
        clients = Client.load_all()
        for client in clients:
            tree.insert('', 'end', values=(client.client_id, client.name, client.address, client.contact_details, client.budget))

    @staticmethod
    def add_event(event_id,event_type,theme,date,time,duration,venue,client,suppliers):
          try:
            new_event = Event(
                event_id=int(event_id.get()),
                event_type=event_type.get(),
                theme=theme.get(),
                date=date.get(),
                time=time.get(),
                duration=duration.get(),
                venue=venue.get(),
                client=client.get(),
                suppliers=suppliers.get()
            )
            new_event.save()
            messagebox.showinfo("Success", "Event added successfully")
            DataManagement.clear_entries([event_id,event_type,theme,date,time,duration,venue,client,suppliers])
            EventForm.refresh_event_view(event_tree)
          except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def update_event():
        selected_item = event_tree.selection()[0]
        selected_event_id = event_tree.item(selected_item)['values'][0]
        try:
            updates = {
                'event_type': MainApp.event_type_entry.get(),
                'theme': MainApp.theme_entry.get(),
                'date': MainApp.date_entry.get(),
                'time': MainApp.time_entry.get(),
                'duration': MainApp.duration_entry.get(),
                'venue': MainApp.venue_entry.get(),
                'client': MainApp.client_entry.get(),
                'suppliers': MainApp.suppliers_entry.get().split(",")
            }
            Event.update(selected_event_id, updates)
            messagebox.showinfo("Success", "Event updated successfully")
            EventForm.refresh_event_view()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def delete_event(event_tree):
        selected_item = event_tree.selection()[0]
        selected_event_id = event_tree.item(selected_item)['values'][0]
        try:
            Event.delete(selected_event_id)
            messagebox.showinfo("Success", "Event deleted successfully")
            EventForm.refresh_event_view(event_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))
#
# Client UI Class
#

class ClientForm:
    @staticmethod
    def refresh_client_view(tree):
        for item in tree.get_children():
            tree.delete(item)
        clients = Client.load_all()
        for client in clients:
            tree.insert('', 'end', values=(client.client_id, client.name, client.address, client.contact_details, client.budget))

    @staticmethod
    def add_client(client_window, client_id_entry, client_name_entry, client_address_entry, client_contact_details_entry, client_budget_entry):
        try:
            new_client = Client(
                client_id=int(client_id_entry.get()),
                name=client_name_entry.get(),
                address=client_address_entry.get(),
                contact_details=client_contact_details_entry.get(),
                budget=float(client_budget_entry.get())
            )
            new_client.save()
            messagebox.showinfo("Success", "Client added successfully")
            DataManagement.clear_entries([client_id_entry, client_name_entry, client_address_entry, client_contact_details_entry, client_budget_entry])
            ClientForm.refresh_client_view(client_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def update_client(client_tree, name_entry, client_address_entry, client_contact_details_entry, client_budget_entry):
        selected_item = client_tree.selection()[0]
        selected_client_id = client_tree.item(selected_item)['values'][0]
        try:
            updates = {
                'name': name_entry.get(),
                'address': client_address_entry.get(),
                'contact_details': client_contact_details_entry.get(),
                'budget': float(client_budget_entry.get())
            }
            Client.update(selected_client_id, updates)
            messagebox.showinfo("Success", "Client updated successfully")
            ClientForm.refresh_client_view(client_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def delete_client(client_tree):
        selected_item = client_tree.selection()[0]
        selected_client_id = client_tree.item(selected_item)['values'][0]
        try:
            Client.delete(selected_client_id)
            messagebox.showinfo("Success", "Client deleted successfully")
            ClientForm.refresh_client_view(client_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

#
# Supplier UI Class
#

class SupplierForm:
    @staticmethod
    def refresh_supplier_view(tree):
        for item in tree.get_children():
            tree.delete(item)
        suppliers = Supplier.load_all()
        for supplier in suppliers:
            tree.insert('', 'end', values=(supplier.supplier_id, supplier.name, supplier.address, supplier.contact_details))

    @staticmethod
    def add_supplier(supplier_id_entry, name_entry, supplier_address_entry, supplier_contact_details_entry, supplier_tree):
        try:
            new_supplier = Supplier(
                supplier_id=int(supplier_id_entry.get()),
                name=name_entry.get(),
                address=supplier_address_entry.get(),
                contact_details=supplier_contact_details_entry.get()
            )
            new_supplier.save()
            messagebox.showinfo("Success", "Supplier added successfully")
            DataManagement.clear_entries([supplier_id_entry, name_entry, supplier_address_entry, supplier_contact_details_entry])
            SupplierForm.refresh_supplier_view(supplier_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def delete_supplier(supplier_tree):
        selected_item = supplier_tree.selection()[0]
        selected_supplier_id = supplier_tree.item(selected_item)['values'][0]
        try:
            Supplier.delete(selected_supplier_id)
            messagebox.showinfo("Success", "Supplier deleted successfully")
            SupplierForm.refresh_supplier_view(supplier_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))


#
# Guest UI Class
#

class GuestForm:
    @staticmethod
    def refresh_guest_view(tree):
        for item in tree.get_children():
            tree.delete(item)
        guests = Guest.load_all()
        for guest in guests:
            tree.insert('', 'end', values=(guest.guest_id, guest.name, guest.address, guest.contact_details))

    @staticmethod
    def add_guest(guest_id_entry, name_entry, guest_address_entry, guest_contact_details_entry, guest_tree):
        try:
            new_guest = Guest(
                guest_id=int(guest_id_entry.get()),
                name=name_entry.get(),
                address=guest_address_entry.get(),
                contact_details=guest_contact_details_entry.get()
            )
            new_guest.save()
            messagebox.showinfo("Success", "Guest added successfully")
            DataManagement.clear_entries([guest_id_entry, name_entry, guest_address_entry, guest_contact_details_entry])
            GuestForm.refresh_guest_view(guest_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def delete_guest(guest_tree):
        selected_item = guest_tree.selection()[0]
        selected_guest_id = guest_tree.item(selected_item)['values'][0]
        try:
            Guest.delete(selected_guest_id)
            messagebox.showinfo("Success", "Guest deleted successfully")
            GuestForm.refresh_guest_view(guest_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))
#
# Venue UI Class
#

class VenueForm:
    @staticmethod
    def refresh_venue_view(tree):
        for item in tree.get_children():
            tree.delete(item)
        venues = Venue.load_all()
        for venue in venues:
            tree.insert('', 'end', values=(venue.venue_id, venue.name, venue.address, venue.contact_details, venue.min_guests, venue.max_guests))

    @staticmethod
    def add_venue(venue_id_entry, name_entry, venue_address_entry, venue_contact_details_entry, venue_min_guests_entry, venue_max_guests_entry, venue_tree):
        try:
            new_venue = Venue(
                venue_id=int(venue_id_entry.get()),
                name=name_entry.get(),
                address=venue_address_entry.get(),
                contact_details=venue_contact_details_entry.get(),
                min_guests=int(venue_min_guests_entry.get()),
                max_guests=int(venue_max_guests_entry.get())
            )
            new_venue.save()
            messagebox.showinfo("Success", "Venue added successfully")
            DataManagement.clear_entries([venue_id_entry, name_entry, venue_address_entry, venue_contact_details_entry, venue_min_guests_entry, venue_max_guests_entry])
            VenueForm.refresh_venue_view(venue_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def delete_venue(venue_tree):
        selected_item = venue_tree.selection()[0]
        selected_venue_id = venue_tree.item(selected_item)['values'][0]
        try:
            Venue.delete(selected_venue_id)
            messagebox.showinfo("Success", "Venue deleted successfully")
            VenueForm.refresh_venue_view(venue_tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))


class MainApp:
    @staticmethod
    def add_employee(name_entry, id_entry, department_entry, title_entry, salary_entry, manager_id_entry, tree):
        try:
            new_employee = Employee(
                name_entry.get(), int(id_entry.get()), department_entry.get(),
                title_entry.get(), float(salary_entry.get()), None, None, None,
                int(manager_id_entry.get()) if manager_id_entry.get() else None
            )
            Employee.save(new_employee)
            messagebox.showinfo("Success", "Employee added successfully")
            EmployeeForm.refresh_employee_view(tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def update_employee(name_entry, department_entry, title_entry, salary_entry, manager_id_entry, tree):
        selected_item = tree.selection()[0]
        selected_employee_id = tree.item(selected_item)['values'][0]
        try:
            updates = {
                'name': name_entry.get(),
                'department': department_entry.get(),
                'job_title': title_entry.get(),
                'basic_salary': float(salary_entry.get()),
                'manager_id': int(manager_id_entry.get()) if manager_id_entry.get() else None
            }
            Employee.update(selected_employee_id, updates)
            messagebox.showinfo("Success", "Employee updated successfully")
            EmployeeForm.refresh_employee_view(tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def delete_employee(tree):
        selected_item = tree.selection()[0]
        selected_employee_id = tree.item(selected_item)['values'][0]
        try:
            Employee.delete(selected_employee_id)
            messagebox.showinfo("Success", "Employee deleted successfully")
            EmployeeForm.refresh_employee_view(tree)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def refresh_employee_view(tree):
        for item in tree.get_children():
            tree.delete(item)
        employees = Employee.load_all()
        for employee in employees:
            tree.insert('', 'end', values=(
            employee.employee_id, employee.name, employee.department, employee.job_title, employee.basic_salary))

    # Entries
    name_entry = id_entry = department_entry = title_entry = salary_entry = manager_id_entry = None
    event_id_entry = event_type_entry = theme_entry = date_entry = time_entry = duration_entry = venue_entry = client_entry = suppliers_entry = None
    client_id_entry = client_name_entry = client_address_entry = client_contact_details_entry = client_budget_entry = None
    supplier_id_entry = supplier_name_entry = supplier_address_entry = supplier_contact_details_entry = None
    guest_id_entry = guest_name_entry = guest_address_entry = guest_contact_details_entry = None
    venue_id_entry = venue_name_entry = venue_address_entry = venue_contact_details_entry = venue_min_guests_entry = venue_max_guests_entry = None

    def __init__(self, root):
        self.root = root
        self.root.title("Management System")

        self.setup_styles()
        self.create_main_menu()

    def create_main_menu(self):
        # List of categories and their associated functions
        categories = {
            "Employees": self.create_employee_tab,
            "Clients": self.create_client_tab,
            "Venues": self.create_venue_tab,
            "Guests": self.create_guest_tab,
            "Suppliers": self.create_supplier_tab,
            "Events": self.create_event_tab
        }

        # Create a button for each category
        for name, func in categories.items():
            btn = ttk.Button(self.root, text=name, command=func)
            btn.pack(pady=10, fill='x', padx=20)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#f0f0f0", foreground="black",
                        rowheight=25, fieldbackground="#e3e3e3")
        style.map('Treeview', background=[('selected', '#034f84')])
        style.configure("TButton", font=('Helvetica', 11), padding=6, background="#4287f5")
        style.configure("TEntry", padding=5, background="#ffffff", font=('Helvetica', 10))

    def create_employee_tab(self):
        def show_employees():
            # Create a new top-level window for showing employee information
            employees_window = tk.Toplevel()
            employees_window.title("Employee List")

            # List frame for displaying employee list in the new window
            list_frame = tk.Frame(employees_window)
            list_frame.pack(padx=10, pady=10)

            # Treeview for displaying employee details
            tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Department", "Title", "Salary"), show="headings")
            for col in ("ID", "Name", "Department", "Title", "Salary"):
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate the treeview with employee data
            EmployeeForm.refresh_employee_view(tree)
            # Button to delete selected employee
            delete_button = tk.Button(employees_window, text="Delete Employee",
                                      command=lambda: MainApp.delete_employee(tree))
            delete_button.pack()

            # Creating a new top-level window for employee management

        new_window = tk.Toplevel()
        new_window.title("Employee Management")

        # Input frame for employee details in the new window
        input_frame = tk.Frame(new_window)
        input_frame.pack(padx=10, pady=10)

        # Input fields and labels for employee details
        labels = ["Name", "ID Number", "Department", "Job Title", "Basic Salary", "Manager ID"]
        self.entries = []
        for idx, label in enumerate(labels):
            tk.Label(input_frame, text=label).grid(row=idx, column=0)
            entry = tk.Entry(input_frame)
            entry.grid(row=idx, column=1)
            self.entries.append(entry)

        # Assigning the entries to attributes for easier access
        self.name_entry, self.id_entry, self.department_entry, self.title_entry, self.salary_entry, self.manager_id_entry = self.entries

        # Button to show employees
        show_button = tk.Button(input_frame, text="Show Employees", command=show_employees)
        show_button.grid(row=len(labels), columnspan=2)

        # Buttons for employee management operations
        add_button = tk.Button(input_frame, text="Add Employee", command=lambda: EmployeeForm.add_employee(
            self.name_entry, self.id_entry, self.department_entry, self.title_entry, self.salary_entry,
            self.manager_id_entry, tree))
        add_button.grid(row=len(labels) + 1, columnspan=2)

        # Placeholder methods for initializing and refreshing employee data
        self.initialize_employee_data()
        # EmployeeForm.refresh_employee_view()

    def create_event_tab(self):
        def show_events():
            # Create a new top-level window for showing event information
            events_window = tk.Toplevel()
            events_window.title("Event List")

            # List frame for displaying event list in the new window
            list_frame = tk.Frame(events_window)
            list_frame.pack(padx=10, pady=10)

            # Treeview for displaying event details
            tree = ttk.Treeview(list_frame, columns=("ID", "Type", "Theme", "Date", "Time"), show="headings")
            for col in ("ID", "Type", "Theme", "Date", "Time"):
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate the treeview with event data
            EventForm.refresh_event_view(tree)

            # Button to delete selected client
            delete_button = tk.Button(events_window, text="Delete Event", command=lambda: EventForm.delete_event(tree))
            delete_button.pack(pady=10)  # Ensure there's some padding for aesthetic spacing

        # Creating a new top-level window for event management
        event_window = tk.Toplevel()
        event_window.title("Event Management")

        # Input frame for event details in the new window
        event_input_frame = tk.Frame(event_window)
        event_input_frame.grid(row=0, column=0, padx=10, pady=10)

        # Input fields and labels for event details
        event_labels = ["Event ID", "Event Type", "Theme", "Date", "Time", "Duration", "Venue", "Client", "Suppliers"]
        event_entries = []
        for idx, label in enumerate(event_labels):
            tk.Label(event_input_frame, text=label).grid(row=idx, column=0)
            entry = tk.Entry(event_input_frame)
            entry.grid(row=idx, column=1)
            event_entries.append(entry)
        # Buttons for event management operations
        tk.Button(event_input_frame, text="Add Event",
                  command=EventForm.add_event(self.event_id_entry, self.event_type_entry, self.theme_entry,
                                              self.date_entry, self.time_entry, self.duration_entry, self.venue_entry,
                                              self.client_entry, self.suppliers_entry)).grid(row=9, columnspan=2)
        tk.Button(event_input_frame, text="Show Events", command=show_events).grid(row=11, columnspan=2)

        # Unpack entries for easy access
        self.event_id_entry, self.event_type_entry, self.theme_entry, self.date_entry, self.time_entry, self.duration_entry, self.venue_entry, self.client_entry, self.suppliers_entry = event_entries

        # Placeholder methods for initializing and refreshing event data
        self.initialize_event_data()
        EventForm.refresh_event_view(tree)

    def create_client_tab(self):
        def show_clients():
            # Create a new top-level window for showing client information
            clients_window = tk.Toplevel()
            clients_window.title("Client List")

            # List frame for displaying client list in the new window
            list_frame = tk.Frame(clients_window)
            list_frame.pack(padx=10, pady=10)

            # Treeview for displaying client details
            tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Address", "Contact Details", "Budget"),
                                show="headings")
            for col in ["ID", "Name", "Address", "Contact Details", "Budget"]:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate the treeview with client data
            ClientForm.refresh_client_view(tree)
            # Button to delete selected client
            delete_button = tk.Button(clients_window, text="Delete Client",
                                      command=lambda: ClientForm.delete_client(tree))
            delete_button.pack(pady=10)  # Ensure there's some padding for aesthetic spacing

        # Creating a new top-level window for client management
        client_window = tk.Toplevel()
        client_window.title("Client Management")

        # Input frame for client details in the new window
        client_input_frame = tk.Frame(client_window)
        client_input_frame.grid(row=0, column=0, padx=10, pady=10)

        # Input fields and labels for clients
        client_labels = ["Client ID", "Name", "Address", "Contact Details", "Budget"]
        client_entries = []
        for idx, label in enumerate(client_labels):
            tk.Label(client_input_frame, text=label).grid(row=idx, column=0)
            entry = tk.Entry(client_input_frame)
            entry.grid(row=idx, column=1)
            client_entries.append(entry)

        # Unpack entries for easy access
        client_id_entry, client_name_entry, client_address_entry, client_contact_details_entry, client_budget_entry = client_entries

        # Buttons for client management operations
        tk.Button(client_input_frame, text="Add Client",
                  command=lambda: ClientForm.add_client(client_window, client_id_entry, client_name_entry,
                                                        client_address_entry, client_contact_details_entry,
                                                        client_budget_entry)).grid(row=5, columnspan=2)
        tk.Button(client_input_frame, text="Show Clients", command=show_clients).grid(row=7, columnspan=2)

        # Placeholder methods for initializing and refreshing client data
        self.initialize_client_data()

    # ClientForm.refresh_client_view()

    def create_supplier_tab(self):
        def show_suppliers():
            # Create a new top-level window for showing supplier information
            suppliers_window = tk.Toplevel()
            suppliers_window.title("Supplier List")

            # List frame for displaying supplier list in the new window
            list_frame = tk.Frame(suppliers_window)
            list_frame.pack(padx=10, pady=10)

            # Treeview for displaying supplier details
            tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Address", "Contact Details"), show="headings")
            for col in ["ID", "Name", "Address", "Contact Details"]:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate the treeview with supplier data
            SupplierForm.refresh_supplier_view(tree)

            # Button to delete selected supplier
            delete_button = tk.Button(suppliers_window, text="Delete Supplier",
                                      command=lambda: SupplierForm.delete_supplier(tree))
            delete_button.pack()

        # Creating a new top-level window for supplier management
        supplier_window = tk.Toplevel()
        supplier_window.title("Supplier Management")

        # Input frame for supplier details in the new window
        supplier_input_frame = tk.Frame(supplier_window)
        supplier_input_frame.grid(row=0, column=0, padx=10, pady=10)

        # Input fields and labels for suppliers
        supplier_labels = ["Supplier ID", "Name", "Address", "Contact Details"]
        supplier_entries = []
        for idx, label in enumerate(supplier_labels):
            tk.Label(supplier_input_frame, text=label).grid(row=idx, column=0)
            entry = tk.Entry(supplier_input_frame)
            entry.grid(row=idx, column=1)
            supplier_entries.append(entry)

        # Unpack entries for easy access
        supplier_id_entry, name_entry, supplier_address_entry, supplier_contact_details_entry = supplier_entries

        # Buttons for supplier management operations
        tk.Button(supplier_input_frame, text="Add Supplier",
                  command=lambda: SupplierForm.add_supplier(supplier_id_entry, name_entry, supplier_address_entry,
                                                            supplier_contact_details_entry, tree)).grid(row=4,
                                                                                                        columnspan=2)
        tk.Button(supplier_input_frame, text="Show Suppliers", command=show_suppliers).grid(row=5, columnspan=2)

        # Placeholder methods for initializing and refreshing supplier data
        self.initialize_supplier_data()

    # SupplierForm.refresh_supplier_view(tree)

    def create_guest_tab(self):
        def show_guests():
            # Create a new top-level window for showing guest information
            guests_window = tk.Toplevel()
            guests_window.title("Guest List")

            # List frame for displaying guest list in the new window
            list_frame = tk.Frame(guests_window)
            list_frame.pack(padx=10, pady=10)

            # Treeview for displaying guest details
            tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Address", "Contact Details"), show="headings")
            for col in ["ID", "Name", "Address", "Contact Details"]:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate the treeview with guest data
            GuestForm.refresh_guest_view(tree)

            # Button to delete selected guest
            delete_button = tk.Button(guests_window, text="Delete Guest", command=lambda: GuestForm.delete_guest(tree))
            delete_button.pack()

        # Creating a new top-level window for guest management
        guest_window = tk.Toplevel()
        guest_window.title("Guest Management")

        # Input frame for guest details in the new window
        guest_input_frame = tk.Frame(guest_window)
        guest_input_frame.grid(row=0, column=0, padx=10, pady=10)

        # Input fields and labels for guests
        guest_labels = ["Guest ID", "Name", "Address", "Contact Details"]
        guest_entries = []
        for idx, label in enumerate(guest_labels):
            tk.Label(guest_input_frame, text=label).grid(row=idx, column=0)
            entry = tk.Entry(guest_input_frame)
            entry.grid(row=idx, column=1)
            guest_entries.append(entry)

        # Unpack entries for easy access
        guest_id_entry, name_entry, guest_address_entry, guest_contact_details_entry = guest_entries

        # Buttons for guest management operations
        tk.Button(guest_input_frame, text="Add Guest",
                  command=lambda: GuestForm.add_guest(guest_id_entry, name_entry, guest_address_entry,
                                                      guest_contact_details_entry, tree)).grid(row=4, columnspan=2)
        tk.Button(guest_input_frame, text="Show Guests", command=show_guests).grid(row=5, columnspan=2)

        # List frame for displaying guest list in the new window
        guest_list_frame = tk.Frame(guest_window)
        guest_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Placeholder for methods to initialize and refresh the guest data
        self.initialize_guest_data()

    #  GuestForm.refresh_guest_view(tree)

    def create_venue_tab(self):
        def show_venues():
            # Create a new top-level window for showing venue information
            venues_window = tk.Toplevel()
            venues_window.title("Venue List")

            # List frame for displaying venue list in the new window
            list_frame = tk.Frame(venues_window)
            list_frame.pack(padx=10, pady=10)

            # Treeview for displaying venue details
            tree = ttk.Treeview(list_frame,
                                columns=("ID", "Name", "Address", "Contact Details", "Min Guests", "Max Guests"),
                                show="headings")
            for col in ["ID", "Name", "Address", "Contact Details", "Min Guests", "Max Guests"]:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.W)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate the treeview with venue data
            VenueForm.refresh_venue_view(tree)

            # Button to delete selected venue
            delete_button = tk.Button(venues_window, text="Delete Venue", command=lambda: VenueForm.delete_venue(tree))
            delete_button.pack()

        # Creating a new top-level window for venue management
        venue_window = tk.Toplevel()
        venue_window.title("Venue Management")

        # Input frame for venue details in the new window
        venue_input_frame = tk.Frame(venue_window)
        venue_input_frame.grid(row=0, column=0, padx=10, pady=10)

        # Input fields and labels for venues
        venue_labels = ["Venue ID", "Name", "Address", "Contact Details", "Min Guests", "Max Guests"]
        venue_entries = []
        for idx, label in enumerate(venue_labels):
            tk.Label(venue_input_frame, text=label).grid(row=idx, column=0)
            entry = tk.Entry(venue_input_frame)
            entry.grid(row=idx, column=1)
            venue_entries.append(entry)

        # Unpack entries for easy access
        venue_id_entry, name_entry, venue_address_entry, venue_contact_details_entry, venue_min_guests_entry, venue_max_guests_entry = venue_entries

        # Buttons for venue management operations
        tk.Button(venue_input_frame, text="Add Venue",
                  command=lambda: VenueForm.add_venue(venue_id_entry, name_entry, venue_address_entry,
                                                      venue_contact_details_entry, venue_min_guests_entry,
                                                      venue_max_guests_entry, tree)).grid(row=6, columnspan=2)
        tk.Button(venue_input_frame, text="Show Venues", command=show_venues).grid(row=7, columnspan=2)

        # List frame for displaying venue list in the new window
        venue_list_frame = tk.Frame(venue_window)
        venue_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Placeholder for methods to initialize and refresh the venue data
        self.initialize_venue_data()

    #    VenueForm.refresh_venue_view(tree)

    # SAMPLE DATA INITIALIZATION

    def initialize_employee_data(self):
        filename = "employees.pkl"
        if not DataManagement.load_data(filename):
            # Pre-populate some employee data if the file doesn't exist
            employees = [
                Employee("Susan Meyers", 47899, "Sales", "Manager", 37500, None, None, None, None),
                Employee("Joy Rogers", 81774, "Sales", "Manager", 24000, None, None, None, None),
                Employee("Shyam Sundar", 11234, "Sales", "Salesperson", 20000, None, None, None, 47899),
                Employee("Mariam Khalid", 98394, "Sales", "Salesperson", 20000, None, None, None, 81774),
                Employee("Salma J Sam", 98637, "Sales", "Salesperson", 20000, None, None, None, 47899)
            ]
            for employee in employees:
                Employee.save(employee)

    def initialize_venue_data(self):
        filename = Venue.FILENAME
        venues = Venue.load_all()
        if not venues:
            venues = [
                Venue(1, "Mount View", "102 Venue Blvd", "101-232-3893", 10, 100),
                Venue(2, "Old School", "201 Venue St", "424-515-3636", 20, 200)
            ]
            for venue in venues:
                venue.save()
        return venues

    def initialize_guest_data(self):
        filename = Guest.FILENAME
        guests = Guest.load_all()
        if not guests:
            guests = [
                Guest(1, "Laura", "789 Guest Lane", "234-567-8901"),
                Guest(2, "Anabelle", "321 Main Road", "890-123-4567")
            ]
            for guest in guests:
                guest.save()
        return guests

    def initialize_supplier_data(self):
        filename = Supplier.FILENAME
        suppliers = Supplier.load_all()
        if not suppliers:
            suppliers = [
                Supplier(1, "WholeTraders", "13 Supplier St", "133-436-7390"),
                Supplier(2, "Whole Market", "456 Supplier Ave", "987-654-3210")
            ]
            for supplier in suppliers:
                supplier.save()
        return suppliers

    def initialize_client_data(self):
        filename = Client.FILENAME
        try:
            with open(filename, 'rb') as file:
                clients = pickle.load(file)
        except FileNotFoundError:
            # Create sample data if file doesn't exist
            clients = [
                Client(1, "Alice Johnson", "123 Elm St", "555-1234", 5000),
                Client(2, "Bob Smith", "456 Oak St", "555-5678", 3000)
            ]
            with open(filename, 'wb') as file:
                pickle.dump(clients, file)
        return clients

    def initialize_event_data(self):
        filename = "events.pkl"
        try:
            with open(filename, 'rb') as file:
                events = pickle.load(file)
        except FileNotFoundError:
            # Create sample data if file doesn't exist
            events = [
                Event(1, "Conference", "Tech", "2023-10-05", "09:00", 3, "Convention Center", "Tech Corp",
                      ["Catering Co", "AV Setup"]),
                Event(2, "Wedding", "Outdoor", "2023-12-15", "15:00", 5, "Beach Resort", "John Doe",
                      ["Florist", "Music Band"])
            ]
            with open(filename, 'wb') as file:
                pickle.dump(events, file)
        return events


if __name__ == "__main__":
    app = MainApp(root)
    root.mainloop()



