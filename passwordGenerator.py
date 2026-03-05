import secrets
import string
from tkinter import *
from tkinter import ttk
from password_checker_connector import score_password, display_score

# Character sets
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
symbols = string.punctuation

#password set(default lowercase)
chars_select = lowercase

#Password Generator Function
def passwordGen():
    chars_select = ''

    #add selected sets to password set
    if lowercaseCheck.get() == 1:
        chars_select += lowercase
    if uppercaseCheck.get() == 1:
        chars_select += uppercase
    if digitCheck.get() == 1:
        chars_select += digits
    if symbolCheck.get() == 1:
        chars_select += symbols

    # Password length (RoboForm default-ish) to fix later
    length = 16

    # Generate secure password
    #Todo add check that it statisfies user inputs
    pw = ''.join(secrets.choice(chars_select) for _ in range(length))

    print("Generated Password:", pw)

    # Send password to checker
    raw_score, strength, suggestions = score_password(pw)

    score_for_ui = display_score(raw_score)

    print("Score:", score_for_ui)
    print("Strength:", strength)
    print("Suggestions:")
    print("".join(suggestions))

    password_displayed.set(pw)



#GUI window
root = Tk()
root.title("PasswordGenerator")
root.geometry("800x600")

#all GUI elements attach to this frame, rather than the window
mainframe = ttk.Frame(root, padding=(3, 3, 3, 3))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

#Title label
title_label = ttk.Label(mainframe, text="Random Password Generator")
title_label.grid(column=1, row=1, columnspan=4, sticky=(N))
title_label['padding'] = 10

#Password Label/Password display (add color to background)
password_displayed = StringVar()
password_label = ttk.Label(mainframe, textvariable=password_displayed)
password_label.grid(column=2, row=2, columnspan=2)

#Strength display (with color)

#Checkbox vars
lowercaseCheck = IntVar(value=1)
uppercaseCheck = IntVar(value=1)
digitCheck = IntVar(value=1)
symbolCheck = IntVar(value=1)

#Checkbutton wigits
lower_checkbox = ttk.Checkbutton(mainframe, text="lower", command=passwordGen, variable=lowercaseCheck, onvalue=1, offvalue=0)
lower_checkbox.grid(column=1, row=3)
upper_checkbox = ttk.Checkbutton(mainframe, text="upper", command=passwordGen, variable=uppercaseCheck, onvalue=1, offvalue=0)
upper_checkbox.grid(column=2, row=3)
digit_checkbox = ttk.Checkbutton(mainframe, text="digit", command=passwordGen, variable=digitCheck, onvalue=1, offvalue=0)
digit_checkbox.grid(column=3, row=3)
symbol_checkbox = ttk.Checkbutton(mainframe, text="symbol", command=passwordGen, variable=symbolCheck, onvalue=1, offvalue=0)
symbol_checkbox.grid(column=4, row=3)

#GUI configuration (for resizing window/padding)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)	
mainframe.columnconfigure(2, weight=1)
mainframe.columnconfigure(3, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()