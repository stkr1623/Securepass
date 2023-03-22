
from http.client import OK
from tkinter import *
from tkinter import messagebox
import random
import tkinter
from jinja2 import pass_eval_context
import pyperclip
from tkinter import simpledialog
import mysql.connector
import os
from encrypt import *
from decrypt import *
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

mydb = mysql.connector.connect(host = "localhost", 
                                user = "root", 
                                passwd = "Na@2254k",
                                database = "Password_Manager",
                                 autocommit=True)
                                  
mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE Password_Manager")

# mycursor.execute("CREATE TABLE passwords(id INT AUTO_INCREMENT PRIMARY KEY,website VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL)")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password():
    small = "abcdefghijklmnopqrstuwxyz"
    capital = small.upper()
    dig = "123456789"
    symbols = "!@#$%^&*(){:};"
    all = small +capital +dig + symbols
    length = 10
    generated_password = "".join(random.sample(all,length))
    password_entry.insert(0,generated_password)
    pyperclip.copy(generated_password)
    pyperclip.paste()
def get():
    # print(webite1_entry)
    w_e=webite1_entry.get()
    query = "SELECT password FROM passwords WHERE website = %s"
    mycursor.execute(query, (w_e,))
    result1 = mycursor.fetchone()
    print(result1)
    result2=str(result1[0])
    result=decrypt_aes(5,result2)
    pyperclip.copy(result)
    pyperclip.paste()
               
    result_entry.config(text=result)
    pass_clip_msg.config(text="Password saved to clipboard")
    if result==None:
            messagebox.showerror(title="Error",message="Website not found")
    # with open("data.txt") as new:
    #     file=new.readlines()
    #     found=0
    #     for i in file:
    #         web_ent=webite1_entry.get()
    #         if  web_ent.upper()==i[1:len(web_ent)+1].upper():
    #             a=len(webite1_entry.get())+len(email_entry.get())+7
    #             found=1
    #             pyperclip.copy(i[a:])
    #             pyperclip.paste()
               
    #             result_entry.config(text=f"{i[a:]}")
    #             pass_clip_msg.config(text="Password saved to clipboard")

        # if found==0:
        #     messagebox.showerror(title="Error",message="Website not found")
           # ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website1 = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website_entry.get())==0:
        messagebox.showerror(title="Error",message="Please enter website")
    elif len(email_entry.get())==0:
        messagebox.showerror(title="Error",message="Please enter email")
    elif len(password_entry.get())==0:
        messagebox.showerror(title="Error",message="Please enter password")
    else:
        is_ok = messagebox.askokcancel(title=website1, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            e_p=encrypt_aes(5,password)
            mycursor.execute("Insert INTO passwords (website, username,password) VALUES(%s,%s,%s)", (website1,email,e_p))
            # with open("data.txt", "a") as data_file:
            #     data_file.write(f" {website1} | {email} | {password}\n")
            #     website_entry.delete(0, END)
            #     password_entry.delete(0, END)


def get_pass():
    global user_password
    global website_entry,email_entry,password_entry,webite1_entry,result_entry,pass_clip_msg
    user_password = simpledialog.askstring("Password Entry", "Enter your passcode for password manager:\t\t\t\n\n")
    if user_password=="1234":
        window= Tk()
        window.title("Password Manager")
        window.config(padx=50,pady=50,bg="#EEEEEE")
        img=Canvas(width=200,height=200,bg="#EEEEEE", highlightthickness=0)
        lock_logo=PhotoImage(file="logo.png")
        img.create_image(100,100,image= lock_logo)
        img.grid(column=1,row=0)

        website_label=Label(text="Website :",font=("Courier",15,"bold"))
        website_label.grid(column=0,row=1)
        website_entry=Entry(width=35,fg="red", bg='White', font=("Arial",16,"bold"))
        website_entry.focus()
        website_entry.grid(column=1,row=1,columnspan = 2)


        email_label = Label(text="Email/UserName :",font=("Courier",15,"bold"))
        email_label.grid(column=0,row=2)
        email_entry=Entry(width=35,fg="#003638", bg='White', font=("Arial",16,"bold"))
        email_entry.insert(0,"tharun@gmail.com")
        email_entry.grid(column=1,row=2,columnspan = 2)


        password_label = Label(text="Password :",font=("Courier",18,"bold"))
        password_label.grid(column=0,row=3)
        password_entry=Entry(width=23,fg="red", bg='White', font=("Arial",16,"bold"))
        pyperclip.copy(password_entry.get())
        pyperclip.paste()
        password_entry.grid(column=1,row=3)
        # password_entry.focus

        #generate a password
        gen_pass_button = Button(text='Generate Password',font=("Arial",11,"italic"),command=password)
        gen_pass_button.grid(column=2,row=3)

        #add password
        add_button = Button(text='Add',font=("Arial",14,"italic"),width=36,command = save)
        add_button.grid(column=1,row=4,columnspan = 2)
        # know your password
        show_label = Label(text="Know your password ",font=("Courier",25,"bold"),pady = 20)
        show_label.grid(column=1,row=5,columnspan = 2)
        website1_label=Label(text="Website :",font=("Courier",15,"bold"))
        website1_label.grid(column=0,row=6)
        #websitename selected
        # mycursor.execute("SELECT website FROM passwords")
        # options = mycursor.fetchall()

        # var = StringVar(window)
        
        # # var.set(options[0][0])
        # dropdown = OptionMenu(window,var, *options)
        # webite1_entry= var.get()
        # print(var.get(),"gkjg")
        # dropdown.grid(column=1,row=6,columnspan = 2)
                
    
        webite1_entry=Entry(width=35,fg="red", bg='White', font=("Arial",16,"bold"))
        webite1_entry.grid(column=1,row=6,columnspan = 2)

        get_button = Button(text='Get Password',font=("Arial",14,"italic"),width=36,command = get )
        get_button.grid(column=1,row=7,columnspan = 2)

        password2_label=Label(text="Your Password:",font=("Courier",15,"bold"),pady=10)
        password2_label.grid(column=0,row=8)
        result_entry =Label(text=" ",font=("Arial",15,"italic"),height=2,background="black",foreground="yellow",width=36,relief = "groove")
        result_entry.grid(column=1,row=8,columnspan = 2)
        pass_clip_msg=Label(text=" ",font=("Arial",7,"italic"),height=1,foreground="red",width=36,relief = "groove")
        pass_clip_msg.grid(column=1,row=9,columnspan = 2)

        window.mainloop()
def populate_options():
    # Connect to the database
    conn = mysql.connector.connect(host="localhost", user="root", password="Na@2254k", database="Password_Manager",autocommit=True)
    cursor = conn.cursor()
    
    # Query the database for the website names
    query = "SELECT website FROM passwords"
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Add the website names to the dropdown menu
    
    
    # Close the database connection
    cursor.close()
    conn.close()
    return results
# ---------------------------- UI SETUP ------------------------------- #
# content=Tk()
# submitButton = Button(content, text="Start", command=get_pass)
# submitButton.config(height=6, width=25, fg='red') #looks a little nicer
# # submitButton.pack()
get_pass()
# # content.mainloop()



