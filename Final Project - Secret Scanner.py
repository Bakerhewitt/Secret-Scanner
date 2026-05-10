import re
import os
import argparse
import logging

#Logging was written with the assistance of Claude
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


patterns = [
    r'password\s*=\s*\S+', 
    r'[a-f0-9]{32}', #Datadog API Key
    r'[a-f0-9]{40}', #Datadog Application Key
    r'sqOatp-[0-9A-Za-z-_]{22}', #Square Access Token
    r'q0csp-[0-9A-Za-z-_]{43}', #OAuth Secret
    r'55[0-9a-fA-F]{32}', #Twilio Access Token
    
]


secrets = []

def _secretsearch_file_():
    filename = input("Enter file path for investigation: :")
    try:
        with open(filename, "r", encoding="utf-8") as f:
#            file_data = f.read() # This line was removed at the recommendation of Claude
            for line_number, line in enumerate(f, start=1): #This line was edited by Claude to replace filename with f
                for pattern in patterns:
                    matches = re.findall(pattern, line)
                    if matches:
                        secrets.append([filename, line_number, matches])
                        logging.warning(f"Match found at line {line_number} in {filename}: {matches}") #This line was written with the assistance of Claude
        if secrets:
            print("Secrets found: ", secrets) 
        else:
            print("No secrets found.")
    except FileNotFoundError:
        print("File not found.")   

        
        
def _secretsearch_directory_():
    directoryname = input("Enter directory for investigation: ")
    for root, dirs, files in os.walk(directoryname):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    #This line was changed from with open(filepath, "r") as f: 
#                   file_data = f.read() # This line was removed at the recommendation of Claude
                    for line_number, line in enumerate(f, start=1):
                        for pattern in patterns:
                            matches = re.findall(pattern, line)
                            if matches:
                                secrets.append([filepath, line_number, matches])
                                #The below lines were written with the assistance of Claude
                                logging.warning(f"Match found at line {line_number} in {filepath}: {matches}") # This line was written with the assistance of Claude
            except FileNotFoundError:
                print("File not found.")
            except UnicodeDecodeError:
                pass
    if secrets:
        print("Secrets found: ", secrets)
    else:
        print("No secrets found.")
        
def _search_():
    print("Choose an option:")
    print("1. File")
    print("2. Directory")
    searchtype = input("Enter your choice (1 or 2): ")
    
    if searchtype == "1":
        _secretsearch_file_()
    elif searchtype == "2":
        _secretsearch_directory_()
    else:
        print("Invalid Choice.")
     
#Testing for regex        
#def validate_file(#fileinfo):
#    pattern = r #An array goes here to define allowable information?
#    
#    if re.findall(pattern, #fileinfo):
#        print(#Valid match affirmation)
#    else
#        print(#Invalid match affirmation)

#Variable goes here for validation, in this case that variable is located within the secretsearch functions
#Validation occurs here? I'm not sure
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secret Scanner - Scans files or directories for hardcoded secrets.") #From here to the next comment was written with the assistance of Claude
    parser.add_argument("--path", help="Path to a file or directory to scan")
    parser.add_argument("--type", choices=["file", "directory"], help="Type of scan: 'file' or 'directory'")
    args = parser.parse_args()

    if args.path and args.type:
        if args.type == "file":
            _secretsearch_file_()
        elif args.type == "directory":
            _secretsearch_directory_() #Endpoint of Claude assistance
   
    choice = input("Would you like to search for some secrets?").strip().lower()
    #Scrub for spaces and capital letters here, allow variations of Yes/yes No/no 
    
    if choice == "yes":
        _search_()
    elif choice == "no":
        print("Scaredy cat!")
    else:
        print("Invalid choice.")
        

        
    
    
        
    

    