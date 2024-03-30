#Main Python file
# import pyfiglet module 
import pyfiglet 

title = pyfiglet.figlet_format(" * * * *", font = "5lineoblique" ) 

print(f"{title}* Welcome to the Coldroom Calculator * \n")

def validate_email():
    while True:
        email = input(" Please enter Your email address to continue: \n")
        if email == "q":
            break
        
    
validate_email()