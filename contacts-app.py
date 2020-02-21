import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime, timedelta
import os
from PIL import Image, ImageTk
import re

contacts = [
  {"phoneNumber":"555 0001","name":"Sheldon Lee Cooper","dateOfBirth":"1980-02-26","email":"sheldon@gmail.com"},
  {"phoneNumber":"555 0002","name":"Howard Joel Wolowitz","dateOfBirth":"1981-03-01","email":"howard@gmail.com"},
  {"phoneNumber":"555 0003","name":"Rajesh Ramayan Koothrappali","dateOfBirth":"1981-10-06","email":"raj@gmail.com"},
  {"phoneNumber":"555 0004","name":"Penny Hofstadter","dateOfBirth":"1985-12-02","email":"penny@gmail.com"},
  {"phoneNumber":"555 0005","name":"Amy Farrah Fowler","dateOfBirth":"1979-12-17","email":"amy@gmail.com"},
  {"phoneNumber":"555 0002","name":"Bernadette Rostenkowski-Wolowitz","dateOfBirth":"1984-01-01","email":"bernadette@gmail.com"},
  {"phoneNumber":"555 0006","name":"Leonard Hofstadter","dateOfBirth":"1980-05-17","email":"leonard@gmail.com"}
]

class AppWindow():
    def __init__(self, parent):
        # Create the window
        self.parent = parent
        self.window = tk.Toplevel()
        self.window.geometry("670x400")
        self.window.title("Contacts app")
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
        # Create a text label and place it in the window
        self.title_label = tk.Label(self.window, text="Contacts app", font=("Arial", 16))
        self.title_label.place(x=10, y=10)
        # Create the list box
        self.contact_list = tk.Listbox(self.window, width=25, height=17)
        self.contact_list.place(x=10, y=40)
        # -- When an item in the list is selected, execute the list_clicked function
        self.contact_list.bind('<<ListboxSelect>>', self.list_clicked) 
        self.update_list()
        # Name
        self.name_label = tk.Label(self.window, text="Name", font=("Arial", 13))
        self.name_label.place(x=250,y=40)
        self.name_text = tk.Entry(self.window, width=25)
        self.name_text.place(x=250,y=60)
        # Email
        self.email_label = tk.Label(self.window, text="Email", font=("Arial", 13))
        self.email_label.place(x=250,y=100)
        self.email_text = tk.Entry(self.window, width=25)
        self.email_text.place(x=250,y=120)
        # Phone number
        self.validate_command1 = parent.register(self.name_validate)
        self.phone_label = tk.Label(self.window, text="Phone", font=("Arial", 13))
        self.phone_label.place(x=250,y=160)
        self.phone_text = tk.Entry(self.window, width=25, validate="all", validatecommand=(self.validate_command1, "%P"))
        self.phone_text.place(x=250,y=180)
        # Date of birth
        self.dob_label = tk.Label(self.window, text="Date of birth", font=("Arial", 13))
        self.dob_label.place(x=250,y=220)
        self.dob_text = tk.Entry(self.window, width=25)
        self.dob_text.place(x=250,y=240)
        # Age
        self.age_label = tk.Label(self.window, text="Age", font=("Arial", 13))
        self.age_label.place(x=250,y=280)
        self.age_info = tk.Label(self.window, text="", font=("Arial", 13))
        self.age_info.place(x=250,y=300)
        # Photo
        self.image_label = tk.Label(self.window)
        self.image_label.place(x=500,y=40,width=150,height=200)
        # Buttons
        self.new_button = tk.Button(self.window, text="Save new", command=self.save_new)
        self.new_button.place(x=250, y=340, width=100, height=40)
        self.existing_button = tk.Button(self.window, text="Save existing", command=self.save_existing)
        self.existing_button.place(x=370, y=340, width=100, height=40)


    def name_validate(self, text_to_check):
        print("Validating "+text_to_check)
        return re.match("^([A-Za-z]{2}[0-9]{5})$", text_to_check)
    
    def list_clicked(self, e):
        if len(self.contact_list.curselection()) == 0:
            return None
        print(f"list_clicked: {self.contact_list.curselection()}")
        self.selected = int(self.contact_list.curselection()[0])      # item number selected in list
        print(f"You clicked item number {self.selected}")
        # Get the selected contact
        contact = contacts[self.selected]
        # Show name
        self.name_text.delete(0, tk.END)
        self.name_text.insert(0, contact["name"])
        # Show email
        self.email_text.delete(0, tk.END)
        self.email_text.insert(0, contact["email"])
        # Show phone number
        self.phone_text.delete(0, tk.END)
        self.phone_text.insert(0, contact["phoneNumber"])
        # Show date of birth and age
        birthday = datetime.strptime(contact["dateOfBirth"], "%Y-%m-%d")
        self.dob_text.delete(0, tk.END)
        self.dob_text.insert(0, birthday.strftime("%d/%m/%Y"))
        today = datetime.now()
        age = today.year - birthday.year
        if today.month < birthday.month:
            age = age - 1
        elif today.month == birthday.month and today.day < birthday.day:
            age = age - 1
        self.age_info["text"] = str(age) + " years"
        # Show photo if it exists
        if os.path.exists(contact["name"]+".jpg"):
            img = Image.open(contact["name"]+".jpg")
            img = img.resize((150, 200))
            self.contact_photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.contact_photo)
        else:
            self.contact_photo = None
            self.image_label.configure(image=None)

    def update_list(self):
        # Empty list
        self.contact_list.delete(0, tk.END)
        # Add all contacts to list
        for contact in contacts:
            # Add each item to the end of the list
            self.contact_list.insert(tk.END, contact["name"])                     
        # Set a default to indicate no item selected
        self.selected = -1      

    def save_new(self):
        print("You clicked button save_new")
        new_contact = {}
        new_contact["name"] = self.name_text.get()
        new_contact["email"] = self.email_text.get()
        new_contact["phoneNumber"] = self.phone_text.get()
        new_contact["dateOfBirth"] = datetime.strptime(self.dob_text.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        contacts.append(new_contact)
        self.update_list()

    def save_existing(self):
        print("You clicked button save_existing")
        if self.selected >= 0:
            contacts[self.selected]["name"] = self.name_text.get()
            contacts[self.selected]["email"] = self.email_text.get()
            contacts[self.selected]["phoneNumber"] = self.phone_text.get()
            contacts[self.selected]["dateOfBirth"] = datetime.strptime(self.dob_text.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        self.update_list()
            
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = AppWindow(root)
    root.mainloop()
