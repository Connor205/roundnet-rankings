from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
from pprint import pprint

driver = webdriver.Chrome()


def parse_page(number: int):
    tournaments = []
    link = "https://fwango.io/search?sport=roundnet&period=past&page=" + str(
        number)
    driver.get(link)
    driver.implicitly_wait(1)
    tournament_cards = driver.find_elements(
        By.CLASS_NAME, "TournamentCard__Container-sc-15zkmn8-0")
    for tournament_card in tournament_cards:
        l = tournament_card.get_attribute("href")
        try:
            image = tournament_card.find_element(By.TAG_NAME,
                                                 "img").get_attribute("src")
        except:
            image = None
        info = tournament_card.find_element(
            By.CLASS_NAME, "TournamentCard__InfoContainer-sc-15zkmn8-1")
        date = info.find_element(By.CLASS_NAME, "date").text
        name = info.find_element(By.CLASS_NAME, "name").text
        location = info.find_element(By.CLASS_NAME, "location").text
        tournaments.append((l, image, date, name, location))
    return tournaments


all_tournaments = []

for i in range(1, 72):
    print("Scraping Page " + str(i))
    all_tournaments += parse_page(i)
pprint(all_tournaments)
pickle.dump(all_tournaments, open("tournaments.pkl", "wb"))

input("Enter To Exit")
driver.quit()