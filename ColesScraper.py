# Import the required libraries
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from msedge.selenium_tools import Edge,EdgeOptions
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Configure Chrome options
options = Options()
#options.headless = True
edge_options = EdgeOptions()  
edge_options.use_chromium = True  
edge_options.add_argument("start-maximized")  
edge_options.add_argument("inprivate")
edge_options.add_argument("headless")

# Initialize the Chrome driver
driver = webdriver.Edge(edge_options)
url = "https://www.coles.com.au"
print("Here we go...")
# Navigate to the Coles website
driver.get(url + "/browse")

# Parse the page content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all product categories on the page
categories = soup.find_all("a", class_="coles-targeting-ShopCategoriesShopCategoryStyledCategoryContainer")

print("Are we there yet?")

# Iterate through each category and follow the link to get the products
for category in categories:
    # Get the link to the category page
    category_link = category.get("href")
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
            filename = category.text.strip().replace("/", "") + ".csv"
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
                    if name and price:
                        name = name.text.strip()
                        price = price.text.strip()
                        link = url + productLink
                        writer.writerow([name, price, link])
                          
                # Get the number of pages
                pagination = soup.find("ul", class_="coles-targeting-PaginationPaginationUl")
                pages = pagination.find_all("li")
                last_page = pages[-2].text
                last_page = int(last_page)
                #total_pages = int(pages[-1].text.strip())
                print(last_page)
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
                        if name and price:
                            name = name.text.strip()
                            price = price.text.strip()
                            link = url + productLink
                            writer.writerow([name, price, link]) 
                if page == last_page:
                    break
