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

# creates some whitespace for Heroku
space = "     "


def clear():
    """
    Function to clear the console
    """
    os.system("cls" if os.name == "nt" else "clear")
def get_project_type():
    while True:
        new_type = input(f"{space}Please enter the Type.\n [k] for Kitchen 2°C\n [b] for Beverages 6°C or \n [d] for Deepfreeze\n")
        if new_type.strip() == 'k':
            return "Kitchen", "2"
        elif new_type.strip() == 'b':
            return "Beverages", "6"
        elif new_type.strip() == 'd':
            return "Deepfreeze", "-18"
        else:
            print(f"{space}Please enter a valid type")

def create_project():
    new_row = [""]
    new_name = input(f"{space}Enter a new project name:  \n")
    if new_name.strip() == "":
        print("Please enter a valid project name: \n")
        return
    else:
        new_row.append(new_name)
    new_type, temp = get_project_type()
    new_row.append(new_type)
    new_temp = temp + "°C"
    new_row.append(new_temp)
    new_volume = calc_volume()
    new_row.append(str(new_volume)+ "m³")
    new_insulation = insulation_thickness()
    new_row.append(new_insulation)
    new_floor = insulsulated_floor()
    new_row.append(new_floor)
    capacity = calculate_capacity(new_type, new_insulation, new_volume, new_floor)
    new_row.append(str(capacity) +" kW") 
    return new_row

def load_project(user_email):
    """
    Load the project and display the project menu
    """
    clear()
    title = pyfiglet.figlet_format("* * * * * *", font = "5lineoblique" ) 
    print(Fore.BLUE + f"{space}{title}" + Style.RESET_ALL + f" * {user_email} Welcome to your project Page * \n") 
    while True:
        project_sheet = SHEET.worksheet(user_email)
        project_display = project_sheet.get_all_values()
        # if project_display:
        print("Your Projects: \n")
        for i in range(1, len(project_display)):
            print(f" || User: {project_display[0][0]} || Project: {project_display[i][1]} || Type: {project_display[i][2]} || Temperature: {project_display[i][3]} ||    Volume: {project_display[i][4]} || Insulation {project_display[i][5]} || Insulated Floor {project_display[i][6]} || Capacity {project_display[i][7]} ||\n")
        # else:
        #     print(f"{space}Please create a new project...... \n")             
        leave = input(f"{space} Enter [c] to create a project or[b] to go back \n")
        if leave == "b":
            check_email_registered()
            break
        elif leave == "c":
            new_row = create_project()
        else:
            print(f"{space} Enter a valid option....")
        if new_row:
            project_sheet.append_row(new_row)
            
         
        
def calculate_capacity(new_type, new_insulation, new_volume, new_floor):
    """
    Calculates the capacacity in kW from Volume, insulation and floor
    """
    print(f"{space}Calculating Capacity....\n")

    temp_ranges = {"Kitchen": 2, "Beverages": 6, "Deepfreeze": -18}
    base_and_steps = {(6, "70mm"): (455, 5.4), (2, "70mm"): (565, 6.4), (-18, "100mm"): (630, 7.2), 
                      (6, "100mm"): (420, 5.4), (2, "100mm"): (509, 5.8)}

  

    temp_range = temp_ranges[new_type]
    if new_type == "Deepfreeze":
        new_insulation = "100mm"

    if (temp_range, new_insulation) not in base_and_steps:
        print(f"{space}Unknown temp range and insulation combination: {temp_range}, {new_insulation}")
        return

    base, step = base_and_steps[(temp_range, new_insulation)]
    capacity = base + (step * (new_volume * 10))
    
    if new_floor == "No":
        capacity *= 1.2
    capacity = round(capacity, 1)

    print(f"{space}The required capacity for the {new_type} Coldroom with a Volume of {new_volume}m³ is {capacity} kW\n")
    return capacity
    



        
def insulsulated_floor():
    print(f"{space}* Please choose if the Coldroom has an Insulated Floor *\n")
    while True:
        try:
            insulated = input("      [y]: Yes or [n]: No: ")
            if insulated == "y":
                return "Yes"
            elif insulated == "n":
                return "No"
            else:
                print(f"{space}Please enter a valid option\n")
        except ValueError as e:
            print(f"{space}{e} is not valid. Please enter a valid option\n") 
            
            
                  
def insulation_thickness(): 
    print(f"{space}* Please choose the Insulation Thickness *\n")
    while True:
        try:
            insulation = input(f"{space}[a]: 70mm or [b]: 100mm: \n")
            if insulation == "a":
                return "70mm"
            elif insulation == "b":
                return "100mm"
            else:
                print(f"{space}Please enter a valid option\n")
        except ValueError as e:
            print(f"{space}{e} is not a number. Please enter a valid number\n")
    
    
    
          
def calc_volume():
    print(f"{space} * Please enter the dimensions of the Coldroom in Meters *\n")
    while True:
        try:
            height = float(input(f"{space}Height: \n"))
            width = float(input(f"{space}Width: \n"))
            length = float(input(f"{space}Length: \n"))
            break
        except ValueError as e:
            print(f"{e} is not a number. Please enter a valid number\n")
    
    return round(height * width * length, 1)
       
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
            print(f"{space}Sorry an error has occurred.\n Please contact support.\n www.ccc@cold-calc.freeze\n")
            break
        
        # Print the title 
        title = pyfiglet.figlet_format("* * * * * * ", font = "5lineoblique" ) 
        print(Fore.BLUE + space, title + Style.RESET_ALL + f"{space}* Welcome to the Coldroom Calculator * \n")    
        
        # get user email and check if they are registered, quit or open the register module
        user_email = input(f"{space}Please enter your registered email address,\n {space}or enter: \n [r] to register.\n [i] for more information\n [q] to quit: \n{space}")
        user_email = user_email.lower().strip()
        if user_email in mail:
            print(f"{space}Loading your Projects......\n")
            load_project(user_email)
            break
        elif user_email == "i":
            print(f"{space}Loading info page...... \n")
            instruction_page()
            break
        elif user_email == "q":
            print(f"{space}See you soon, Stay Cool\n")
            break
        elif user_email == "r":
            print(f"{space}Loading the register page.......\n")
            register_user(mail)
            break
        else:
            print(f"{space}{user_email} is not registered. \n Please try again\n")

def instruction_page():
    while True:
        instructions = """The 'Coldroom Capacity Calculator' is a tool designed to help \n
you get peak performance from commercial refrigeration systems.\n
The power capacity of newly installed systems must match the demand\n
to keep you and your customers happy.\n
This tool is the place to start.\n
Please enter an email address to get started.\n

choose a user name and start a new project.\n

Step 1: Enter the desired Temperature in celsius \n
        2°C for Kitchen 6°C for Beverages -18 for Deep Freeze\n
        
Step 2: Enter the Dimensions of the Coldroom in Meters. \n
        Height, Width and Length \n
        
Step 3: Select the thickness of the Insulation Panels \n
        A: 70mm B: 100mm \n
                         
Step 4: Enter whether or not the Coldroom has an insulated floor:\n
        A: Yes B: No \n
                                
Step 5: The Coldroom Capacity Calculator then calculates the required\n
refrigeration capacity needed in Kilo-Watts.\n

Allowing you to select the appropriate equipment\n
for inatallation. \n

  Please bear in mind that any results are merely suggestions. \n
                        """
        print(space, instructions)
        back = input(f"{space}Enter [b] to go back: ")
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
        new_user_email = input(f"{space}Please enter your email address to register: \n {space}or enter [b] to go back.\n{space}")
        try:
           valid_new_user_email = validate_email(new_user_email,check_deliverability = False)
           print(f"{space}{valid_new_user_email } is a valid email.")
           new_email_check(new_user_email, mail)
           break
           
        except EmailNotValidError:  
            print(f"{space}{new_user_email} is not a valid email address.\n")
        if new_user_email.strip() == "b":
            clear()
            print(f"{space}Going back.....\n")
            check_email_registered()
            break
                
            
def new_email_check(new_user_email, mail):
    """
    Checks to see if the entered email is already in use
    """
    if new_user_email in mail:
        print(f"{space}The email addrress you entered is already in use. \n")
        print(f"{space}Please use a different email or login \n")
        check_email_registered()
        
        
    else:
        SHEET.worksheet("email").append_row([new_user_email])
        create_new_user_name(new_user_email)  
                
def create_new_user_name(new_email):
    while True:
        new_user_name = input(f"{space}Please enter a new user name(no more than 8 characters): \n{space}")
        new_user_name.strip().replace(' ', '-')
        if len(new_user_name) <= 8 and len(new_user_name) > 0:
            SHEET.add_worksheet(title = new_email, rows=100, cols=20)
            worksheet_to_update = SHEET.worksheet(new_email)
            worksheet_to_update.append_row([new_user_name, "Project", "Type", "Temperature", "Volume", "Insulation", "Insulated Floor", "Capacity in kW"])
            print(f"{space}{new_user_name} welcome to the Coldroom Capacity Calculator. ")
            print(f"{space}{new_email} is your registered email.")
            print(f"{space}Loading Projects......")
            load_project(new_email)
            break
        else:
             print(f"{space}Your username cannot be bigger than 8 characters or empty!")
                   
    
check_email_registered()