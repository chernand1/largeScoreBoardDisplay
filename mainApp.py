#!/usr/bin/env python3

import time

from largeDigitLib import largeDigitLib

myLargeDigit = largeDigitLib(2)

#while(1):

for i in range (99, 0, -1):
    myLargeDigit.write_string(str('%1.1f' % (i*0.1)))
    print(str('%1.1f' % (i*0.1)))
    time.sleep(0.1)
    #print(i)

myLargeDigit.write_string("1.2.")
time.sleep(5)
myLargeDigit.write_string("4.5")
time.sleep(5)

'''
for i in range(0, 10):
    #myLargeDigit.write_char("B", 1, True)
    #myLargeDigit.write_char(i, 2, False)
    myLargeDigit.chasser_digit()
    #time.sleep(1)
'''

#myLargeDigit.chasser_digit()

myLargeDigit.write_char("off", 1, False)
myLargeDigit.write_char("off", 2, False)

