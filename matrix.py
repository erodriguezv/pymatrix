#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import fcntl
import termios
import struct
import random
import signal
import time

# CONFIGS #########################

density = 0.1
chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '~', ':', '"', '?', 'ｱ', 'ｲ', 'ｳ', 'ｴ', 'ｵ', 'ｶ', 'ｷ', 'ｸ', 'ｹ', 'ｺ', 'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ', 'ﾀ', 'ﾁ', 'ﾂ', 'ﾃ', 'ﾄ', 'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ', 'ﾉ', 'ﾊ', 'ﾋ', 'ﾌ', 'ﾍ', 'ﾎ', 'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ', 'ﾔ', 'ﾕ', 'ﾖ', 'ﾗ', 'ﾘ', 'ﾙ', 'ﾚ', 'ﾛ', 'ﾜ', 'ﾝ', '𐌀', '𐌁', '𐌂', '𐌃', '𐌄', '𐌅', '𐌆', '𐌇', '𐌈', 'Θ', '𐌉', '𐌊', '𐌋', '𐌌', '𐌍', '𐌎', 'Ξ', '𐌏', '𐌐', '𐌑', '𐌒', 'Φ', '𐌓', '𐌔', '𐌕', '𐌖', '𐌗', '𐌘', '𐌙', '𐌚', 'Ψ', ' ', ' ', ' ', ' ', ' ']

###################################


def clear():
    """Clear screen, return cursor to top left"""
    sys.stdout.write('\033[2J')  # clear
    sys.stdout.write('\033[H')  # top
    sys.stdout.flush()


def bold(msg):
    return u'\033[1m%s\033[0m' % msg


def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df\033[7m%s\033[0m\x1b8" % (x, y, text)) # bold
     sys.stdout.flush()
     time.sleep(random.uniform(0.001, 0.004))  # wait from 1 to 4 ms
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()


def signal_handler(signal, frame):
        clear()
        sys.exit(0)


def generate_size_params():
    lines, cols = struct.unpack('hh',  fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '9999'))
    # print('Terminal is %d lines high by %d chars wide' % (lines, cols))
    number_of_cols = int(cols * density)
    # print "number of cols for density {}: {}".format(density, number_of_cols)
    random_strings = {}
    for i in range(0, number_of_cols):
        random_strings[i] = sorted(chars, key=lambda x: random.random())
    return lines, cols, number_of_cols, random_strings


signal.signal(signal.SIGINT, signal_handler)
clear()

lines, cols, number_of_cols, random_strings = generate_size_params()

while True:
    lines, cols, number_of_cols, random_strings = generate_size_params()
    # random start positions
    random_start = {}
    for i in range(0, number_of_cols):
        random_start[i] = [random.randint(0, lines), random.randint(0, cols)]
    while random_start[0][0] < lines or random_start[1][0] < lines:
        for s_ptr in random_start:  # for each chain string to print
            l = random_start[s_ptr][0]
            c = random_start[s_ptr][1]
            if random_start[s_ptr][0] < lines:
                print_there(l, c, random_strings[s_ptr][l])
                sys.stdout.flush()
            random_start[s_ptr][0] = l + 1
    print_there(lines, 0, "\n")
    sys.stdout.flush()
