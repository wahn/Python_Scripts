#!/opt/local/bin/python3.2

import csv
import sys
import math
import argparse
import subprocess

class Bank: # interface
    def __init__(self, args):
        self.filenames = []
        self.encoding = "utf8"
        self.delimiter = ','
        self.dates = {}
        self.whos = {}
        self.balance = 0.0
        self.currency = "Euro"
        self.args = args

    def readCsvFile(self, filename):
        print("TODO: %s has to implement readCsvFile(...)" % self.__class__)

    def convertAmount(self, amount):
        print("TODO: %s has to implement convertAmount(...)" % self.__class__)
        return None

    def convertDate(self, date):
        print("TODO: %s has to implement convertDate(...)" % self.__class__)
        return None

    def printInfo(self):
        # (see http://www.termsys.demon.co.uk/vtansi.htm#colors)
        bright = 1
        red = 31
        green = 32
        yellow = 33
        cyan = 36
        # formating
        len_date = len("YYYY-MM-DD")
        len_amount = len("-1234.12")
        len_space = len(" ")
        len_fill = 0   # varies
        len_amount = 0 # varies
        len_currency = len(self.currency)
        # print the collected data with color and formatting
        keys = list(self.dates.keys())
        keys.sort()
        for date in keys:
            for who_amount in self.dates[date]:
                who, amount = who_amount
                amount = float(amount)
                self.balance += amount
                len_amount = len(str("%.2f" % amount))
                if args.use_no_colors:
                    amount = "%.2f" % amount
                else:
                    if amount < 0.0:
                        amount = "\033[%s;%sm%.2f\033[0m" % (bright, red, 
                                                             amount)
                    else:
                        amount = "\033[%s;%sm%.2f\033[0m" % (bright, green, 
                                                             amount)
                len_fill = (79 - len_date - 2 * len_space - len(who) - 
                            len_amount)
                if (len_fill < 0):
                    who = who[:len_fill]
                fill = " " * len_fill
                if args.use_no_colors:
                    date = "%s" % date
                else:
                    date = "\033[%s;%sm%s\033[0m" % (bright, yellow, date)
                print("%s %s%s %s" % (date, who, fill, amount))
        print("-" * 79)
        self.balance = self.balance * 100.0 # cent
        self.balance = math.floor(self.balance + 0.5)
        self.balance = self.balance / 100.0 # euro
        len_amount = len(str(self.balance))
        if args.use_no_colors:
            self.balance = "%s" % self.balance
        else:
            if self.balance < 0.0:
                self.balance = "\033[%s;%sm%s\033[0m" % (bright, red, 
                                                         self.balance)
            else:
                self.balance = "\033[%s;%sm%s\033[0m" % (bright, green, 
                                                         self.balance)
        len_fill = 79 - len_date - 2 * len_space - len_amount - len_currency
        fill = " " * len_fill
        if args.use_no_colors:
            cyan_currency = "%s" % self.currency
        else:
            cyan_currency = "\033[%s;%sm%s\033[0m" % (bright, cyan, 
                                                      self.currency)
        print("%s %s%s %s" % (date, fill, cyan_currency, self.balance))

class Sparkasse(Bank):
    def __init__(self, cmd_line_args):
        args = [self, cmd_line_args]
        Bank.__init__(*tuple(args))
        # bank specific members
        self.currency = "Euro"
        self.encoding = "cp1252"
        self.delimiter = ';'
        # Kontostand am 07.10.2011 **: 2.190,48 EUR
        self.dates["2011-10-07"] = [["KONTOSTAND", 2190.48]]

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
                    pass
                else:
                    words = line[:-1].split(self.delimiter)
                    date = self.convertDate(words[2])
                    who = words[5][1:-1] # get rid of the enclosing '"'
                    if who == "":
                        who = "%s %s" % (words[3][1:-1], words[4][1:-1])
                    amount = self.convertAmount(words[8])
                    try:
                        self.dates[date].append([who, amount])
                    except KeyError:
                        self.dates[date] = [[who, amount]]
                    try:
                        self.whos[who].append([who, amount])
                    except KeyError:
                        self.whos[who] = [[who, amount]]
        iFile.close()

    def convertAmount(self, amount):
        words = amount.split('"') # get rid of the enclosing '"'
        words = words[1].split(',')
        amount = '.'.join(words)
        return amount

    def convertDate(self, date):
        words = date.split('"') # get rid of the enclosing '"'
        words = words[1].split('.')
        day = words[0]
        month = words[1]
        year = "20%s" % words[2]
        date = "%s-%s-%s" % (year, month, day)
        return date

class HSBC(Bank):
    def __init__(self, cmd_line_args):
        args = [self, cmd_line_args]
        Bank.__init__(*tuple(args))
        # TODO: bank specific members
        self.currency = "GBP"
        self.encoding = "utf8"
        self.delimiter = ','

    def readCsvFile(self, filename):
        print("reading \"%s\" ..." % filename)
        # we assume the CSV file to be utf8 encoded (see
        # http://en.wikipedia.org/wiki/UTF-8)
        iFile = open(filename, "r", encoding = self.encoding)
        lineNumber = 0
        while 1:
            lineNumber = lineNumber + 1
            line = iFile.readline()
            if line == "":
                # EOF
                break
            else:
                words = line[:-1].split(self.delimiter)
                if len(words) != 3:
                    # repair lines which use delimiter in the middle word
                    newWords = [words[0],
                                self.delimiter.join(words[1:-1]),
                                words[-1]]
                    words = newWords
                date = self.convertDate(words[0])
                who = words[1]
                amount = self.convertAmount(words[2])
                try:
                    self.dates[date].append([who, amount])
                except KeyError:
                    self.dates[date] = [[who, amount]]
                try:
                    self.whos[who].append([who, amount])
                except KeyError:
                    self.whos[who] = [[who, amount]]
        iFile.close()

    def convertAmount(self, amount):
        return amount

    def convertDate(self, date):
        return date

def checkBank(filename, args):
    bank = None
    iFile = open(filename, "r")
    try:
        line = iFile.readline()
    except UnicodeDecodeError:
        bank = Sparkasse(args)
        iFile.close()
    else:
        bank = HSBC(args)
        iFile.close()
    return bank

if __name__ == "__main__":
    # deal with arguments
    description = ('Read some CSV files and print useful information ' +
                   'read from them.')
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument('-nc', dest = 'use_no_colors', 
                        action = 'store_true', 
                        help = 'use no colors ' +
                        '(the default is to use colors during printing)')
    args = parser.parse_args()
    print("use_no_colors = %s" % args.use_no_colors)
    # collect info here
    dates = {}
    whos = {}
    balance = 0.0
    # list CSV files
    byte_string = subprocess.check_output("ls *.csv", shell = True)
    words = byte_string.split()
    # check which bank we are using
    bank = checkBank(words[0], args)
    if bank.__class__ == Sparkasse:
        for word in words:
            filename = str(word, encoding='utf8')
            bank.readCsvFile(filename)
        bank.printInfo()
    elif bank.__class__ == HSBC:
        for word in words:
            filename = str(word, encoding='utf8')
            bank.readCsvFile(filename)
        bank.printInfo()
    else:
        print("TODO: bank.__class__")
