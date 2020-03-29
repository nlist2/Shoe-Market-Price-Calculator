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

print(colored("Shoe Market Price Calculator\n", "green"))

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
driver = webdriver.Firefox()
print(colored("\nAutomation successfully created as a headless Firefox Webdriver...\n", "green"))

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
    stockx_url = driver.current_url
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
        
    ebay_url = driver.current_url

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

    ebay_average_price = str(statistics.mean(ebay_price_list))[0:6]
    print("Ebay average price: " + colored("$" + ebay_average_price, "green"))

except:
    print(colored("Ebay failed.... Continuing...", "red"))

try:
    print("Getting GOAT...")
    driver.get("https://www.goat.com")

    #clicking the search button
    driver.find_element_by_id("Layer_1").click()

    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "InstantSearchBox__Input-wfzp5c-1.gboPWO")))
    search_input.send_keys(str(shoe) + Keys.RETURN)
    print("Getting " + str(shoe) + "...")

    results_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "filter-results-area")))
    time.sleep(1)
    results_box.find_elements_by_class_name("Grid__CellWrapper-sc-1njij7e-0.dWCtit")[0].click()

    price_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProductTitlePaneActions__ButtonTextWrapper-l1sjea-0.kHmiHb")))
    price_box.click()

    size_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProductSelectSize__SizeList-eiqexh-5.kHqGmR")))
    sizes = size_box.find_elements_by_class_name("ProductVariantSize__Wrapper-ci5six-0.dCiSfE")
    prices = size_box.find_elements_by_class_name("ProductVariantButton__Price-fapubr-2.fHJrlz")

    for x in range(len(sizes)):
        if(str(size) in sizes[x].text):
            goat_price = str(prices[x].text)[0:4]
            print("GOAT current price: " + colored(goat_price, "green"))
            sizes[x].click()
            time.sleep(1)
            goat_url = driver.current_url
            break
except:
    print(colored("GOAT failed.... Continuing...", "red"))

try:
    print("Getting Grailed...")
    driver.get("https://www.grailed.com")

    driver.find_element_by_id("globalheader_search").send_keys(str(shoe) + Keys.RETURN)
    print("Getting " + str(shoe) + "...")
    time.sleep(2)
    grailed_url = driver.current_url

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "listing-size.sub-title")))
    sizes = driver.find_elements_by_class_name("listing-size.sub-title")
    prices = driver.find_elements_by_class_name("sub-title.original-price")
    grailed_price_list = []

    for x in range(len(sizes)):
        if(str(sizes[x].text) == str(size)):
            grailed_price_list.append(int(str(prices[x].text)[1:4]))
            print(grailed_price_list)

    grailed_average_price = str(statistics.mean(grailed_price_list))
    print("Grailed average price: " + colored("$" + grailed_average_price, "green"))
 
except:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ReactModal__Content ReactModal__Content--after-open.modal._hasHeader.AuthenticationModal")))
    driver.find_element_by_class_name("close").click()
    print("Closed Grailed 2FA...")
    print(colored("Grailed failed.... Continuing...", "red"))

#Print Summary
print("\nPrice Summary for: " + str(shoe) + " size " + str(size) + ":\n")
print("\t StockX:")
print("\t\t Current price: N/A")
print("Find at: " + str(stockx_url) + "\n")
print("\t Ebay:")
print("\t\t Average price: $" + ebay_average_price)
print("Find at: " + str(ebay_url) + "\n")
print("\t GOAT:")
print("\t\t Current price: " + str(goat_price))
print("Find at: " + str(goat_url) + "\n")
print("\t Grailed:")
print("\t\t Average price: " + str(grailed_average_price))
print("Find at: " + str(grailed_url) + "\n")