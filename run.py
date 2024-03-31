#Main Python file

# import pyfiglet module command line font creator library
import pyfiglet 

#import the gspread online spreadsheet
import gspread
from google.oauth2.service_account import Credentials

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

def check_email_registered():
    while True:
        # try statement to check if worksheet exists otherwise break and show error message
        try:
            email_address = SHEET.worksheet("emailx")
            mail = email_address.col_values(1)
            
        except:
            print("Sorry an error has occurred.\n Please contact support.\n www.ccc@cold-calc.freeze")
            break
            
        # get user email and check if they are registered, quit or open the register module
        user_email = input("Please enter your registered email address, \n 'r' to register or 'q' to quit: \n")
        if user_email in mail:
            print("Loading Projects......\n")
            break
        elif user_email == "q":
            print("See you soon, Stay Cool")
            break
        elif user_email == "r":
            print("Loading the register page.......")
            break
        else:
            print(f"{user_email} is not registered. \n Please try again\n")
            
       
    
check_email_registered()