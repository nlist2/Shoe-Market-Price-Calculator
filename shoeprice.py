#!/usr/bin/python3
import smtplib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from termcolor import colored
import sys
import statistics

print(colored("Shoe Market Price Calculator", "green"))

shoe = input("What shoe do you want the market price range of? ")
size = input("What size? ")
condition = input("New or used? ")

# Asserting the size is legitimate -> 11.5 won't work right now.
while(size.isdigit() is False or 4 > float(size) or float(size) > 15):
    print(colored("Invalid size, try again. Size needs to be greater than 4 and less than 15.", "red"))
    size = input("What size? ")

# Defining the driver 
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
print(colored("Automation successfully created as a headless Firefox Webdriver...", "green"))

# Stock X prices:
try:
    print("Getting StockX.com...")
    driver.get("https://www.stockx.com")

    #Finding the search input and sending keys of the shoe that we want
    driver.find_element_by_id("home-search").send_keys(str(shoe) + Keys.RETURN)
    print("Getting " + str(shoe) + "...")

    #First element in result and clicking it
    shoe_tile = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tile.Tile-c8u7wn-0.bCufAv")))
    shoe_tile.click()

    #Size number
    #implicitywait
    size_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "fa.fa-chevron-down")))
    size_box.click()

    #Picking your size...
    size_div = driver.find_element_by_class_name("list-unstyled.sneakers")
    size_div.find_elements_by_class_name("title")

    for x in range(len(size_div)):
        if(size_div[x].text == str(size)):
            stockx_price = size_div[x].find_element_by_class_name("subtitle").text
        
    print(colored("StockX price: " + str(stockx_price), "green"))

except:
    print(colored("StockX failed.... Continuing...", "red"))

try:
    print("Getting Ebay.com...")
    driver.get("https://www.ebay.com")

    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gh-tb.ui-autocomplete-input")))
    search_input.send_keys(str(shoe) + Keys.RETURN)

    print("Getting " + str(shoe) + "...")

    size_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "size-component")))
    sizes = size_div.find_elements_by_class_name("size-component__square")

    for x in range(len(sizes)):
        if(sizes[x].text == str(size)):
            sizes[x].click()
            break
            print(colored("Correct size chosen...", "green"))

    num_results_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"srp-controls__count-heading")))
    num_results = num_results_box.find_element_by_tag_name("span").text
    print("Ebay has " + str(num_results) + " results...")

    results_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"srp-river-results")))
    listings = results_box.find_elements_by_class_name("s-item__price")
    ebay_price_list = []

    if(int(num_results) > 47):
        num_results = 47

    for x in range(int(num_results)):
        current_price = str(listings[x].text)
        ebay_price_list.append(float(current_price[1:7]))

    print("Ebay average price: $" + colored(str(statistics.mean(ebay_price_list)), "green"))
    
except:
    print(colored("Ebay failed.... Continuing...", "red"))