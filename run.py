#Main Python file

# import the various libraries
import pyfiglet 
import gspread
from google.oauth2.service_account import Credentials
import os
from email_validator import validate_email, EmailNotValidError

# create the scope for the connected APIs
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    
    ]
# create constant vars for validation of connected APIs
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("coldroom_capacity_calculator")

email_address = SHEET.worksheet("email").get_all_values()


title = pyfiglet.figlet_format(" * * * *", font = "5lineoblique" ) 

print(f"{title}* Welcome to the Coldroom Calculator * \n")


def clear():
    """
    Function to clear the console
    """
    os.system("cls" if os.name == "nt" else "clear")
    

def check_email_registered():
    """
    Checks if user is registered
    """
    while True:
        # try statement to check if worksheet exists otherwise break and show error message
        # including support website link
        try:
            email_address = SHEET.worksheet("email")
            mail = email_address.col_values(1)
            
        except:
            print("Sorry an error has occurred.\n Please contact support.\n www.ccc@cold-calc.freeze")
            break
            
        # get user email and check if they are registered, quit or open the register module
        user_email = input("Please enter your registered email address, \n 'r' to register or 'q' to quit: \n")
        if user_email in mail:
            print("Loading your Projects......\n")
            
            #open projects module
            
            
            break
        elif user_email == "q":
            print("See you soon, Stay Cool")
            break
        elif user_email == "r":
            print("Loading the register page.......")
            register_user(mail)
            break
        else:
            print(f"{user_email} is not registered. \n Please try again\n")

            
def register_user(mail):
    """
    registers new user email
    """
    clear()
    while True:
        new_user_email = input("Please enter your email address to register: \n")
        try:
           valid_new_user_email = validate_email(new_user_email,check_deliverability = False)
           print(f"{valid_new_user_email } is a valid email.")
           new_email_check(new_user_email, mail)
           break
           
        except EmailNotValidError:  
            print(f"{new_user_email} is not a valid email address.")
            
            
def new_email_check(new_user_email, mail):
    """
    Checks to see if the entered email is already in use
    """
    if new_user_email in mail:
        print("The email addrress you entered is already in use. \n")
        print("Please use a different email or login \n")
        check_email_registered()
        
    else:
        SHEET.worksheet("email").append_row([new_user_email])
        create_new_user_name(new_user_email)  
                
def create_new_user_name(new_email):
    while True:
        new_user_name = [input("Please enter a new user name(no more than 8 characters): ")]
        if len(new_user_name) <= 8:
            SHEET.add_worksheet(title = new_email, rows=100, cols=20)
            worksheet_to_update = SHEET.worksheet(new_email)
            worksheet_to_update.append_row(new_user_name)
            print(f"{new_user_name[0]} welcome to the Coldroom Capacity Calculator. ")
            print(f"{new_email} is your registered email.")
            print("Loading Projects......")
            break
        else:
             print("Your username cannot be bigger than 8 characters!")
                   
    
check_email_registered()