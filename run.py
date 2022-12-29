from scraper import run
from os import system, name
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read("config_ssolver.ini", encoding="utf-8")

execution_language = config["settings"]["language"]

if name == 'nt':
    clear_cmd = 'cls'
else:
    clear_cmd = 'clear'

while True:
    
    system(clear_cmd)
    print(config[execution_language]["scraping_day_word"])
    print(config[execution_language]["settings_button"])
    print(config[execution_language]["exit_button"])
    choice = input()
    if choice == "1":
        system(clear_cmd)
        run()
        break
    elif choice == "2":
        while True:
            system(clear_cmd)
            print(config[execution_language]["choose_language"])
            print(config[execution_language]["execution_mode"])
            print("3 - " + config[execution_language]["back"])
            choice = input()
            if choice == "1":
                while True:
                    system(clear_cmd)
                    print(config[execution_language]["lang_fr"])
                    print(config[execution_language]["lang_en"])
                    print("3 - " + config[execution_language]["back"])
                    choice = input()
                    if choice == "1":
                        config["settings"]["language"] = "fr"
                    elif choice == "2":
                        config["settings"]["language"] = "en"
                    elif choice == "3":
                        break
            elif choice == "2":
                while True:
                    system(clear_cmd)
                    print(config[execution_language]["open_browser"])
                    print("")
                    print("3 - " + config[execution_language]["back"])
                    choice = input()
                    if choice in ["Y", "y"]:
                        config["settings"]["headless"] = "no"
                    elif choice in ["N", "n"]:
                        config["settings"]["headless"] = "yes"
                    elif choice == "3":
                        break
            elif choice == "3":
                break
    elif choice == "3":
        break
    with open('config_ssolver.ini', 'w', encoding="utf-8") as f:
        config.write(f)

