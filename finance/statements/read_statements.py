#!/opt/local/bin/python3.2

import sys
import math
import subprocess

class Bank: # interface
    def __init__(self):
        pass

class Sparkasse(Bank):
    def __init__(self):
        pass

class HSBC(Bank):
    def __init__(self):
        pass

def checkBank(filename):
    bank = None
    iFile = open(filename, "r")
    try:
        line = iFile.readline()
    except UnicodeDecodeError:
        bank = Sparkasse()
        iFile.close()
    else:
        bank = HSBC()
        iFile.close()
    return bank

if __name__ == "__main__":
    # collect info here
    dates = {}
    whos = {}
    balance = 0.0
    # list CSV files
    byte_string = subprocess.check_output("ls *.csv", shell = True)
    words = byte_string.split()
    # check which bank we are using
    bank = checkBank(words[0])
    if bank.__class__ == Sparkasse:
        print("TODO: Sparkasse")
        sys.exit()
    else:
        print("TODO: HSBC")
    # HSBC
    for word in words:
        print("reading \"%s\" ..." % str(word, encoding='utf8'))
        iFile = open(word, "r")
        # read CSV file line by line
        lineNumber = 0
        while 1:
            lineNumber = lineNumber + 1
            line = iFile.readline()
            if line == "":
                # EOF
                break
            else:
                words = line[:-1].split(',')
                date = words[0]
                who = words[1]
                amount = words[2]
                try:
                    dates[date].append([who, amount])
                except KeyError:
                    dates[date] = [[who, amount]]
                try:
                    whos[who].append([who, amount])
                except KeyError:
                    whos[who] = [[who, amount]]
        iFile.close()
    # colored lines using ANSI/VT100 Terminal Control Escape Sequences
    # (see http://www.termsys.demon.co.uk/vtansi.htm#colors)
    bright = 1
    red = 31
    green = 32
    yellow = 33
    # formating
    len_date = len("YYYY-MM-DD")
    len_amount = len("-1234.12")
    len_space = len(" ")
    len_fill = 0   # varies
    len_amount = 0 # varies
    # do something with the collected data
    keys = list(dates.keys())
    keys.sort()
    for date in keys:
        for who_amount in dates[date]:
            who, amount = who_amount
            amount = float(amount)
            balance += amount
            len_amount = len(str("%.2f" % amount))
            if amount < 0.0:
                amount = "\033[%s;%sm%.2f\033[0m" % (bright, red, amount)
            else:
                amount = "\033[%s;%sm%.2f\033[0m" % (bright, green, amount)
            len_fill = 79 - len_date - 2 * len_space - len(who) - len_amount
            fill = " " * len_fill
            date = "\033[%s;%sm%s\033[0m" % (bright, yellow, date)
            print("%s %s%s %s" % (date, who, fill, amount))
    print("-" * 79)
    balance = balance * 100.0 # pence
    balance = math.floor(balance + 0.5)
    balance = balance / 100.0 # pound
    len_amount = len(str(balance))
    if balance < 0.0:
        balance = "\033[%s;%sm%s\033[0m" % (bright, red, balance)
    else:
        balance = "\033[%s;%sm%s\033[0m" % (bright, green, balance)
    len_fill = 79 - len_date - 2 * len_space - len_amount
    fill = " " * len_fill
    print("%s %s %s" % (date, fill, balance))
