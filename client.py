
import os, sys, signal, platform

from constants import *
from banner import *
from calc import calc

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def quit():
    print()
    print("Goodbye!")
    print()
    sys.exit(0)

# catch Ctrl+C interrupt
def signal_handler(sig, frame):
    print(entry)
    print()
    quit()

signal.signal(signal.SIGINT, signal_handler)

def printError(msg: str):
    print(bcolors.WARNING, bcolors.BOLD, ERR_prefix, bcolors.ENDC, msg, sep="")

# START HERE

clear()

# TODO: parse the arguments so you can switch convention notation and select banner using convention= and banner=
if 1 in sys.argv:
    banner(int(sys.argv[1]))
else:
    banner()

print()
print("Welcome!")
print("You may enter your desired calculation below then press enter to get the result")
print()



convention = 1
limit = 32
entry = ""
while True:
    doCalc = True
    entry = input("> ")
    print()

    words = entry.split(" ")
    lenW = len(words)
    if lenW >= 1:
        if words[0] == "q" or words[0] == "quit" or words[0] == "exit" or words[0] == "bye":
            break
        elif words[0] == "b" or words[0] == "banner":
            if lenW == 2:
                try:
                    bcount = int(words[1])
                    clear()
                    banner(bcount)
                except:
                    printError("banner selection needs a number")
            doCalc = False
        elif words[0] == "set":
            if lenW == 3:
                if words[1] == "convention" or words[1] == "conv" or words[1] == "c":
                    try:
                        if words[2] >= "1" and words[2] <= "4":
                            convention = int(words[2])
                        else:
                            raise Exception("Number not in range")
                    except:
                        printError("bad convention number")
                elif words[1] == "limit" or words[1] == "lim" or words[1] == "l":
                    try:
                        limit = int(words[2])
                    except:
                        printError("limit has to be a number")
                else:
                    printError("unrecognized command")
            else:
                printError("set needs more parameters, see help")
            doCalc = False
        elif words[0] == "help" or words[0] == "h":
            print("""
Usage:
    q|quit|exit|bye             => quits program (as well as Ctrl+c interrupt)
    b|banner (1-9)              => displays a random banner again (you can optionally choose the banner with a number)
    h|help                      => displays this usage
    set                         => sets a parameter
    set l|lim|limit number      => sets the limit for decimal calculation in divisions (default is 32) 
    set c|conv|convention 1-3   => sets convention (1=dev ; 2=eu ; 3=us) dev convention is the default 
        # convention list:
        # 1 = "." float separation and no space (default)
        # 2 = "," float separation with spacing each 3 decimal (eu)
        # 3 = "." float separation and "," groups of 3 decimal separation (us)
                """)
            doCalc = False

    if doCalc:
        out = calc(entry, convention, limit)
        # if the output of calc is an error, print a colored version instead
        if out[:len(ERR_prefix)] == ERR_prefix:
            printError(out[len(ERR_prefix):])
        else:
            print(out)

    print()
    entry = ""

quit()

