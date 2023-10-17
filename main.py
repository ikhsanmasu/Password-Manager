from random import choice, randint, shuffle
import pyperclip
import json
from tkinter import *
from tkinter import messagebox
import os
import sys

# use this directory when generating exe file
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

password_file_dir = application_path + "/password.json"
image_dir = application_path + "/logo.png"

# password_file_dir = "password.json"
# image_dir = "logo.png"

def search_password():
    try:
        with open(password_file_dir, mode="r") as file:
            website = website_entry.get()
            data = json.load(file)
            try:
                username = data[website]["username"]
                password = data[website]["password"]
                messagebox.showinfo(title="Here it is",
                                    message=f"your username is: {username} and the password is: {password}\n"
                                            f"password copied to clipboard")
                pyperclip.copy(password)
            except KeyError:
                messagebox.showinfo(title="Oops", message=f"No password create for this username")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message=f"No password create for this username")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_pass = [letters[randint(0, len(letters) - 1)] for _ in range(randint(1, 32))]
    numbers_pass = [numbers[randint(0, len(numbers) - 1)] for _ in range(randint(1, 32))]
    symbols_pass = [symbols[randint(0, len(symbols) - 1)] for _ in range(randint(1, 32))]
    password = letters_pass + numbers_pass + symbols_pass
    shuffle(password)
    password = "".join(password[0:randint(8, 32)])
    password_entry.insert(index=0, string=password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = email_entry.get()
    password = password_entry.get()
    new_password = {
        website: {
            "username": username,
            "password": password
        }
    }
    if len(website) == 0 or len(username) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title="password created", message=f"Are you ok with {password} password")
        if is_ok:
            try:
                with open(password_file_dir, mode="r") as password_file:
                    data = json.load(password_file)
            except FileNotFoundError:
                with open(password_file_dir, mode="w") as password_file:
                    json.dump(new_password, password_file, indent=4)
            else:
                data.update(new_password)
                with open(password_file_dir, "w") as password_file:
                    # Saving updated data
                    json.dump(data, password_file, indent=4)
            finally:
                messagebox.showinfo(title="Great", message="New Password Saved")
                website_entry.delete(0, END)
                password_entry.delete(0, END)



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

logo_img = PhotoImage(file=image_dir)
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entry
website_entry = Entry(width=30)
website_entry.grid(column=1, row=1)
email_entry = Entry(width=49)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(index=0, string="user@gmail.com")
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3)

# Button
search_password_button = Button(text="Search", command=search_password, width=15)
search_password_button.grid(column=2, row=1)
generate_password_button = Button(text="Generate Password", command=generate_password, width=15)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=42, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
