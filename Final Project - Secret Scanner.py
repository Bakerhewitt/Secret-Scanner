import re
import os
import argparse
import logging

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
    filename = input("Enter filename for investigation: ")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            file_data = f.read()
            for line_number, line in enumerate(file_data, start=1):
                for pattern in patterns:
                    matches = re.findall(pattern, line)
                    if matches:
                        secrets.append([filename, line_number, matches])
        print("Secrets found: ", secrets)
    except FileNotFoundError:
        print("File not found.")
        
        
def _secretsearch_directory_():
    directoryname = input("Enter directory for investigation: ")
    for root, dirs, files in os.walk(directoryname):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r") as f:
                    file_data = f.read()
                    for line_number, line in enumerate(file_data, start=1):
                        for pattern in patterns:
                            matches = re.findall(pattern, line)
                            if matches:
                                secrets.append([filepath, line_number, matches])

                    print("Secrets found: ", secrets)
            except FileNotFoundError:
                print("File not found.")
        
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
    choice = input("Would you like to search for some secrets?").strip().lower()
    #Scrub for spaces and capital letters here, allow variations of Yes/yes No/no 
    
    if choice == "Yes":
        _search_()
    elif choice == "No":
        print("Scaredy cat!")
    else:
        print("Invalid choice.")
        

        
    
    
        
    

    