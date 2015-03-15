#!/usr/bin/env python

import os
import csv
import sys
import inspect

def usage():
    print('usage: python %s ' % inspect.getfile(usage) +
          'filename.csv')

class Booking:
    def __init__(self, date, recipient, booking_text, amount):
        self.date = date
        self.recipient = recipient
        self.booking_text = booking_text
        self.amount = amount

    def printIndented(self, len_recipient, len_booking_text, len_amount):
        print("| %s | %s%s | %s%s | %s%s |" %
              (self.date,
               self.recipient,
               ' ' * (len_recipient - len(self.recipient)),
               self.booking_text,
               ' ' * (len_booking_text - len(self.booking_text)),
               ' ' * (len_amount - len(self.amount)),
               self.amount))
        
class GLS:
    def __init__(self):
        # has_header
        sample = open('sample.csv', 'r')
        self.has_header = csv.Sniffer().has_header(sample.read())
        sample.close()
        # dialect
        sample = open('sample.csv', 'r')
        self.dialect = csv.Sniffer().sniff(sample.read())
        sample.close()

    def read(self, filename):
        bookings = []
        len_recipient = 0
        len_booking_text = 0
        len_amount = 0
        # extract info from filename
        basename = os.path.basename(filename)
        year, month, path = basename.split('_')
        root, ext = os.path.splitext(path)
        account_number = root[len('KTO'):]
        # read CSV file
        iFile = open(filename, 'r')
        reader = csv.DictReader(iFile, dialect = self.dialect)
        for row in reader:
            # check account number
            if row['Kontonummer'] != account_number:
                print(row['Kontonummer'])
            # check booking date
            date = row['Buchungstag']
            bday, bmonth, byear = date.split('.')
            if bmonth != month or byear != year:
                print(bday, bmonth, byear)
            # recipient
            recipient = row['Auftraggeber/Empf\xe4nger']
            if len(recipient) > len_recipient:
                len_recipient = len(recipient)
            # booking text
            booking_text = row['Buchungstext']
            if len(booking_text) > len_booking_text:
                len_booking_text = len(booking_text)
            # check value date
            date = row['Wertstellung']
            vday, vmonth, vyear = date.split('.')
            if vday != bday or vmonth != bmonth or vyear != byear:
                if recipient:
                    print('[WARNING] booking date: %04d-%02d-%02d != value date: %04d-%02d-%02d | %s' %
                          (int(byear), int(bmonth), int(bday),
                           int(vyear), int(vmonth), int(vday),
                           recipient))
                else:
                    print('[WARNING] booking date: %04d-%02d-%02d != value date: %04d-%02d-%02d | %s' %
                          (int(byear), int(bmonth), int(bday),
                           int(vyear), int(vmonth), int(vday),
                           booking_text))
            # amount
            amount = row['Betrag']
            amount = amount.replace('.', '')
            amount = amount.replace(',', '.')
            if len(amount) > len_amount:
                len_amount = len(amount)
            # date
            date = "%04d-%02d-%02d" % (int(byear), int(bmonth), int(bday))
            # booking
            booking = Booking(date, recipient, booking_text, amount)
            bookings.append(booking)
        iFile.close()
        ## print(reader.fieldnames)
        bookings.reverse()
        print('%s%s%s' % ('/',
                          '-' * (len(date) + len_recipient + len_booking_text + len_amount + 11),
                          '\\'))
        sum = 0.0
        for booking in bookings:
            booking.printIndented(len_recipient, len_booking_text, len_amount)
            sum += float(booking.amount)
        print('%s%s%s' % ('\\',
                          '-' * (len(date) + len_recipient + len_booking_text + len_amount + 11),
                          '/'))
        print('%s%s' % (' ' * (len(date) + len_recipient + len_booking_text + 11 +
                               len_amount - len("%s" % sum)), sum))
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        exit()
    else:
        filename = sys.argv[1]
    gls = GLS()
    gls.read(filename)
    
