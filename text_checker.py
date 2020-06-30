#!/usr/bin/python3

###########################################
#  http://github.com/r4v10l1              #
#  https://raidforums.com/User-ravi0li    #
#  This script checks if the content of   #
#  a page changes.                        #
#  Check the comments in code to adapt    #
#  the code.                              #
###########################################


import requests
import smtplib
import time
from colorama import Fore, Style
from bs4 import BeautifulSoup

##  VARS YOU NEED TO EDIT  ##
TESTER = False
MANUAL_MODE = True
#############################

if "MANUAL_MODE" not in locals():
    print()
    print(" %s%s[!] Error. MANUAL_MODE variable is not set.%s" % (Style.BRIGHT, Fore.RED, Style.RESET_ALL))
    print()
    exit(1)

#MANUAL-MODE---------------------------------------------------------------------------------
if MANUAL_MODE:
    SSL = input(" %s%s[*] Does your site have (http) or (https)?%s >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.WHITE, Style.RESET_ALL))
    URL = input(" %s%s[*] Your URL%s >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.WHITE, Style.RESET_ALL))

    if "http" not in URL.lower():
        if SSL.strip().lower() == "http":
            URL = "http://%s" % URL
        elif SSL.strip().lower() == "https":
            URL = "https://%s" % URL
        else:
            print(" %s%s[!] Error. You must type \"http\" or \"https\"%s" % (Style.BRIGHT, Fore.RED, Style.RESET_ALL))
            print()
            exit(1)
    elif "https://" in URL.lower() and SSL.strip().lower() != "https":
        print(" %s%s[!] Error. Https and URL do not match...%s" % (Style.BRIGHT, Fore.RED, Style.RESET_ALL))
        exit(1)
    elif "http://" in URL.lower() and SSL.strip().lower() != "http":
        print(" %s%s[!] Error. Http and URL do not match...%s" % (Style.BRIGHT, Fore.RED, Style.RESET_ALL))
        exit(1)

    USER_AGENT = input(" %s%s[*] Your user agent%s (https://www.google.com/search?q=my+user+agent) >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.WHITE, Style.RESET_ALL))
    if "/" not in USER_AGENT:
        print(" %s%s[!] Error. You must type a valid user agent.%s" % (Style.BRIGHT, Fore.RED, Style.RESET_ALL))
        print()
        exit(1)
    HEADERS = {"User-Agent": str(USER_AGENT)}

    CLASS_ID = input(" %s%s[*] ID of the class you want to check%s >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.WHITE, Style.RESET_ALL))
    TEXT2CHECK = input(" %s%s[*] Text you want to check%s >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.WHITE, Style.RESET_ALL))
#NOT-MANUAL----------------------------------------------------------------------------------
elif not MANUAL_MODE:
    URL = "http://example.com"  # Here you put the URL you want to check
    CLASS_ID = "example_123"  # Replace the id with the <div class="the_id_is_here"> of the text you want to check, for example.
    TEXT2CHECK = "eXaMpLe"  # The text that is inside the CLASS_ID text. ! Capital letters count !
    # TEXT2CHECK = TEXT2CHECK.lower()
    USER_AGENT = "Here/Your/User/Agent"# Here you replace the second string with your user agent (https://www.google.com/search?q=my+user+agent)

    if URL == "http://example.com":
        print()
        print(" %s[!] Error. You need to replace the url in the python code or use manual mode.%s" % (Fore.RED, Style.RESET_ALL))
        print()
        exit(1)
    if CLASS_ID == "example_123":
        print()
        print(" %s[!] Error. You need to replace the class id in the python code or use manual mode.%s" % (Fore.RED, Style.RESET_ALL))
        print()
        exit(1)
    if USER_AGENT == "Here/Your/User/Agent":
        print()
        print(" %s[!] Error. You need to replace the user agent in the python code or use manual mode.%s" % (Fore.RED, Style.RESET_ALL))
        print()
        exit(1)
    if TEXT2CHECK == "eXaMpLe":
        print()
        print(" %s[!] Error. You need to replace the text to check in the python code or use manual mode.%s" % (Fore.RED, Style.RESET_ALL))
        print()
        exit(1)

    HEADERS = {"User-Agent": str(USER_AGENT)}


def check_page():
    PAGE = requests.get(URL, headers=HEADERS)  # Uses requests lib to get the content of the page
    SOUP = BeautifulSoup(PAGE.content, "html.parser")
    CONTENT = SOUP.find(id=CLASS_ID)
    if CONTENT == None:
        print()
        print(" %s[!] Error. Class id not found.%s" % (Fore.RED, Style.RESET_ALL))
        print()
        exit(1)


    if TESTER:  # Here dependinng of the var at the begining if displays the CONTENT and FILTERED_CONTENT variables.
        print(CONTENT)
        FILTERED_CONTENT = CONTENT[5:15]  # You can change this variable to extrat a part of the CONTENT variable.
        print("----------------------------------------------------")
        print("[" + FILTERED_CONTENT + "]")
        print("----------------------------------------------------")
        exit(1)

    if MANUAL_MODE:
        if TEXT2CHECK in CONTENT:
            print()
            print(" %s[+] Success! [%s] was found in [%s]!%s" % (Fore.GREEN, TEXT2CHECK, URL, Style.RESET_ALL))
            print()
            exit(1)
        else:
            print()
            print(" %s[!] Error. [%s] was found in [%s].%s" % (Fore.RED, TEXT2CHECK, URL, Style.RESET_ALL))
            print()
            exit(1)

def send_mail():

    MAIL = "your_email"  # Here goes your email
    PASSWORD = "your_password"  # !! DO NOT USE YOUR ORIGINAL PASSWORD !! Go to (https://myaccount.google.com/apppasswords) to set one.

    if MAIL == "your_email":
        print()
        print(" %s[!] Error. You need to replace the email in the python code.%s" % (Fore.RED, Style.RESET_ALL))
        print()
        exit(1)
    if PASSWORD == "your_password":
        print()
        print(" %s[!] Error. You need to replace the password in the python code.%s" % (Fore.RED, Style.RESET_ALL))
        print()
        exit(1)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(MAIL, PASSWORD)

    subject = "[+] Web changes!"
    body = "Your content changed! [%s] changed in [%s]!" % (TEXT2CHECK, URL)"
    msg = "Subject: %s\n\n%s" % (subject, body)
    server.sendmail(MAIL, MAIL, msg)

    server.quit()

# while True:
#     check_page()
#     time.sleep()  # Your secconds
#     if TEXT2CHECK in CONTENT:
#         send_mail()

check_page()
if TEXT2CHECK in CONTENT:
    send_mail()

exit(1)
