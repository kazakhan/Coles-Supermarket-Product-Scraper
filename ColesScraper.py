# Import the required libraries
import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from webdriver_manager.microsoft import EdgeChromiumDriverManager


# Configure Chrome options
options = Options()

# Initialize the Chrome driver
driver = webdriver.Edge(EdgeChromiumDriverManager().install())
url = "https://www.coles.com.au"
print("Here we go...")
# Navigate to the Coles website
driver.get(url + "/browse")

# Parse the page content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all product categories on the page
categories = soup.find_all("a", class_="coles-targeting-ShopCategoriesShopCategoryStyledCategoryContainer")

for category in categories:
    print(category.text)
# Iterate through each category and follow the link to get the products
for category in categories:
    # Get the link to the category page
    category_link = category.get("href")
    # Liqour breaks more often than not and the Tobacco category has an age check so stop here
    if category_link == "/browse/tobacco":
        break;
    category_link = url + category_link
    print(category_link)
    

        
    if category_link is not None:
        # Follow the link to the category page
        driver.get(category_link)
        
        while True:
            # Parse the page content
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Find all products on the page
            products = soup.find_all("header", class_="product__header")
            
            # Create a new csv file for each category
            filename = category.text + ".csv"
            filepath = "D:\\Documents\\Budget\\" + filename
            if os.path.exists(filepath):
                os.remove(filepath)
            with open(filepath, "a", newline="") as f:
                writer = csv.writer(f)
                
                # Iterate through each product and extract the product name, price and link
                for product in products:
                    name = product.find("h2", class_="product__title")
                    price = product.find("span", class_="price__value")
                    productLink = product.find("a", class_="product__link")["href"]
                    productcode = productLink.split("-")[-1]
                    if name and price:
                        name = name.text.strip()
                        price = price.text.strip()
                        link = url + productLink
                        writer.writerow([productcode, name, price, link])
                          
                # Get the number of pages
                try:
                    pagination = soup.find("ul", class_="coles-targeting-PaginationPaginationUl")
                except:
                    break

                pages = pagination.find_all("li")
                last_page = pages[-2].text
                last_page = int(last_page)
                total_pages = int(pages[-2].text.strip())
                print(total_pages)
                for page in range(2, last_page + 1):
                    # Get the link to the next page
                    next_page_link = f"{category_link}?page={page}"
                    # Navigate to the next page
                    driver.get(next_page_link)

                    # Parse the page content
                    soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Find all products on the page
                    products = soup.find_all("header", class_="product__header")

                    # Iterate through each product and extract the product name, price and link
                    for product in products:
                        name = product.find("h2", class_="product__title")
                        price = product.find("span", class_="price__value")
                        productLink = product.find("a", class_="product__link")["href"]
                        productcode = productLink.split("-")[-1]
                        if name and price:
                            name = name.text.strip()
                            price = price.text.strip()
                            link = url + productLink
                            writer.writerow([productcode, name, price, link])
                time.sleep(3)
                if page == last_page:
                    break
print("Finished")
