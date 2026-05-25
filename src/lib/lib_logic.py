import argparse
import sys
from prompt_toolkit import prompt #TODO import ot readme that they  must to pip install prompt_toolkit
import os
#own library
import lib.lib_file as lib_file


def CLI_interface():
    """Start the script with argparse"""
    parser = argparse.ArgumentParser(description="process file path")
    parser.add_argument("-r", "--route", type=str, help="route to the file")
    parser.add_argument("-b", "--route_back", type=str, help="route to the back file")
    parser.add_argument("-s", "--save_route", type=str, help="route where the file can be saved")
    args = parser.parse_args()
    
    if args.route and args.route_back:
        sys.exit("Pocet povolenych argumentu -b, -r je pouze 1")
    elif args.route:
        lib_file.createCompressFile(args.route, args.route_back)
        sys.exit(0)
    elif args.route_back:
        lib_file.createNormalFile(args.route_back)
    else:
        command_own_interface()

def predefined_input(normal_input:str, additional_input:str = "") -> prompt:
    """Input using last user query, that can be modifed"""
    return prompt(normal_input, default=additional_input)

    
def command_own_interface():
    """Start the script out of the normal CLI to own"""
    res = "Compre Response>>> "
    resError = "Compre Error>>> "
    resHelp = "Compre Help>>> "


    version = "0.1.7"
    helpBlock = ""
    historyText = ""
    helpCurrentDirectoryHelpActivate = False

    print(f"Welcome to COMPRE\nCAUTION: This program is case sensitive\nVersion: {version}\nFor showing all commands type \"help\"\n")

    while True:
        if helpCurrentDirectoryHelpActivate:
            helpCurrentDirectoryHelpActivate = False
        userInput = predefined_input("Compre Terminal>> ", helpBlock)
        helpBlock = ""
        try:
            if (userInput == "quit" or userInput == "q"):
                break
            elif (userInput == "b"):
                helpBlock = historyText
            elif (userInput == "help"):
                for cmd, info in commands.items():
                    print(res + cmd + " : " + info)
            elif userInput.startswith("compre") and len(userInput.split()) > 1:
                newUserInput=userInput.split()
                if (newUserInput[1] == "h"):
                    helpBlock = "compre "
                    helpBlock += os.getcwd()
                elif(newUserInput[1] == "bh"):
                    helpBlock = "compre b "
                    helpBlock += os.getcwd()
                elif (len(newUserInput) == 3):
                    if (newUserInput[2] == "ls"):
                        print(resHelp, os.listdir(newUserInput[1]))
                        helpBlock = newUserInput[0] + " " + newUserInput[1]
                    elif newUserInput[1] == "b":
                        if len(newUserInput) > 2:
                            lib_file.createNormalFile(newUserInput[2])
                        else:
                            print(res + f"Neplatný příkaz. Pro pomoc napište \"help\"\n")
                            
                    else:
                        print(res + f"Neplatný příkaz. Pro pomoc napište \"help\"\n")
                else:
                    lib_file.createCompressFile(newUserInput[1])
            else:
                print(res+"Neplatný příkaz. Pro pomoc napište \"help\"\n")
        except Exception as e:
            print(resError,e)
        historyText = userInput


commands = {
    "q/quit": "exit the program",
    "b": "return previous command",
    "help": "show available commands",
    "compre <path>": "create a compressed file",
    "compre h": "return working directory in next line(can be changed by user)",
    "compre bh": "return working directory used to decompressed(can be changed by user)",
    "compre <path> ls": "list of the names of the entries in a directory",
    "compre b <path>": "return back the compressed file .barcal to normal one",
}