from tkinter import *
from tkinter import messagebox
from password_generator import *
import pyperclip
import json
from bg_cipher import *
import os

BACKGROUND = "#f7f5dd"
FILL_COLOUR = "black"

# BACKGROUND = "black"
# FILL_COLOUR = "white"
FONT = ("Courier", 34, "bold")



def app():
    def search_password():
        """Method to Retrieve Email and Password from json file and display to the user"""
        website = website_entry.get().title()

        # Check if user entered a website in website field
        if len(website) == 0:
            messagebox.showinfo(title="Field Empty", message="Please Enter Website Field.")
        # If website entered, load json file
        else:
            # If the json file is empty, delete file to avoid JSONDecodeError
            try:
                if os.stat("data.json").st_size == 0:
                    os.remove("data.json")
            except FileNotFoundError:
                pass
            try:
                with open("data.json", mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No Data File Found.")
            else:
                # if website exists in json file, display to the user, if not display message
                if website in data:
                    website_data = data[website]
                    website_password = decode(website_data["password"])
                    website_email = decode(website_data['email'])
                    pyperclip.copy(website_password)
                    messagebox.showinfo(title=website,
                                        message=f"Email: {website_email}\nPassword: {website_password}")
                else:
                    messagebox.showinfo(title="Oops", message=f"No Details for {website} Found.")

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def generate_password():
        """Displays randomly generated password in password field"""
        password_entry.delete(0, END)
        generated_password = password_generator()
        pyperclip.copy(generated_password)
        password_entry.insert(0, generated_password)

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def save():
        """Stores User Details in Json file"""
        website = website_entry.get().title()
        email = email_entry.get()
        password = password_entry.get()
        encrypted_email = encode(email)
        encrypted_password = encode(password)
        # Defined format for storing data
        new_data = {
            website: {
                "email": encrypted_email,
                "password": encrypted_password,
            }
        }
        # Firstly check if Details have been entered
        if len(website) == 0 or len(password) == 0 or len(email) == 0:
            messagebox.showinfo(title="Oops", message="Please enter all fields.")
        else:
            # Verify details with user before proceeding
            is_ok = messagebox.askokcancel(title=website,
                                           message=f"These are the details entered: \nEmail: {email} \nPassword: {password}"
                                                   f"\nSave Details?")
            # If Details okay with user proceed to saving
            if is_ok:
                # If the json file is empty, delete file to avoid JSONDecodeError
                try:
                    if os.stat("data.json").st_size == 0:
                        os.remove("data.json")
                except FileNotFoundError:
                    pass
                try:
                    # load file to save details
                    with open("data.json", mode="r") as file:
                        data = json.load(file)
                        data.update(new_data)
                    # if file does not exist, create file and then save details
                except FileNotFoundError:
                    with open("data.json", mode="w") as file:
                        json.dump(new_data, file, indent=4)
                    # if file exists, then save details
                else:
                    with open("data.json", mode="w") as file:
                        json.dump(data, file, indent=4)
                    messagebox.showinfo(title=f"{website}", message="Details Saved Successfully")

                    # clear fields
                finally:
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
                    website_entry.focus()

    # -----------------------------------UI SETUP--------------------------------------#
    window = Tk()
    window.title("Password Manager")
    window.config(bg=BACKGROUND)
    window.config(padx=50, pady=50)

    canvas = Canvas(width=200, height=180, bg=BACKGROUND, highlightthickness=0)
    logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(row=0, column=1, columnspan=18)

    # Labels
    website_label = Label(text="Website:", bg=BACKGROUND, fg=FILL_COLOUR)
    website_label.grid(row=1, column=1)

    email_label = Label(text="Email/Username:", bg=BACKGROUND, fg=FILL_COLOUR)
    email_label.grid(row=2, column=1)

    password_label = Label(text="Password:", bg=BACKGROUND, fg=FILL_COLOUR)
    password_label.grid(row=3, column=1)

    # Entries
    website_entry = Entry(width=18)
    website_entry.grid(row=1, column=2, sticky="w")
    website_entry.focus()

    search_button = Button(text="Search", command=search_password)
    search_button.config(width=14, borderwidth=0, bg=BACKGROUND, fg=FILL_COLOUR)
    search_button.grid(row=1, column=2, sticky="e", columnspan=2)

    email_entry = Entry(width=35)
    email_entry.grid(row=2, column=2, columnspan=2)
    email_entry.insert(index=0, string="JohnDoe@email.com")

    password_entry = Entry(width=18)
    password_entry.grid(row=3, column=2, sticky="w")

    # Button
    generate_pass_button = Button(text="Generate Password", command=generate_password)
    generate_pass_button.config(width=14, bg=BACKGROUND, borderwidth=0, fg=FILL_COLOUR)
    generate_pass_button.grid(row=3, column=2, sticky="e", columnspan=2)

    add_button = Button(text="Add", width=30, command=save, borderwidth=0)
    add_button.grid(row=5, column=2, columnspan=2)


    window.mainloop()


# ------------------------------Verification Function-----------------------------------#
def verify_login_pin():
    # get entered pin
    pin = win_ver_entry.get()
    pin_data = {"pin": pin}

    # load json file to verify pin
    try:
        with open("pin.json", mode="r") as file:
            saved_pin = json.load(file)
    # if first json file does not exist
    except FileNotFoundError:
        # try open backup file
        try:
            with open("../backup_pin.json", mode="r") as backup_file:
                backup_saved_pin = json.load(backup_file)
        # if backup json file does not exist, user hasn't set pin yet
        # create first json file and backup file
        except FileNotFoundError:
            messagebox.showinfo(title="Verification", message="Set Pin First")
            win_ver_entry.delete(0, END)
            go_on = messagebox.askokcancel(title="Verification", message=f"Set {pin} As Pin?")
            # verify pin with user before saving to json files
            if go_on:
                if len(pin) != 4:
                    messagebox.showinfo(title="Oops", message="Pin Must Be 4 Digits")
                else:
                    if not pin.isdigit():
                        messagebox.showinfo(title="Oops", message="Pin Must Be Digits")
                    else:
                        with open("../backup_pin.json", mode="w") as backup_file:
                            json.dump(pin_data, backup_file, indent=4)
                            messagebox.showinfo(title="Verification", message="Pin Set Successful")
                        with open("pin.json", mode="w") as file:
                            json.dump(pin_data, file, indent=4)
            else:
                pass
        else:
            # backup json file exists, use data to perform verification and create first json file
            if pin == backup_saved_pin["pin"]:
                with open("pin.json", mode="w") as file:
                    json.dump(backup_saved_pin, file, indent=4)
                win_verification.destroy()
                app()
            else:
                # display if pin not valid
                messagebox.showinfo(title="Oops", message="Incorrect Pin")
                win_ver_entry.delete(0, END)
    else:
        # main json file exists, use data to perform verification and create backup json file
        if pin == saved_pin["pin"]:
            with open("../backup_pin.json", mode="w") as backup_file:
                json.dump(pin_data, backup_file, indent=4)
            win_verification.destroy()
            app()
        else:
            # display if pin not valid
            messagebox.showinfo(title="Oops", message="Incorrect Pin")
            win_ver_entry.delete(0, END)


# -------------------------Verification Screen--------------------------#
win_verification = Tk()
win_verification.resizable(False, False)
win_verification.title("Password Manager Login")
win_verification.config(bg="Black", padx=100, pady=100)

win_ver_label = Label(win_verification, text="Enter Pin:", fg="White", bg="black")
win_ver_label.grid(row=0, column=0, sticky="e")
win_ver_entry = Entry(win_verification, width=10)
win_ver_entry.grid(row=0, column=2, sticky="w")
win_ver_button = Button(win_verification, text="Proceed", bg="black", fg="white", width=10, borderwidth=0)
win_ver_button.config(command=verify_login_pin)
win_ver_button.grid(row=1, column=0, columnspan=3, pady=10)

win_verification.mainloop()
