#
# Chisel Reverse tunnel Configuration Script
# Author: github.com/Azumi67
# This is for educational use and my own learning, please provide me with feedback if possible
# This script is designed to simplify the configuration of Chisel Direct Tunnel.
#
# Supported operating systems: Ubuntu 20, Debian 12
## I use the same imports and other stuff to speed up in creating the script
# you should only install colorama & netifaces
# Usage:
#   Run the script with root privileges.
#   Follow the on-screen prompts to install, configure, or uninstall the tunnel.
#
#
# Disclaimer:
# This script comes with no warranties or guarantees. Use it at your own risk.
import sys
import os
import time
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import random
import string
import shutil
import netifaces as ni
import urllib.request
import zipfile
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')

if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)


def display_progress(total, current):
    width = 40
    percentage = current * 100 // total
    completed = width * current // total
    remaining = width - completed

    print('\r[' + '=' * completed + '>' + ' ' * remaining + '] %d%%' % percentage, end='')


def display_checkmark(message):
    print('\u2714 ' + message)


def display_error(message):
    print('\u2718 Error: ' + message)


def display_notification(message):
    print('\u2728 ' + message)


def display_loading():
    duration = 3
    end_time = time.time() + duration
    ball_width = 10
    ball_position = 0
    ball_direction = 1

    while time.time() < end_time:
        sys.stdout.write('\r\033[93mLoading, Please wait... [' + ' ' * ball_position + 'o' + ' ' * (ball_width - ball_position - 1) + ']')
        sys.stdout.flush()

        if ball_position == 0:
            ball_direction = 1
        elif ball_position == ball_width - 1:
            ball_direction = -1

        ball_position += ball_direction
        time.sleep(0.1)
    
    sys.stdout.write('\r' + ' ' * (len('Loading, Please wait...') + ball_width + 4) + '\r')
    sys.stdout.flush()
    display_notification("\033[96mIt might take a while...\033[0m")

    
def display_logo2():
    colorama.init()
    logo2 = colorama.Style.BRIGHT + colorama.Fore.GREEN + """
     _____       _     _      
    / ____|     (_)   | |     
   | |  __ _   _ _  __| | ___ 
   | | |_ | | | | |/ _` |/ _ \\
   | |__| | |_| | | (_| |  __/
    \_____|\__,_|_|\__,_|\___|
""" + colorama.Style.RESET_ALL
    print(logo2)
    
def display_logo():
    colorama.init()  
    logo = """ 
\033[1;96m          
                 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⠤⠒⠊⠉⠀⠀⠀⠀⠈⠁⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀\033[1;93m⠀⢀⠔⠉⠀⠀⠀⠀⢀⡠⠤⠐⠒⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⣀⡠⠤⠤⠀⠀⠂⠐\033[1;96m⠀⠠⢤⠎⢑⡭⣽⣳⠶⣖⡶⣤⣖⣬⡽⡭⣥⣄\033[1;93m⠒⠒⠀⠐⠁⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢀⠴⠊⠁⠀⠀⠀⠀⡀⠀\033[1;96m⣠⣴⡶⣿⢏⡿⣝⡳⢧⡻⣟⡻⣞⠿⣾⡽⣳⣯⣳⣞⡻⣦⡀⠀⠀\033[1;93m⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢨⠀⠀⠀⢀⠤⠂⠁\033[1;96m⢠⣾⡟⣧⠿⣝⣮⣽⢺⣝⣳⡽⣎⢷⣫⡟⡵⡿⣵⢫⡷⣾⢷⣭⢻⣦⡄\033[1;93m⠤⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⡄⠀⠀⠓⠂⠀\033[1;96m⣴⣿⢷⡿⣝⣻⣏⡷⣾⣟⡼⣣⢟⣼⣣⢟⣯⢗⣻⣽⣏⡾⡽⣟⣧⠿⡼⣿⣦\033[1;93m⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠇⠀⠀⠀⠀\033[1;96m⣼⣿⢿⣼⡻⣼⡟⣼⣧⢿⣿⣸⡧⠿⠃⢿⣜⣻⢿⣤⣛⣿⢧⣻⢻⢿⡿⢧⣛⣿⣧⠀\033[1;93m⠛⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢸⠁⠀⠀⠀⠀\033[1;96m⣼⣻⡿⣾⣳⡽⣾⣽⡷⣻⣞⢿⣫⠕⣫⣫⣸⢮⣝⡇⠱⣏⣾⣻⡽⣻⣮⣿⣻⡜⣞⡿⣷\033[1;93m⢀⠀⠀⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⣧⠀⠀⠀\033[1;96m⣼⣳⢯⣿⣗⣿⣏⣿⠆⣟⣿⣵⢛⣵⡿⣿⣏⣟⡾⣜⣻⠀⢻⡖⣷⢳⣏⡶⣻⡧⣟⡼⣻⡽⣇\033[1;93m⠁⠢⡀⠠⡀⠑⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠈⢦⠀\033[1;96m⣰⣯⣟⢯⣿⢾⣹⢾⡟⠰⣏⡾⣾⣟⡷⣿⣻⣽⣷⡶⣟⠿⡆⠀⢻⣝⣯⢷⣹⢧⣿⢧⡻⣽⣳⢽⡀\033[1;93m⠀⠈⠀⠈⠂⡼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⢵\033[1;96m⣟⣾⡟⣾⣿⣻⢽⣺⠇⠀⣿⡱⢿⡞⣵⡳⣭⣿⡜⣿⣭⣻⣷⠲⠤⢿⣾⢯⢯⣛⢿⣳⡝⣾⣿⢭⡇⠀\033[1;93m⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠤⠊⠀\033[1;96m⣼⢻⣿⢞⣯⢿⡽⣸⣹⡆⠀⢷⣏⢯⣿⣧⣛⠶⣯⢿⣽⣷⣧⣛⣦⠀⠀⠙⢿⣳⣽⣿⣣⢟⡶⣿⣫⡇⠀⠀\033[1;93m⠀⠰⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⣠⠖⠁⠀⠀⡄\033[1;96m⡿⣯⣷⣻⡽⣞⡟⣿⣿⣟⠉⠈⢯⣗⣻⣕⢯⣛⡞⣯⢮⣷⣭⡚⠓⠋⠀⠀⠀⠈⠉⣿⡽⣎⠷⡏⡷⣷⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠐⣇⠀⠀⢀⠊\033[1;96m⣼⣇⣿⡗⣿⣽⣷⡿⣿⣱⡿⣆⠀⠀⠙⠒⠛⠓⠋⠉⠉⠀⠀⠀\033[1;91m⢠⣴⣯⣶⣶⣤⡀\033[1;96m ⠀⣿⣟⡼⣛⡇⣟⣿⡆\033[1;93m⡀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⢤⠀⠃⠌\033[1;96m⣸⣿⢾⡽⣹⣾⠹⣞⡵⣳⣽⡽⣖⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;91m⣤⣖⣻⣾⣝⢿⡄\033[1;96m ⢸⣯⢳⣏⡿⣏⣾⢧\033[1;93m⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⠀⠈⠀\033[1;96m⡿⣿⣻⡽⣽⣿⢧⠌⠉\033[1;91m⠉⣴⣿⣿⣫⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣛⠿⠿⢟⢙⡄⠙\033[1;96m ⠘⣯⢳⣞⡟⣯⢾⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀\033[1;96m⡿⣿⣿⢵⣫⣿⣆⠁⠂\033[1;91m⣼⡿⢹⣿⡿⠽⠟⢢⠀⠀⠀⠀⠀⠀⠀⢹⠀⢄⢀⠀⡿⠀⠀\033[1;96m ⢰⣯⢷⣺⣏⣯⢻⡽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⢀⠠\033[1;96m⣿⣿⢾⣛⡶⣽⠈⢓⠀\033[1;91m⢻⠁⢸⠇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠑⠠⠤⠔⠂⠀⠀\033[1;96m ⢸⣿⢮⣽⠿⣜⣻⡝⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠑⠊⠁\033[1;96m⢠⡷⡇⣿⣿⢼⣹⡀⠀⠑⢄⠀\033[1;91m⠀⠃⠌⣁⠦⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀\033[1;96m⢀⣿⢾⡝⣾⡽⣺⢽⣹⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢽⣻⡟⣮⣝⡷⢦⣄⣄⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣯⢿⡺⣟⢷⡹⢾⣷⡞⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⡿⣎⢿⡽⣳⢮⣿⣹⣾⣯⡝⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⣀⣴⡟⣿⢧⣏⢷⡟⣮⠝⢿⣹⣯⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⡷⣏⣾⡳⣽⢺⣷⡹⣟⢶⡹⣾⡽⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⣾⢯⣷⡇⣿⢳⣎⢿⡞⣽⢦⣼⡽⣧⢻⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⢾⡷⣭⣿⢳⣭⢻⣷⡻⣜⣻⡵⣻⡼⣿⠾⠫\033[1;96m⣽⣟⣶⣶⣶⠒⠒⠂⠉⠀\033[1;96m⢸⣽⢺⡷⣷⣯⢗⣮⣟⢾⢧⣻⠼⡿⣿⢣⡟⣼⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣝⣾⢳⢧⣟⡳⣎⣿⣿⣱⢏⣾⣽⣳⠟\033[1;92m⠁⠀⡌⠈\033[1;96m⢹⡯⠟⠛⠀⠀⠀⠀⠀⠈\033[1;96m⣷⢻⣼⣽⣿⡾⣼⣏⣾⣻⡜⣯⣷⢿⣟⣼⡳⣞⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢿⡸⣎⠿⣾⡏⣷⣉⣷⣿⢹⣎⡿\033[1;92m⠎⡎⠀⠀⠀⡇⠀⣾⠱⡀⠀⠀⠀⠀⠀⠀⠀⠈⣹⠉⡏⠀\033[1;96m⠹⣾⣏⢹⣶⢹⣶⢿⡾⣿⢶⣿⣸⠾⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⢫⣞⡽⣯⢿⣹⡟⣶⣹⢷⣻\033[1;92m⡷⠊⠀⡜⠀⠀⠀⠀⢱⠀⣿⡀⠈⠢⢀⣀⣀⠠⠄⠒⢈⡏⡰⠀⠀⠀\033[1;96m⠀⣿⡜⣮⢟⡼⣻⡵⣻⣗⠾⣟⣯⢻⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⢣⣟⡾⣽⣯⢳⣿⡹⣖⣿⡳\033[1;92m⠋⠀⠀⡸⠀⠀⠀⠀⠀⢸⠀⢺⢂⠀⠀⠀⠀⠀⠀⠀⢠⡺⡱⠁⠀⠀⠀⠀\033[1;96m⢹⣧⣻⢮⡳⣝⡷⢧⣻⢯⢿⣻⣳⢞⡆⠀⠀⠀
⠀⠀⠀⠀⢀⡾⣽⣣⡿⣼⣏⡿⣼⣳⡯⢷⣹⣯⠇\033[1;92m⠀⠀⢠⠁⠀⠀⠀⠀⠀⠈⡆⠈⢹⡰⠤⡀⠀⠀⠀⢠⡼⢱⠁⠀⠀⠀⠀⠀⠀\033[1;96m⠹⣿⣿⣱⣻⣼⣏⢷⣯⣿⡳⣿⣎⢿⡀⠀⠀
⠀⠀⠀⠀⣾⣽⠷⣿⣵⡿⣼⡟⣭⣷⡟⣿⢯⡏⠀\033[1;92m⠀⠀⠘⠀⠀⠒⠈⢡⠀⠀⢗⢄⠀⠃⠀⠺⢁⢈⠥⠋⣀⠇⠀⠀⠀⠀⠀⠀⡀⠀\033[1;96m⠈⠙⢿⣳⢞⣽⢯⣞⣾⣯⡝⣿⡾⡇⠀⠀\033[1;92mAuthor: github.com/Azumi67  \033[1;96m  ⠀⠀

  \033[96m  ______   \033[1;94m _______  \033[1;92m __    \033[1;93m  _______     \033[1;91m    __      \033[1;96m  _____  ___  
 \033[96m  /    " \  \033[1;94m|   __ "\ \033[1;92m|" \  \033[1;93m  /"      \    \033[1;91m   /""\     \033[1;96m (\"   \|"  \ 
 \033[96m // ____  \ \033[1;94m(. |__) :)\033[1;92m||  |  \033[1;93m|:        |   \033[1;91m  /    \   \033[1;96m  |.\\   \    |
 \033[96m/  /    ) :)\033[1;94m|:  ____/ \033[1;92m|:  |  \033[1;93m|_____/   )   \033[1;91m /' /\  \   \033[1;96m |: \.   \\  |
\033[96m(: (____/ // \033[1;94m(|  /     \033[1;92m|.  | \033[1;93m //       /   \033[1;91m //  __'  \  \033[1;96m |.  \    \ |
 \033[96m\        / \033[1;94m/|__/ \   \033[1;92m/\  |\ \033[1;93m |:  __   \  \033[1;91m /   /  \\   \ \033[1;96m |    \    \|
 \033[96m \"_____ / \033[1;94m(_______) \033[1;92m(__\_|_)\033[1;93m |__|  \___) \033[1;91m(___/    \___) \033[1;96m\___|\____\)
"""
    print(logo)
def main_menu():
    try:
        while True:
            display_logo()
            border = "\033[93m+" + "="*70 + "+\033[0m"
            content = "\033[93m║            ▌║█║▌│║▌│║▌║▌█║ \033[92mMain Menu\033[93m  ▌│║▌║▌│║║▌█║▌                  ║"
            footer = " \033[92m            Join Opiran Telegram \033[34m@https://t.me/OPIranClub\033[0m "

            border_length = len(border) - 2
            centered_content = content.center(border_length)

            print(border)
            print(centered_content)
            print(border)
            

            print(border)
            print(footer)
            print(border)
            print("0. \033[92mStatus Menu\033[0m")
            print("9.\033[94mStop | Restart Service \033[0m")
            print("10.\033[91mUninstall\033[0m")
            print("11.\033[93mEdit \033[92mReset Timer\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            display_notification("\033[93mSingle Server\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            print("1. \033[96mChisel \033[92mTCP \033[96m[IPV4]\033[0m")
            print("2. \033[96mChisel \033[92mUDP \033[96m[IPV4]\033[0m") 
           
            print("3. \033[93mChisel \033[92mTCP\033[93m [IPV6]\033[0m")            
            print("4. \033[93mChisel \033[92mUDP\033[93m [IPV6]\033[0m")
            print(border)
            print("\033[93m─────────────────────────────────────────── \033[0m")
            display_notification("\033[92m[5] \033[96mKharej \033[92m[1] \033[93mIRAN\033[0m")
            print("\033[93m─────────────────────────────────────────── \033[0m")
            print("5. \033[96mChisel \033[92mTCP \033[96m[IPV4] \033[92m[5] \033[96mKHAREJ\033[92m [1] \033[96mIRAN")
            print("\033[97m6. \033[96mChisel \033[92mUDP \033[96m[IPV4] \033[92m[5] \033[96mKHAREJ\033[92m [1] \033[96mIRAN")
            
            print("\033[97m7. \033[93mChisel \033[92mTCP \033[93m[IPV6] \033[92m[5] \033[93mKHAREJ\033[92m [1] \033[93mIRAN")
            print("\033[97m8. \033[93mChisel \033[92mUDP \033[93m[IPV6] \033[92m[5] \033[93mKHAREJ\033[92m [1] \033[93mIRAN")
            print(border)               
            print("q. Exit")
            print("\033[93m╰─────────────────────────────────────────────────────────────────────╯\033[0m")

            choice = input("\033[5mEnter your choice Please: \033[0m")
            
            if choice == '0':
                chisel_status()
            elif choice == '1':
                chisel_tcp_ip4()
            elif choice == '2':
                chisel_udp_ip4()
            elif choice == '3':
                chisel_tcp_ip6()
            elif choice == '4':
                chisel_udp_ip6()
            elif choice == '5':
                kharej5_t()
            elif choice == '6':
                kharej5_u()
            elif choice == '7':
                kharej5_t6()
            elif choice == '8':
                kharej5_u6()
            elif choice == '9':
                start_serv()
            elif choice == '10':
                uni_menu() 
            elif choice == '11':
                timez()
            elif choice == 'q':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        display_error("\033[91m\nProgram interrupted. Exiting...\033[0m")
        sys.exit()
 
def timez():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mReset Timer\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mHour \033[0m')
    print('2. \033[92mMinutes \033[0m')
    print('0. \033[34mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hourz()
            break
        elif server_type == '2':
            minutes()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 
            
def hourz():
   
    hours = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in hours]:\033[0m "))
    delete_cron()
    delete_cron2()

    if hours == 1:
        cron_entry = "0 * * * * /etc/reschiseld.sh"
    else:
        cron_entry = f"0 */{hours} * * * /etc/reschiseld.sh"

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        display_checkmark("\033[92mCron entry added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")

def minutes():
    minutes = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in minutes]:\033[0m "))
    delete_cron()
    delete_cron2()

    cron_entry = f"*/{minutes} * * * * /etc/reschiseld.sh"

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        display_checkmark("\033[92mCron entry added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")
        
def kharej5_t():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV4 \033[92mTCP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4()
            break
        elif server_type == '2':
            kharej_ipv4()
            break
        elif server_type == '3':
            kharej_ipv4()
            break
        elif server_type == '4':
            kharej_ipv4()
            break
        elif server_type == '5':
            kharej_ipv4()
            break
        elif server_type == '6':
            iran_ipv4()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def kharej5_t6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV6 \033[92mTCP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6()
            break
        elif server_type == '2':
            kharej_ipv6()
            break
        elif server_type == '3':
            kharej_ipv6()
        elif server_type == '4':
            kharej_ipv6()
            break
        elif server_type == '5':
            kharej_ipv6()
            break
        elif server_type == '6':
            iran_ipv6()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def kharej5_u():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV4 \033[92mUDP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4_udp()
            break
        elif server_type == '2':
            kharej_ipv4_udp()
            break
        elif server_type == '3':
            kharej_ipv4_udp()
            break
        elif server_type == '4':
            kharej_ipv4_udp()
            break
        elif server_type == '5':
            kharej_ipv4_udp()
            break
        elif server_type == '6':
            iran_ipv4_udp()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def kharej5_u6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mKharej \033[93mIPV6 \033[92mUDP\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mKharej\033[92m [1] \033[0m')
    print('2. \033[93mKharej\033[92m [2] \033[0m')
    print('3. \033[93mKharej\033[92m [3] \033[0m')
    print('4. \033[93mKharej\033[92m [4] \033[0m')
    print('5. \033[93mKharej\033[92m [5] \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[96mIRAN \033[0m')
    print('0. \033[92mBack to main menu \033[0m')

    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6_udp()
            break
        elif server_type == '2':
            kharej_ipv6_udp()
            break
        elif server_type == '3':
            kharej_ipv6_udp()
            break
        elif server_type == '4':
            kharej_ipv6_udp()
            break
        elif server_type == '5':
            kharej_ipv6_udp()
            break
        elif server_type == '6':
            iran_ipv6_udp()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
            

         
        
def chisel_tcp_ip4():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mTCP\033[96m IPV4\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4()
            break
        elif server_type == '2':
            iran_ipv41()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')      
            
def iran_tcp1(config_number, kharej_ipv4, kharej_port, tunnel_port=443):
    service_name = f"irand_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s {kharej_ipv4}:{tunnel_port} localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=IRAN Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mIRAN service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}. Error: {}\033[0m".format(config_number, e.output))
        

        
def iran_ipv41():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    kharej_ipv4 = input("\033[93mEnter \033[92mKharej\033[96m IPV4\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m") or "443"
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m: \033[0m")
        server_ports.append(kharej_port)

        iran_tcp1(i, kharej_ipv4, kharej_port, tunnel_port)
    res_chisel1()
    current_ipv4 = get_ipv4()
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
    
def chisel_udp_ip4():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mUDP\033[96m IPV4\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv4_udp()
            break
        elif server_type == '2':
            iran_ipv41_udp()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')                 

def iran1_udp(config_number, kharej_ipv4, kharej_port, tunnel_port=443):
    service_name = f"irand_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s {kharej_ipv4}:{tunnel_port} localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mIRAN service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}. Error: {}\033[0m".format(config_number, e.output))
        

def iran_ipv41_udp():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
        
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKHAREJ\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    kharej_ipv4 = input("\033[93mEnter \033[92mKharej\033[96m IPV4 \033[93maddress: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel\033[96m port\033[93m : \033[0m") or "443"
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port \033[93m[UDP]: \033[0m")
        server_ports.append(kharej_port)

        iran1_udp(i, kharej_ipv4, kharej_port, tunnel_port)
    res_chisel1()
    current_ipv4 = get_ipv4()
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
    
def chisel_tcp_ip6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mTCP\033[96m IPV6\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6()
            break
        elif server_type == '2':
            iran_ipv61()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')   

def iran_tcp21(config_number, kharej_ipv6, kharej_port, tunnel_port=443):
    service_name = f"irand_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s [{kharej_ipv6}]:{tunnel_port} localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=IRAN Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mIRAN service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}. Error: {}\033[0m".format(config_number, e.output))


def iran_ipv61():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port: \033[0m") or '443'
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m") 
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m: \033[0m")
        server_ports.append(kharej_port)

        iran_tcp21(i, kharej_ipv6, kharej_port, tunnel_port)
    res_chisel1()
    current_ipv4 = get_ipv4()
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports        
    
def chisel_udp_ip6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Chisel \033[92mUDP\033[96m IPV6\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipv6_udp()
            break
        elif server_type == '2':
            iran_ipv61_udp()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 
            
def iran_ud61(config_number, kharej_ipv6, kharej_port, tunnel_port):
    service_name = f"irand_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s [{kharej_ipv6}]:{tunnel_port} localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=IRAN Service {config_number} - Server {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
        display_checkmark("\033[92mIRAN service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}/{}. Error: {}\033[0m".format(config_number, e.output))
def iran_ipv61_udp():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")

    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej\033[93m Configs: \033[0m"))
    kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel Port: \033[0m") or '443'
    server_ports = []

    for i in range(1, num_configs + 1):
        print("\033[93m────────────────────────\033[0m")
        print("\033[92m    --- Config {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")
        kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m: \033[0m")
        server_ports.append(kharej_port)

        iran_ud61(i, kharej_ipv6, kharej_port, tunnel_port)  

    res_chisel1()
    current_ipv4 = get_ipv4()
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    for i in range(num_configs):
        print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return server_ports
            
def forward():

    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])
       
    with open('/etc/resolv.conf', 'a') as f:
        f.write("nameserver 1.1.1.1\n")

    
def chisel_mnu():
    def stop_loading():
        display_error("\033[91mInstallation process interrupted..\033[0m")
        exit(1)

    arch = subprocess.check_output('uname -m', shell=True).decode().strip()

    if arch in ['x86_64', 'amd64']:
        chisel_download_url = "https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_linux_amd64.gz"
        chisel_directory_name = "chisel"
    elif arch in ['aarch64', 'arm64']:
        chisel_download_url = "https://github.com/jpillora/chisel/releases/download/v1.9.1/chisel_1.9.1_linux_arm64.gz"
        chisel_directory_name = "chisel"
    else:
        display_error("\033[91mUnsupported CPU architecture: {}\033[0m".format(arch))
        return

    display_loading()

    display_notification("\033[93mDownloading Chisel...\033[0m")
    download_result = subprocess.run(f"wget --quiet --show-progress {chisel_download_url} -O {chisel_directory_name}.gz", shell=True)
    if download_result.returncode != 0:
        display_error("\033[91mChisel download failed.\033[0m")
        return

    gunzip_result = subprocess.run(f"gunzip {chisel_directory_name}.gz", shell=True)
    if gunzip_result.returncode != 0:
        display_error("\033[91mFailed to extract !!\033[0m")
        return

    try:
        os.rename(chisel_directory_name, "chisel")
        subprocess.run(f"chmod +x chisel", shell=True)
    except Exception as e:
        display_error("\033[91mError occurred during Chisel installation: {}\033[0m".format(str(e)))
        return

    display_checkmark("\033[92mDownload Completed!\033[0m")
    
def chisel_key(key_path):
    keygen_command = f"./chisel server --keygen {key_path}"
    try:
        subprocess.run(keygen_command, shell=True, check=True)
        display_notification("\033[93mChisel key generated at {}\033[0m".format(key_path))

    except subprocess.CalledProcessError as e:
        display_notification("\033[91mFailed to generate key. Error: {}\033[0m".format(e.output))

def kharej_tcp(host, key_path, port=443):
    service_name = "kharejd_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --port {port} --host {host} --keepalive 10s"

    service_content = f"""[Unit]
Description=Chisel Service kharej
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mKharej service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service. Error: {}\033[0m".format(e.output))
      

def kharej_ipv4():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKharej\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel2()

    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)  
            except NotADirectoryError:
                os.remove(key_directory)  
    except Exception as e:
       display_error("An error occurred while removing: {}".format(str(e)))

    host = input("\033[93mEnter \033[92mKharej\033[96m IPV4\033[93m address: \033[0m")
    port = input("\033[93mEnter  \033[92mTunnel Port \033[93m : \033[0m") or '443'

    try:
        os.makedirs(key_directory, exist_ok=True) 
        print("\033[93m────────────────────────\033[0m")        

        key_path = f"{key_directory}/chisel_key_1.key"

        chisel_key(key_path)
        kharej_tcp(host, key_path, int(port))
    except Exception as e:
         display_error("An error occurred: {}".format(str(e)))
    
def get_ipv4():
    interfaces = ni.interfaces()
    for interface in interfaces:
        if interface.startswith('eth') or interface.startswith('en'):
            try:
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    ipv4 = addresses[ni.AF_INET][0]['addr']
                    return ipv4
            except KeyError:
                pass
    return None
    
def iran_tc4(config_number, server_number, kharej_ipv4, kharej_port, tunnel_port=443):
    service_name = f"irand_{server_number}_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s {kharej_ipv4}:{tunnel_port} localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=Kharej Service {config_number} - Server {server_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
        display_checkmark("\033[92mIRAN service {}/{} started successfully!\033[0m".format(server_number, config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}/{}. Error: {}\033[0m".format(server_number, config_number, e.output))

def iran_ipv4():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel3()
    print("\033[93m───────────────────────────\033[0m")
    num_servers = int(input("\033[93mEnter the number of \033[92mKharej\033[93m servers:\033[0m "))
    server_configs = []

    for i in range(1, num_servers + 1):
        print("\033[93m────────────────────────\033[0m")
        print("\033[92m    --- Server {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")

        num_configs = int(input("\033[93mEnter the \033[92mNumber \033[93mof \033[96mKharej Configs: \033[0m".format(i)))
        kharej_ipv4 = input("\033[93mEnter \033[92mKharej Server {}\033[96m IPV4\033[93m address: \033[0m".format(i))

        configs = []
        for j in range(1, num_configs + 1):
            kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m for config {}: \033[0m".format(j))
            configs.append(kharej_port)

            tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m") or "443"
            iran_tc4(j, i, kharej_ipv4, kharej_port, tunnel_port)
        
        current_ipv4 = get_ipv4()
        print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
        for j, config_port in enumerate(configs, start=1):
            print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
        print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

        server_configs.append((current_ipv4, configs))

    return server_configs
    
def iran_tc(config_number, server_number, kharej_ipv6, kharej_port, tunnel_port=443):
    service_name = f"irand_{server_number}_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s [{kharej_ipv6}]:{tunnel_port} localhost:{kharej_port}"

    service_content = f"""[Unit]
Description=Kharej Service {config_number} - Server {server_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
        display_checkmark("\033[92mIRAN service {}/{} started successfully!\033[0m".format(server_number, config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}/{}. Error: {}\033[0m".format(server_number, config_number, e.output))

def iran_ipv6():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel3()
    print("\033[93m───────────────────────────\033[0m")
    num_servers = int(input("\033[93mEnter the number of \033[92mKharej\033[93m servers:\033[0m "))
    server_configs = []

    for i in range(1, num_servers + 1):
        print("\033[93m────────────────────────\033[0m")
        print("\033[92m    --- Server {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")

        num_configs = int(input("\033[93mEnter the \033[92mNumber \033[93mof \033[96mKharej Configs: \033[0m".format(i)))
        kharej_ipv6 = input("\033[93mEnter \033[92mKharej Server {}\033[96m IPV6\033[93m address: \033[0m".format(i))

        configs = []
        for j in range(1, num_configs + 1):
            kharej_port = input("\033[93mEnter Kharej \033[92mConfig port\033[93m for config {}: \033[0m".format(j))
            configs.append(kharej_port)

            tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m") or "443"
            iran_tc(j, i, kharej_ipv6, kharej_port, tunnel_port)
        
        current_ipv4 = get_ipv4()
        print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
        for j, config_port in enumerate(configs, start=1):
            print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
        print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

        server_configs.append((current_ipv4, configs))

    return server_configs

def iran_ud4(config_number, server_number, kharej_ipv4, kharej_port, tunnel_port):
    service_name = f"irand_{server_number}_{config_number}.service"
    service_file = f"/etc/systemd/system/{service_name}"
    chisel_command = f"./chisel client --keepalive 10s {kharej_ipv4}:{tunnel_port} localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=IRAN Service {config_number} - Server {server_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', service_file], check=True)
        display_checkmark("\033[92mIRAN service {}/{} started successfully!\033[0m".format(server_number, config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}/{}. Error: {}\033[0m".format(server_number, config_number, e.output))


def iran_ipv4_udp():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel3()
    print("\033[93m───────────────────────────\033[0m")
    num_servers = int(input("\033[93mEnter the number of \033[92mKharej\033[93m servers:\033[0m "))
    server_configs = []

    for i in range(1, num_servers + 1):
        print("\033[93m────────────────────────\033[0m")
        print("\033[92m    --- Server {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej configs: \033[0m"))
        kharej_ipv4 = input("\033[93mEnter \033[92mKharej Server {}\033[96m IPV4\033[93m address: \033[0m".format(i))

        configs = []
        for j in range(1, num_configs + 1):
            kharej_port = input("\033[93mEnter \033[96mKharej \033[92mConfig {} port\033[93m: \033[0m".format(j))
            tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m") or "443"

            configs.append(kharej_port)

            iran_ud4(j, i, kharej_ipv4, kharej_port, tunnel_port)

        
        current_ipv4 = get_ipv4()
        print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
        for j, config_port in enumerate(configs, start=1):
            service_name = f"iran_{i}_{j}.service"
            print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
        print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

        server_configs.append((current_ipv4, configs))

    return server_configs

        
def iran_ud6(config_number, server_number, kharej_ipv6, kharej_port, tunnel_port):
    service_name = f"irand_{server_number}_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s [{kharej_ipv6}]:{tunnel_port} R:localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=iran Service {config_number} - Server {server_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
        display_checkmark("\033[92mKharej service {}/{} started successfully!\033[0m".format(server_number, config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}/{}. Error: {}\033[0m".format(server_number, config_number, e.output))


def iran_ipv6_udp():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

        
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mIRAN\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel3()    
    print("\033[93m───────────────────────────\033[0m")
    num_servers = int(input("\033[93mEnter the number of \033[92mKharej\033[93m servers:\033[0m "))
    server_configs = []

    for i in range(1, num_servers + 1):
        print("\033[93m────────────────────────\033[0m")
        print("\033[92m    --- Server {} ---\033[0m".format(i))
        print("\033[93m────────────────────────\033[0m")

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mKharej configs: \033[0m".format(i)))
            
        kharej_ipv6 = input("\033[93mEnter \033[92mKharej Server {}\033[96m IPV6\033[93m address: \033[0m".format(i))

        configs = []
        for j in range(1, num_configs + 1):
            kharej_port = input("\033[93mEnter \033[96mKharej \033[92mConfig {} port\033[93m: \033[0m".format(j))
            tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m") or "443"

            configs.append(kharej_port)

            iran_ud6(j, i, kharej_ipv6, kharej_port, tunnel_port)
        
        current_ipv4 = get_ipv4()
        print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
        for j, config_port in enumerate(configs, start=1):
            print(f"\033[93m| Server {i} - Config {j}: Your Address & Port: {current_ipv4} : {config_port}  \033[0m")
        print("\033[93m╰──────────────────────────────────────────────────────────────────────╯\033[0m")

        server_configs.append((current_ipv4, configs))

    return server_configs
    
        
def kharej_tcp2(host, key_path, tunnel_port=443):
    service_name = "kharejd_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --port {tunnel_port} --host [{host}] --keepalive 10s"

    service_content = f"""[Unit]
Description=Chisel Service Kharej
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mKharej service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service. Error: {}\033[0m".format(e.output))

def kharej_ipv6():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
    
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKharej\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel2()
    key_directory = "/etc/chisel"
    try:
        os.makedirs(key_directory, exist_ok=True)
    except Exception as e:
        display_error("An error occurred while creating the key dir: {}".format(str(e)))

    host = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m address: \033[0m")
    tunnel_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m") or "443"

    print("\033[93m────────────────────────\033[0m")

    key_path = f"{key_directory}/chisel_key_1.key"
    chisel_key(key_path)
    kharej_tcp2(host, key_path, tunnel_port)
    

        
        
def kharej_udp(host, key_path, tunnel_port=443):
    service_name = "kharejd_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --port {tunnel_port} --host {host} --keepalive 10s"

    service_content = f"""[Unit]
Description=Chisel Service Kharej
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mKharej service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service. Error: {}\033[0m".format(e.output))


def kharej_ipv4_udp():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()

    
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKharej\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel2()
    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)
            except NotADirectoryError:
                os.remove(key_directory)
    except Exception as e:
        display_error("An error occurred while removing: {}".format(str(e)))

    try:
        os.makedirs(key_directory, exist_ok=True)
        print("\033[93m────────────────────────\033[0m")
        host = input("\033[93mEnter \033[92mKharej\033[96m IPV4\033[93m address: \033[0m")
        tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m") or '443'
        print("\033[93m────────────────────────\033[0m")

        key_path = f"{key_directory}/chisel_key_1.key"

        try:
            chisel_key(key_path)
            kharej_udp(host, key_path, int(tunnel_port))
        except Exception as e:
            display_error("Failed to generate key: Error: {}".format(str(e)))
    except Exception as e:
        display_error("An error occurred while making dir: {}".format(str(e)))
    

    
def res_chisel3():
    delete_cron()
    if subprocess.call("test -f /etc/reschiseld.sh", shell=True) == 0:
        subprocess.call("rm /etc/reschiseld.sh", shell=True)

    with open("/etc/reschiseld.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("sudo journalctl --vacuum-size=1M\n")
        print("\033[93m───────────────────────────\033[0m")
        print("\033[93mReset timer Questions\033[0m")
        print("\033[93m───────────────────────────\033[0m") 
        num_servers = int(input("\033[93mEnter the\033[92m number of \033[96mKharej \033[92mservers\033[93m[Reset Timer]:\033[0m "))
        num_configs = int(input("\033[93mEnter the\033[92m number of \033[96mKharej \033[92mconfigs\033[93m[Reset Timer]:\033[0m "))
        print("\033[93m───────────────────────────\033[0m") 
        
        for i in range(1, num_configs + 1):
            for j in range(1, num_servers + 1):
                f.write(f"systemctl restart irand_{j}_{i}\n")            

    subprocess.call("chmod +x /etc/reschiseld.sh", shell=True)
    hours = "2"
    cron_entry = f"0 */{hours} * * * /etc/reschiseld.sh"
    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        print("Cron entry added successfully!")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")
        

def res_chisel2():
    delete_cron()
    if subprocess.call("test -f /etc/reschiseld.sh", shell=True) == 0:
        subprocess.call("rm /etc/reschiseld.sh", shell=True)

    with open("/etc/reschiseld.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart kharejd_1\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/reschiseld.sh", shell=True)
    hours = "2"
    cron_entry = f"0 */{hours} * * * /etc/reschiseld.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        print("Cron entry added successfully!")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")
        
def kharej_udp2(host, key_path, tunnel_port=443):
    service_name = "kharejd_1"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel server --keyfile {key_path} --port {tunnel_port} --host [{host}] --keepalive 10s"

    service_content = f"""[Unit]
Description=Chisel Service Kharej
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mKharej service started successfully!\033[0m")

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)
        
        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating Kharej service. Error: {}\033[0m".format(e.output))

def kharej_ipv6_udp():
    forward()
    if not os.path.isfile("/root/chisel"):
        chisel_mnu()
        
    
    print("\033[93m───────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[96mKharej\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    res_chisel2()

    key_directory = "/etc/chisel"
    try:
        if os.path.exists(key_directory):
            try:
                shutil.rmtree(key_directory)
            except NotADirectoryError:
                os.remove(key_directory)
    except Exception as e:
        display_error("An error occurred while removing: {}".format(str(e)))

    try:
        os.makedirs(key_directory, exist_ok=True)  
        host = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m address: \033[0m")
        tunnel_port = input("\033[93mEnter \033[92mTunnel Port\033[93m :\033[0m ") or 443

        print("\033[93m────────────────────────\033[0m") 
        
        key_path = f"{key_directory}/chisel_key_1.key"
        chisel_key(key_path)
        kharej_udp2(host, key_path, tunnel_port)

    except Exception as e:
        display_error("An error occurred: {}".format(str(e)))
    
        
def res_chisel1():
    delete_cron()
    if subprocess.call("test -f /etc/reschiseld.sh", shell=True) == 0:
        subprocess.call("rm /etc/reschiseld.sh", shell=True)

    with open("/etc/reschiseld.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("systemctl daemon-reload\n")
        f.write("sudo journalctl --vacuum-size=1M\n")
        
        print("\033[93m───────────────────────────\033[0m")
        print("\033[93mReset timer questions\033[0m")
        print("\033[93m───────────────────────────\033[0m") 
        num_configs = int(input("\033[93mEnter the\033[92m number of Kharej configs\033[93m:\033[0m "))
        for i in range(1, num_configs + 1):
            config_name = f"irand_{i}"
            f.write(f"systemctl restart {config_name}\n")
        print("\033[93m───────────────────────────\033[0m")

    subprocess.call("chmod +x /etc/reschiseld.sh", shell=True)
    hours = "2"
    cron_entry = f"0 */{hours} * * * /etc/reschiseld.sh"
    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        print("Cron entry added successfully!")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")
        
def iran_udp2(config_number, kharej_ipv6, kharej_port, tunnel_port=443):
    service_name = f"irand_{config_number}"
    service_file = f"/etc/systemd/system/{service_name}.service"
    chisel_command = f"./chisel client --keepalive 10s [{kharej_ipv6}]:{tunnel_port} localhost:{kharej_port}/udp"

    service_content = f"""[Unit]
Description=Kharej Service {config_number}
After=network.target

[Service]
ExecStart=/root/{chisel_command}
Restart=always
RestartSec=5
User=root
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    try:
        with open(service_file, 'w') as file:
            file.write(service_content)

        subprocess.run("systemctl daemon-reload", shell=True, check=True)

        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)

        display_checkmark("\033[92mIRAN service {} started successfully!\033[0m".format(config_number))

        subprocess.run(f"systemctl enable {service_name}", shell=True, check=True)

        subprocess.run(f"systemctl restart {service_name}", shell=True, check=True)

    except subprocess.CalledProcessError as e:
        display_error("\033[91mFailed in creating IRAN service {}. Error: {}\033[0m".format(config_number, e.output))

def delete_cron():
    entries_to_delete = [
        "0 * * * * /etc/reschiseld.sh",  
        "0 */2 * * * /etc/reschiseld.sh",  
        "0 */3 * * * /etc/reschiseld.sh",  
        "0 */4 * * * /etc/reschiseld.sh",  
        "0 */5 * * * /etc/reschiseld.sh", 
        "0 */6 * * * /etc/reschiseld.sh", 
        "0 */7 * * * /etc/reschiseld.sh", 
        "0 */8 * * * /etc/reschiseld.sh", 
        "0 */9 * * * /etc/reschiseld.sh", 
        "0 */10 * * * /etc/reschiseld.sh", 
        "0 */11 * * * /etc/reschiseld.sh", 
        "0 */12 * * * /etc/reschiseld.sh", 
        "0 */13 * * * /etc/reschiseld.sh", 
        "0 */14 * * * /etc/reschiseld.sh", 
        "0 */15 * * * /etc/reschiseld.sh", 
        "0 */16 * * * /etc/reschiseld.sh", 
        "0 */17 * * * /etc/reschiseld.sh", 
        "0 */18 * * * /etc/reschiseld.sh", 
        "0 */19 * * * /etc/reschiseld.sh", 
        "0 */20 * * * /etc/reschiseld.sh", 
        "0 */21 * * * /etc/reschiseld.sh", 
        "0 */22 * * * /etc/reschiseld.sh", 
        "0 */23 * * * /etc/reschiseld.sh",  
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m")

def delete_cron2():
    entries_to_delete = [
        "*/1 * * * * /etc/reschiseld.sh",  
        "*/2 * * * * /etc/reschiseld.sh",  
        "*/3 * * * * /etc/reschiseld.sh",  
        "*/4 * * * * /etc/reschiseld.sh",  
        "*/5 * * * * /etc/reschiseld.sh", 
        "*/6 * * * * /etc/reschiseld.sh",
        "*/7 * * * * /etc/reschiseld.sh",
        "*/8 * * * * /etc/reschiseld.sh",
        "*/9 * * * * /etc/reschiseld.sh",		
        "*/10 * * * * /etc/reschiseld.sh",  
        "*/11 * * * * /etc/reschiseld.sh",  
        "*/12 * * * * /etc/reschiseld.sh", 
        "*/13 * * * * /etc/reschiseld.sh",
        "*/14 * * * * /etc/reschiseld.sh",
        "*/15 * * * * /etc/reschiseld.sh",
        "*/16 * * * * /etc/reschiseld.sh",
        "*/17 * * * * /etc/reschiseld.sh",
        "*/18 * * * * /etc/reschiseld.sh",
        "*/19 * * * * /etc/reschiseld.sh",
        "*/20 * * * * /etc/reschiseld.sh",
        "*/21 * * * * /etc/reschiseld.sh",
        "*/22 * * * * /etc/reschiseld.sh",
        "*/23 * * * * /etc/reschiseld.sh",
        "*/24 * * * * /etc/reschiseld.sh",
        "*/25 * * * * /etc/reschiseld.sh",
        "*/26 * * * * /etc/reschiseld.sh",
        "*/27 * * * * /etc/reschiseld.sh",
        "*/28 * * * * /etc/reschiseld.sh",
        "*/29 * * * * /etc/reschiseld.sh",
        "*/30 * * * * /etc/reschiseld.sh",
        "*/31 * * * * /etc/reschiseld.sh",
        "*/32 * * * * /etc/reschiseld.sh",
        "*/33 * * * * /etc/reschiseld.sh",
        "*/34 * * * * /etc/reschiseld.sh",
        "*/35 * * * * /etc/reschiseld.sh",
        "*/36 * * * * /etc/reschiseld.sh",
        "*/37 * * * * /etc/reschiseld.sh",
        "*/38 * * * * /etc/reschiseld.sh",
        "*/39 * * * * /etc/reschiseld.sh",
        "*/40 * * * * /etc/reschiseld.sh",
        "*/41 * * * * /etc/reschiseld.sh",
        "*/42 * * * * /etc/reschiseld.sh",
        "*/43 * * * * /etc/reschiseld.sh",
        "*/44 * * * * /etc/reschiseld.sh",
        "*/45 * * * * /etc/reschiseld.sh",
        "*/46 * * * * /etc/reschiseld.sh",
        "*/47 * * * * /etc/reschiseld.sh",
        "*/48 * * * * /etc/reschiseld.sh",
        "*/49 * * * * /etc/reschiseld.sh",
        "*/50 * * * * /etc/reschiseld.sh",
        "*/51 * * * * /etc/reschiseld.sh",
        "*/52 * * * * /etc/reschiseld.sh",
        "*/53 * * * * /etc/reschiseld.sh",
        "*/54 * * * * /etc/reschiseld.sh",
        "*/55 * * * * /etc/reschiseld.sh",
        "*/56 * * * * /etc/reschiseld.sh",
        "*/57 * * * * /etc/reschiseld.sh",
        "*/58 * * * * /etc/reschiseld.sh",
        "*/59 * * * * /etc/reschiseld.sh",
        
        
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m")  
        
        
 

def chisel_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mChisel Single Server \033[0m')
    print('2. \033[93m[5] Kharej [1] IRAN  \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            chisel1_status()
            break
        elif server_type == '2':
            menu_status()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def menu_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mMulti Status Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN \033[0m')
    print('2. \033[93mKharej \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            chisel4_status()
            break
        elif server_type == '2':
            chisel5_status()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def chisel2_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mChisel Status\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

    services = {
        'kharej': 'kharejd',
        'iran': 'irand_1',
        'iran': 'irand_2',
        'iran': 'irand_3',
        'iran': 'irand_4',
        'iran': 'irand_5'
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║               \033[92mChisel Status\033[93m                ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            for i in range(num_configs):
                config_service_name = f"{service_name}_{i+1}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                else:
                    status = "\033[91m✘ Inactive   \033[0m"

                if service == 'iran':
                    display_name = '\033[93mIRAN Server   \033[0m'
                elif service == 'kharej':
                    display_name = '\033[93mKharej Service\033[0m'
                else:
                    display_name = service

                print(f"\033[93m║\033[0m    {display_name} {i+1}:   |    {status:<10} \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")
    
def chisel4_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mChisel Status\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    num_servers = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[92mKharej \033[96mServers\033[93m:\033[0m "))
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║               \033[92mChisel Status\033[93m                ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    try:
        for server in range(1, num_servers + 1):
            for config in range(1, num_configs + 1):
                service_name = f"irand_{server}_{config}.service"
                status_output = os.popen(f"systemctl is-active {service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                else:
                    status = "\033[91m✘ Inactive   \033[0m"

                display_name = f'\033[93mIRAN Server {server}   \033[0m'

                print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m ║\033[0m")

    except OSError as e:
        print(f"Error in retrieving status for {service_name}: {e}")

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")
    
def chisel5_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mChisel Status\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    service_name = 'kharejd_1'

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║               \033[92mChisel Status\033[93m                ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    try:
        config_service_name = f"{service_name}.service"
        status_output = os.popen(f"systemctl is-active {service_name}").read().strip()

        if status_output == "active":
            status = "\033[92m✓ Active     \033[0m"
        else:
            status = "\033[91m✘ Inactive   \033[0m"

        display_name = '\033[93mKharej Server   \033[0m'

        print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m ║\033[0m")

    except OSError as e:
        print(f"Error in retrieving status for {service_name}: {e}")

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")
    
def chisel1_status():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mChisel Status\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mConfigs\033[93m:\033[0m "))

    services = {
        'iran': 'irand',
        'kharej': 'kharejd'
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║               \033[92mChisel Status\033[93m                ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            for i in range(num_configs):
                config_service_name = f"{service_name}_{i+1}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service

                    print(f"\033[93m║\033[0m    {display_name} {i+1}:   |    {status:<10} \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")

def uni_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mUninstall Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mChisel Single Server \033[0m')
    print('2. \033[93mChisel Multiple Servers \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_chisel3()
            break
        elif server_type == '2':
            rmv_u()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def rmv_u():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mMultiple Servers Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN \033[0m')
    print('2. \033[93mKharej \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_chisel()
            break
        elif server_type == '2':
            remove_chisel4()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def remove_chisel4():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mChisel\033[93m ...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    delete_cron()
    delete_cron2()

    try:
        if subprocess.call("test -f /root/chisel", shell=True) == 0:
            subprocess.run("rm /root/chisel", shell=True)

        service_name_kharej = "kharejd_1.service"
        subprocess.run(f"systemctl disable {service_name_kharej} > /dev/null 2>&1", shell=True)
        subprocess.run(f"systemctl stop {service_name_kharej} > /dev/null 2>&1", shell=True)
        subprocess.run(f"rm /etc/systemd/system/{service_name_kharej} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred while uninstalling:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_chisel3():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mChisel\033[93m ...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    delete_cron()
    delete_cron2()

    try:
        if subprocess.call("test -f /root/chisel", shell=True) == 0:
            subprocess.run("rm /root/chisel", shell=True)

        time.sleep(1)

        chisel_services = ["kharejd", "irand"]  

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[92mKharej \033[96mConfigs\033[93m:\033[0m "))

        for service_name in chisel_services:
            for i in range(1, num_configs + 1):
                service_name_with_num = f"{service_name}_{i}"
                subprocess.run(f"systemctl disable {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_with_num}.service > /dev/null 2>&1", shell=True)
                time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred while uninstalling..:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_chisel():
    os.system("clear")
    display_notification("\033[93mRemoving \033[92mChisel\033[93m ...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    delete_cron()
    delete_cron2()

    try:
        if subprocess.call("test -f /root/chisel", shell=True) == 0:
            subprocess.run("rm /root/chisel", shell=True)

        time.sleep(1)

        num_servers = int(input("\033[93mEnter the \033[92mnumber\033[93m of Kharej \033[96mServers\033[93m:\033[0m "))
        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of Kharej \033[96mConfigs\033[93m:\033[0m "))

        for server in range(1, num_servers + 1):
            for config in range(1, num_configs + 1):
                service_name_iran = f"irand_{server}_{config}.service"
                subprocess.run(f"systemctl disable {service_name_iran} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_iran} > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_iran} > /dev/null 2>&1", shell=True)
                time.sleep(1)

        service_name_kharej = "kharejd_1.service"
        subprocess.run(f"systemctl disable {service_name_kharej} > /dev/null 2>&1", shell=True)
        subprocess.run(f"systemctl stop {service_name_kharej} > /dev/null 2>&1", shell=True)
        subprocess.run(f"rm /etc/systemd/system/{service_name_kharej} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred while uninstalling:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
        
def start_serv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICES \033[0m')
    print('2. \033[93mStop SERVICES \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            start_servv()
            break
        elif server_type == '2':
            stop_servv()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
         
def start_servv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Restart SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[93m[5] Kharej [1] IRAN \033[0m')
    print('2. \033[96mSingle Server \033[0m')
    print('0. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart2()
            break
        elif server_type == '2':
            restart3()
            break
        elif server_type == '0':
            os.system("clear")
            start_serv()
            break
        else:
            print('Invalid choice.')
            
def restart3():
    os.system("clear")
    display_notification("\033[93mRestarting \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"irand_{i}.service"

            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"kharejd_{i}.service"
            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def restart2():
    os.system("clear")
    display_notification("\033[93mRestarting \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_servers = int(input("\033[93mEnter the number of \033[92m Kharej \033[96mServers\033[93m? \033[0m"))
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for server in range(1, num_servers + 1):
            for config in range(1, num_configs + 1):
                service_name = f"irand_{server}_{config}.service"
                subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
                time.sleep(1)
        
        service_name_kharej = "kharejd_1.service"
        subprocess.run(f"systemctl stop {service_name_kharej} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def restart1():
    os.system("clear")
    display_notification("\033[93mRestarting \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many\033[92m Configs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharejd_1_{i}.service"

            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"irand_{i}.service"
            subprocess.run(f"systemctl restart {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def stop_servv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Stop SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[93m[5] Kharej [1] IRAN \033[0m')
    print('2. \033[96mSingle Server \033[0m')
    print('0. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            stop2()
            break
        elif server_type == '2':
            stop3()
            break
        elif server_type == '0':
            os.system("clear")
            start_serv()
            break
        else:
            print('Invalid choice.')

def stop3():
    os.system("clear")
    display_notification("\033[93mStopping \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"irand_{i}.service"

            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"kharejd_{i}.service"
            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop2():
    os.system("clear")
    display_notification("\033[93mStopping \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_servers = int(input("\033[93mEnter the number of \033[92m Kharej \033[96mServers\033[93m? \033[0m"))
        num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have? \033[0m"))
        
        for server in range(1, num_servers + 1):
            for config in range(1, num_configs + 1):
                service_name = f"irand_{server}_{config}.service"
                subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
                time.sleep(1)
        
        service_name_kharej = "kharejd_1.service"
        subprocess.run(f"systemctl stop {service_name_kharej} > /dev/null 2>&1", shell=True)
        time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop1():
    os.system("clear")
    display_notification("\033[93mStopping \033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        
        num_configs = int(input("\033[93mHow many\033[92m Configs\033[93m do you have? \033[0m"))
        
        for i in range(1, num_configs+1):
            service_name = f"kharejd_1_{i}.service"

            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)
        
        for i in range(1, num_configs+1):
            service_name = f"irand_{i}.service"
            subprocess.run(f"systemctl stop {service_name} > /dev/null 2>&1", shell=True)
            time.sleep(1)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
main_menu()
