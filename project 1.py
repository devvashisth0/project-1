import os
import tkinter as tk
from tkinter import messagebox

# File handling functions
CONTACTS_FILE = 'contacts.txt'

def load_contacts():
    contacts = []
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            for line in file:
                name, phone = line.strip().split(',')
                contacts.append({'name': name, 'phone': phone})
    return contacts

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        for contact in contacts:
            file.write(f"{contact['name']},{contact['phone']}\n")

def add_contact(name, phone):
    contacts = load_contacts()
    contacts.append({'name': name, 'phone': phone})
    save_contacts(contacts)

def delete_contact(name):
    contacts = load_contacts()
    contacts = [contact for contact in contacts if contact['name'] != name]
    save_contacts(contacts)

def update_contact(old_name, new_name, new_phone):
    contacts = load_contacts()
    for contact in contacts:
        if contact['name'] == old_name:
            contact['name'] = new_name
            contact['phone'] = new_phone
            break
    save_contacts(contacts)

def get_contacts():
    return load_contacts()

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

# Tkinter GUI functions
def refresh_contacts_listbox():
    listbox_contacts.delete(0, tk.END)
    for contact in get_contacts():
        listbox_contacts.insert(tk.END, f"{contact['name']} - {contact['phone']}")

def on_add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    if name and phone:
        add_contact(name, phone)
        refresh_contacts_listbox()
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter both name and phone number")

def on_delete_contact():
    selected_contact = listbox_contacts.get(tk.ACTIVE)
    if selected_contact:
        name = selected_contact.split(' - ')[0]
        delete_contact(name)
        refresh_contacts_listbox()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete")

def on_update_contact():
    selected_contact = listbox_contacts.get(tk.ACTIVE)
    new_name = entry_name.get()
    new_phone = entry_phone.get()
    if selected_contact and new_name and new_phone:
        old_name = selected_contact.split(' - ')[0]
        update_contact(old_name, new_name, new_phone)
        refresh_contacts_listbox()
        clear_entries()
    else:
        messagebox.showwarning("Update Error", "Please select a contact and enter new details")

def on_reset():
    listbox_contacts.delete(0, tk.END)
    if os.path.exists(CONTACTS_FILE):
        os.remove(CONTACTS_FILE)

def on_clear_entries():
    clear_entries()

# GUI setup
root = tk.Tk()
root.title("Contact Book")

frame = tk.Frame(root)
frame.pack(pady=20)

# Name entry
label_name = tk.Label(frame, text="Name:")
label_name.grid(row=0, column=0, padx=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1, padx=5)

# Phone entry
label_phone = tk.Label(frame, text="Phone:")
label_phone.grid(row=1, column=0, padx=5)
entry_phone = tk.Entry(frame)
entry_phone.grid(row=1, column=1, padx=5)

# Buttons
button_add = tk.Button(frame, text="Add Contact", command=on_add_contact)
button_add.grid(row=2, column=0, pady=10)

button_update = tk.Button(frame, text="Update Contact", command=on_update_contact)
button_update.grid(row=2, column=1, pady=10)

button_delete = tk.Button(frame, text="Delete Contact", command=on_delete_contact)
button_delete.grid(row=3, column=0, pady=10)

button_reset = tk.Button(frame, text="Reset Contacts", command=on_reset)
button_reset.grid(row=3, column=1, pady=10)

button_clear = tk.Button(frame, text="Clear Entries", command=on_clear_entries)
button_clear.grid(row=4, columnspan=2, pady=10)

# Contacts listbox
listbox_contacts = tk.Listbox(root, width=40)
listbox_contacts.pack(pady=20)

# Load contacts on start
refresh_contacts_listbox()

root.mainloop()
