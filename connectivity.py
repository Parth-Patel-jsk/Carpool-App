import mysql.connector
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
import re
import smtplib
import random
import string
otp=None
def connect_to_database():

    connection = mysql.connector.connect(
        host='localhost',
        database='carpool_db',
        user='root',
        password='krrish1234'
        )
    return connection
def is_valid_email(email):
    # Regular expression to validate email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None
def signup_check(self,new_username,new_licence,new_email,new_password):
    global otp
    if not is_valid_email(new_email):
        self.show_error_email_format("Invalid email format.")
        return
    #  if new_username:
    if new_email:
        if email_registered(new_email):
                print("Already registered")
                self.show_already_registered_dialog()
        else:
                if new_password and new_email and new_username and new_licence:
                     
                    print("Not registered")
                    # self.root.current="login"
                    insert_user(new_username,new_licence,new_email, new_password)
                    self.receiver_email=new_email
                    otp= self.generate_otp()  # Generate an OTP
                    receiver_email = new_email
                    send_otp_via_email(self.receiver_email, otp)
                    self.handle_successful_signup()
    else:
        print("Please enter email")
def check_login(self,email,password):
    if not is_valid_email(email):
        self.show_error_email_format("Invalid email format.")
        return

    if email and password:
        if email_registered(email):
            if check_password(self,email, password):
                l(self,email,password)
                self.root.current = "home"
                print("Correct")
            else:
                print("Error", "Invalid password.")
                self.show_wrong_password("password inserted is wrong")
        else:
            print("Error", "Email not registered.")
            self.show_wrong_password_email("Email and password are not registered")
    else:
            print("Error", "Please enter both email and password.")

def email_registered(new_email):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE email = %s"
    cursor.execute(query, (new_email,))
    result = cursor.fetchone()
   
    cursor.close()
    connection.close()
    return result[0] > 0 if result else False
    
def insert_user(new_username,new_licence, new_email,new_password):
    connection = connect_to_database()
    cursor = connection.cursor()
    # Only include columns `username`, `email`, and `password`
    query = "INSERT INTO users (username,Dlicence, email, password) VALUES (%s,%s, %s, %s)"
    cursor.execute(query, (new_username,new_licence, new_email, new_password))
    connection.commit()
    print("User inserted successfully.")
    cursor.close()
    connection.close()
def check_password(self, email, password):
    # Connect to the MySQL database and validate the password
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT password FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    if result:
        stored_password = result[0]
        return stored_password == password  # You should hash and compare passwords in a real-world application
    return False

def show_already_registered_dialog(app):
    # Call the method from the app instance to show the dialog
    app.show_already_registered_dialog()

def l(self,email,password):
        # Email= email_customer.text  # Get the entered username
        # passwordw = password_customer.text
        # print(Email)
        # print(passwordw)
        
    
        db = mysql.connector.connect(
            host='localhost', user='root', password='krrish1234', database='carpool_db'
        )
        cursor = db.cursor()
        cursor.execute("SELECT user FROM users WHERE email=%s AND password=%s", (email, password))
        result = cursor.fetchone()
        User=str(result[0])
        print(result)
        
        # self.screen_manager.get_screen("accountf").ids.welcome_label_farmer.text=User
        # Pass username to account screen
    
def generate_otp(self,length=4):
    # Generate a random OTP of the given length
    digits = string.digits
    otp = ''.join(random.choice(digits) for i in range(length))
    print(otp)
    
    return otp
    

def send_otp_via_email(receiver_email, otp):
    # Your email credentials
    sender_email = "farmazon.in@gmail.com"
    app_password = "xtps kifr lbtr oaum"  # Replace with the App Password
    # Setting up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Craft the message
    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}. It is valid for 10 minutes."
    message = f"Subject: {subject}\n\n{body}"

    # Send the email
    server.sendmail(sender_email,receiver_email, message)
    print('OTP Sent')

    # Close the SMTP server connection
    server.quit()
def otp(self,otp_id,):
    global otp
    value=otp_id
    print(value)
    # print(krrish)
    if otp==value:
         self.show_welcome_email(self.receiver_email)
         self.root.current="login"
         
    else:
         self.show_wrong_otp_farmer("Wrong otp inserted")  
def show_welcome_email(self,receiver_email):
    sender_email = "farmazon.in@gmail.com"
    app_password = "xtps kifr lbtr oaum"  # Replace with the App Password
    # Setting up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Craft the message
    subject = "Welcome to Farmazon! "
    body ="""
We're thrilled to have you join our community of passionate farmers and buyers
Get ready to explore and connect with a vibrant marketplace designed just for you.\nWhether you're here to sell your produce or discover fresh, local products, we're here to help you every step of the way.
Thank you for choosing Farmazon. We're excited to support your journey!
Best Regards
The Farmazon Team"""
    message = f"Subject: Dear {receiver_email}\n{subject}\n\n{body}"

    # Send the email
    server.sendmail(sender_email,receiver_email, message)
    server.quit()
     

