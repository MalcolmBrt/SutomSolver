from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from solveur_mot import solveur
from time import sleep
import logging
import configparser

config = configparser.ConfigParser()
config.read("config_ssolver.ini", encoding="utf-8")

# Parti logging
logger = logging.getLogger('sutom_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
formatter.datefmt = '%H:%M:%S'
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)




def run():
    execution_language = config["settings"]["language"]
    # Ouvre naviguateurs
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # désactive message erreur selenium
    
    if config["settings"]["headless"] == "yes":
        options.add_argument("--headless")
    sutom = webdriver.Chrome(options=options)

    logger.info(config[execution_language]["waiting_loading"])
    # Aller sur sutom
    sutom.get("https://sutom.nocle.fr")

    # Trouver le bouton en utilisant son ID puis le cliquer
    try:
        croix = sutom.find_element(By.ID, "panel-fenetre-bouton-fermeture-icone")
        croix.click()
    except:
        pass # Si l'élément n'existe pas, ignorer l'erreur

    # Attend que la page se charge avant d'entrer dans la boucle

    WebDriverWait(sutom, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'input-ligne')))
    logger.info(config[execution_language]["start_searching"])
    body_page = sutom.find_element(By.TAG_NAME, "body")

    lettres_interdites = set()
    lettres_mal_placés = set()
    mot_déjà_écrit = []
    nb_essai = 1
    while True:
        if sutom.find_elements(By.CLASS_NAME, "fin-de-partie-panel-phrase") == []: # Vérifier que la partie n'est pas encore finie
            row = sutom.find_element(By.XPATH, f"//table/tr[{nb_essai}]")
            row_text = row.text.lower()
            mot_possible = solveur(row_text, mot_déjà_écrit, lettres_interdites, lettres_mal_placés)
            logger.info(config[execution_language]["test_number"] + str(nb_essai) + " " + config[execution_language]["with"] + " " + mot_possible[0] + ".")
            if mot_possible == []:
                logger.error(config[execution_language]["non_existent_word"])
                break
            mot_déjà_écrit.append(mot_possible[0]) # inverser 2 lignes haut bas
            body_page.send_keys(mot_possible[0], Keys.ENTER)
            sleep(3)
            for element in sutom.find_elements(By.CLASS_NAME, "lettre-non-trouve"):
                lettres_interdites.add(element.text.lower())
            liste_td = sutom.find_elements(By.XPATH, f'//*[@id="grille"]/table/tr[{nb_essai}]/td')
            for n in range(len(liste_td)):
                if liste_td[n].get_attribute("class") == "mal-place resultat":
                    lettres_mal_placés.add((liste_td[n].text.lower(), n))
            nb_essai += 1
        else:
            logger.info(config[execution_language]["i_found"] + " " + str(mot_possible[0]) + ".")
            break
        
if __name__ == "__main__":
    run()
    print("hok")