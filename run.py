#Main Python file

# import the various libraries
import pyfiglet 
import gspread
from google.oauth2.service_account import Credentials
import os
from email_validator import validate_email, EmailNotValidError
from colorama import Fore, Style


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



# define a class for the coldrooms
# class Coldroom:
#     def __init__(self, user, project, type, temperature, volume, insulation, floor, capacity):
#         self.user = user
#         self.project = project
#         self.type = type
#         self.temperature = temperature
#         self.volume = volume
#         self.insulation = insulation
#         self.floor = floor
#         self.capacity = capacity

def clear():
    """
    Function to clear the console
    """
    os.system("cls" if os.name == "nt" else "clear")
    


def load_project(user_email):
        """
        Load the project and display the project menu
        """
        clear()
       
        title = pyfiglet.figlet_format(" * * * *", font = "5lineoblique" ) 
        print(Fore.BLUE + f"{title}" + Style.RESET_ALL + "* Welcome to your project Page * \n") 
        print(f"{user_email} Project Page")
        project_sheet = SHEET.worksheet(user_email)
        
        # projects = project_sheet.col_values(2)
        new_row = [""]
        new_name = input("Please enter a new project name:  ")
        new_row.append(new_name)
        while True:
            new_type = input("Please enter the Type.\n [k] for Kitchen 2°C\n [b] for Beverages 6°C or \n [d] for Deepfreeze\n")
            if new_type.strip() == 'k':
                new_type = "Kitchen"
                temp = "2"
                break
            elif new_type.strip() == 'b':
                new_type = "Beverages"
                temp = "5"
                break
            elif new_type.strip() == 'd':
                new_type = "Deepfreeze"
                temp = "-18"
                break
            else:
                print("Please enter a valid type")
        new_row.append(new_type)
        new_temp = temp + "°C"
        new_row.append(new_temp)
        new_volume = calc_volume()
        new_row.append(str(new_volume)+ "m³")
        new_insulation = insulation_thickness()
        new_row.append(new_insulation)
        new_floor = insulsulated_floor()
        new_row.append(new_floor)
        
        
        
        
        project_sheet.append_row(new_row)
        
def insulsulated_floor():
    print("* Please choose if the Coldroom has an Insulated Floor *")
    while True:
        try:
            insulated = input("[y]: Yes or [n]: No: ")
            if insulated == "y":
                return "Yes"
            elif insulated == "n":
                return "No"
            else:
                print("Please enter a valid option")
        except ValueError as e:
            print(f"{e} is not valid. Please enter a valid option") 
            
            
                  
def insulation_thickness(): 
    print("* Please choose the Insulation Thickness *")
    while True:
        try:
            insulation = input("[a]: 70mm or [b]: 100mm: ")
            if insulation == "a":
                return "70mm"
            elif insulation == "b":
                return "100mm"
            else:
                print("Please enter a valid option")
        except ValueError as e:
            print(f"{e} is not a number. Please enter a valid number")
    
    
    
          
def calc_volume():
    print(" * Please enter the dimensions of the Coldroom in Meters *")
    while True:
        try:
            height = float(input("Height: "))
            width = float(input("Width: "))
            length = float(input("Length: "))
            break
        except ValueError as e:
            print(f"{e} is not a number. Please enter a valid number")
    
    return height * width * length
    
        

              
            
            
            
            
# mail = "dd@ee.aa"
# new_user_name = "Derek"
# load_project(mail)           

       
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
        
        # Print the title 
        title = pyfiglet.figlet_format(" * * * *", font = "5lineoblique" ) 
        print(Fore.BLUE + f"{title}" + Style.RESET_ALL + "* Welcome to the Coldroom Calculator * \n")    
        
        # get user email and check if they are registered, quit or open the register module
        user_email = input("Please enter your registered email address,\n or Enter: \n [r] to register.\n [i] for more information\n [q] to quit: \n")
        user_email = user_email.lower().strip()
        if user_email in mail:
            print("Loading your Projects......\n")
            load_project(user_email)
            break
           
            
            
            break
        elif user_email == "i":
            print("Loading info page...... \n")
            instruction_page()
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

def instruction_page():
    while True:
        instructions = """The 'Coldroom Capacity Calculator' is a tool designed to help \n
you get peak performance from commercial refrigeration systems.\n
The power capacity of newly installed systems must match the demand\n
to keep you and your customers happy.\n
This tool is the place to start.\n
Step 1: Enter the desired Temperature in celsinn Panels \n
        Industry Standard A: 70mm or B: 100mm \n
                                
Step 4: Enter whether or not the Coldroom has an insulated floor:\n
        A: Yes B: No \n
                                
Step 5: The Coldroom Capacity Calculator then calculates the required\n
refrigeration capacity needed in Kilo-Watts.\n
Allowing you to select the appropriate equipment\n
for inatallation. \n
  Please bear in mind that any results are merely suggestions. \n
                        """
        print(instructions)
        back = input("Enter [b] to go back: ")
        if back.strip() == "b":
            clear()
            check_email_registered()
            break
        
    
    
    
               
def register_user(mail):
    """
    registers new user email
    """
    clear()
    while True:
        new_user_email = input("Please enter your email address to register: \n or enter [b] to go back.\n")
        try:
           valid_new_user_email = validate_email(new_user_email,check_deliverability = False)
           print(f"{valid_new_user_email } is a valid email.")
           new_email_check(new_user_email, mail)
           break
           
        except EmailNotValidError:  
            print(f"{new_user_email} is not a valid email address.")
        if new_user_email.strip() == "b":
            clear()
            print("Going back.....")
            check_email_registered()
            break
                
            
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
        
        new_user_name = input("Please enter a new user name(no more than 8 characters): \n")
        new_user_name.strip().replace(' ', '-')
        if len(new_user_name) <= 8:
            SHEET.add_worksheet(title = new_email, rows=100, cols=20)
            worksheet_to_update = SHEET.worksheet(new_email)
            worksheet_to_update.append_row([new_user_name, "Project", "Type", "Temperature", "Volume", "Insulation", "Insulated Floor", "Capacity in kW"])
            print(f"{new_user_name} welcome to the Coldroom Capacity Calculator. ")
            print(f"{new_email} is your registered email.")
            print("Loading Projects......")
            load_project(new_email, new_user_name)
            break
        else:
             print("Your username cannot be bigger than 8 characters!")
                   
    
check_email_registered()