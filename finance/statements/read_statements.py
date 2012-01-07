#!/opt/local/bin/python3.2

import csv
import sys
import math
import subprocess

class Bank: # interface
    def __init__(self):
        self.filenames = []
        self.encoding = "utf8"
        self.delimiter = ','
        self.dates = {}
        self.whos = {}
        self.balance = 0.0

    def readCsvFile(self, filename):
        print("TODO: %s has to implement readCsvFile(...)" % self.__class__)

    def convertDate(self, date):
        print("TODO: %s has to implement convertDate(...)" % self.__class__)
        return None

class Sparkasse(Bank):
    def __init__(self):
        args = [self]
        Bank.__init__(*tuple(args))
        # bank specific members
        self.encoding = "cp1252"
        self.delimiter = ';'

    def readCsvFile(self, filename):
        print("reading \"%s\" ..." % filename)
        # we assume the CSV file to be cp1252 encoded (see
        # http://en.wikipedia.org/wiki/Windows-1252)
        iFile = open(filename, "r", encoding = self.encoding)
        lineNumber = 0
        while 1:
            lineNumber = lineNumber + 1
            line = iFile.readline()
            if line == "":
                # EOF
                break
            else:
                if lineNumber == 1:
                    # TODO: deal with header
                    # ignore header for now
                    print(line[:-1])
                    ##pass
                else:
                    print(line[:-1])
                    words = line[:-1].split(self.delimiter)
                    print(words)
                    date = self.convertDate(words[2])
                    print(date)
                    who = words[5]
                    print(who)
        iFile.close()

    def convertDate(self, date):
        words = date.split('"') # get rid of the enclosing '"'
        words = words[1].split('.')
        day = words[0]
        month = words[1]
        year = "20%s" % words[2]
        date = "%s-%s-%s" % (year, month, day)
        return date

class HSBC(Bank):
    def __init__(self):
        args = [self]
        Bank.__init__(*tuple(args))
        # TODO: bank specific members
        self.encoding = "utf8"
        self.delimiter = ','

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
        for word in words:
            filename = str(word, encoding='utf8')
            bank.readCsvFile(filename)
        sys.exit()
    else:
        print("TODO: HSBC")
    # HSBC
    for word in words:
        print("reading \"%s\" ..." % str(word, encoding = 'utf8'))
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
