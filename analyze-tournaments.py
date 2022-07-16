from ast import parse
from multiprocessing.sharedctypes import Value
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
from pprint import pprint

test_link = "https://fwango.io/sccs"

driver = webdriver.Chrome()
driver.set_window_size(1080, 2000)


def look_for_elements_by_classes(element, classes: list):
    elements = []
    for class_name in classes:
        try:
            elements = elements + element.find_elements(
                By.CLASS_NAME, class_name)
        except:
            pass
    return elements


def parse_results(tourney_link: str):
    driver.get(tourney_link)
    driver.implicitly_wait(3)
    driver.find_element(By.CLASS_NAME,
                        "Checkboxstyle__Checkbox-sc-1hb25xn-0").click()
    teams_elements = driver.find_elements(
        By.CLASS_NAME, "TournamentTeamItemstyle__TeamContainer-sc-1wtiy8a-0")
    team_data = {}
    for team_element in teams_elements:
        try:
            team_players = team_element.find_element(By.CLASS_NAME,
                                                     "players").text
            team_players = team_players.split(" and ")
        except:
            team_players = None
        try:
            team_name = look_for_elements_by_classes(
                team_element, ['team-name-clickable', 'team-names'])
            team_name = team_name[0].text.split("\n")[0]
            print(team_name)
        except:
            team_name = None

        if team_name is not None:
            team_data[team_name] = {"players": team_players}

    pprint(team_data)

    driver.get(tourney_link + "/results")
    driver.implicitly_wait(2)

    driver.find_element(By.CLASS_NAME,
                        "SelectInput__Container-sc-2qbc7r-0").click()
    options = driver.find_element(By.CLASS_NAME, "css-11unzgr")
    division_selections = options.find_elements(By.CSS_SELECTOR, "*")
    for i in range(len(division_selections)):
        options.find_element(By.ID, "react-select-2-option-" + str(i)).click()
        driver.implicitly_wait(0.5)
        results_items = driver.find_elements(By.TAG_NAME, "tr")[1:]
        for result_item in results_items:
            print(result_item.text)
            team_name = result_item.find_element(By.CLASS_NAME,
                                                 "team-name").text
            record = result_item.find_element(By.CLASS_NAME,
                                              "record-column").text
            team_data[team_name]["record"] = record
        driver.find_element(By.CLASS_NAME,
                            "SelectInput__Container-sc-2qbc7r-0").click()
        options = driver.find_element(By.CLASS_NAME, "css-11unzgr")
        division_selections = options.find_elements(By.CSS_SELECTOR, "*")

    pprint(team_data)


parse_results(test_link)

input("Enter To Exit")
driver.quit()