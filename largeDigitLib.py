#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

class largeDigitLib:
    #  -  A
    # | | F / B
    #  -  G
    # | | E / C
    #  -. D / DP

    # define a  1<<7 10000000 A
    # define b  1<<1 00000010 B
    # define c  1<<2 00000100 C
    # define d  1<<3 00001000 D
    # define e  1<<4 00010000 E
    # define f  1<<6 01000000 F
    # define g  1<<5 00100000 G
    # define dp 1<<0 00000001 DP

    digit_to_segment = {"off": 0b00000000, "0": 0b11011110, "1": 0b00000110, "2": 0b10111010, "3": 0b10101110, "4": 0b01100110,
                        "5": 0b11101100, "6": 0b11111100, "7": 0b10000110, "8": 0b11111110, "9": 0b11101110, "A": 0b11110110,
                        "B": 0b01111100, "C": 0b00111000, "D": 0b00111110, "E": 0b11111000, "F": 0b11110000}

    digit_elements = [0, 1<<3, 1<<4, 1<<6, 1<<7, 1<<1, 1<<2, 1<<5, 1]

    '''
    digit_to_segment = [
        0b11011110, # 0
        0b00000110, # 1
        0b10111010, # 2
        0b10101110, # 3
        0b01100110, # 4
        0b11101100, # 5
        0b11111100, # 6
        0b10000110, # 7
        0b11111110, # 8
        0b11101110, # 9
        0b11110110, # A
        0b01111100, # b
        0b00111000, # C
        0b00111110, # d
        0b11111000, # E
        0b11110000  # F
        ]
    '''

    def __init__(self, numdigits, pin_io_clk=22, pin_io_ser=24, pin_io_lat=23):
        self.numdigits = numdigits
        self.clk = pin_io_clk
        self.ser = pin_io_ser
        self.lat = pin_io_lat
        self.num_digits = numdigits
        self.digit_array = []
        self.dot_array = []

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.ser, GPIO.OUT)
        GPIO.setup(self.lat, GPIO.OUT)

        GPIO.output(self.clk, GPIO.LOW)
        GPIO.output(self.ser, GPIO.LOW)
        GPIO.output(self.lat, GPIO.LOW)

        for digit in range(numdigits):
            self.digit_array.append("off")
            self.dot_array.append("off")
            self.write_char("off", digit, False)

    def write_char(self, number, position, dot=False):

        self.digit_array[position-1] = number
        if dot == False:
            self.dot_array[position-1] = False
        else:
            self.dot_array[position - 1] = True

        GPIO.setup(self.lat, GPIO.OUT)
        GPIO.output(self.lat, GPIO.LOW)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.output(self.clk, GPIO.LOW)
        #time.sleep(0.01)
        GPIO.output(self.lat, GPIO.LOW)

        for num in self.digit_array:
            segments = self.digit_to_segment[str(num)]
            current_dot = self.dot_array[self.digit_array.index(num)]

            for digit in range(0, 8):
                GPIO.setup(self.clk, GPIO.OUT)
                GPIO.output(self.clk, GPIO.LOW)
                #time.sleep(0.01)
                if ((segments >> digit) & 0x1) == 0x1:
                    GPIO.setup(self.ser, GPIO.IN)
                else:
                    GPIO.setup(self.ser, GPIO.OUT)
                    GPIO.output(self.ser, GPIO.LOW)
                if (digit == 0) and (current_dot == True):
                    GPIO.setup(self.ser, GPIO.IN)

                GPIO.setup(self.clk, GPIO.IN)
                #time.sleep(0.01)

        #time.sleep(0.01)
        GPIO.output(self.lat, GPIO.LOW)
        #time.sleep(0.01)
        GPIO.setup(self.lat, GPIO.IN)
        #time.sleep(0.01)
        GPIO.setup(self.lat, GPIO.OUT)
        GPIO.output(self.lat, GPIO.LOW)

    def write_string(self, string):

        char_index = 0
        num_index = self.num_digits
        dot = False

        for charac in string:
            if char_index + 1 < len(string):
                if string[char_index + 1] == ".":
                    dot = True
            if charac != ".":
                self.write_char(charac, num_index, dot)
                num_index = num_index - 1
                dot = False

            if num_index == 0:
                break

            char_index = char_index + 1

    def chasser_digit(self):

        GPIO.setup(self.lat, GPIO.OUT)
        GPIO.output(self.lat, GPIO.LOW)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.output(self.clk, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self.lat, GPIO.LOW)

        for cycle in range (1, 9):
            for num in self.digit_array:
                segments = self.digit_elements[cycle]

                for digit in range(0, 8):
                    GPIO.setup(self.clk, GPIO.OUT)
                    GPIO.output(self.clk, GPIO.LOW)
                    if ((segments >> digit) & 0x1) == 0x1:
                        GPIO.setup(self.ser, GPIO.IN)
                    else:
                        GPIO.setup(self.ser, GPIO.OUT)
                        GPIO.output(self.ser, GPIO.LOW)

                    GPIO.setup(self.clk, GPIO.IN)

            GPIO.output(self.lat, GPIO.LOW)
            GPIO.setup(self.lat, GPIO.IN)
            GPIO.setup(self.lat, GPIO.OUT)
            GPIO.output(self.lat, GPIO.LOW)
            time.sleep(0.05)
