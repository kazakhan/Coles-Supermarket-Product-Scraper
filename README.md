# Coles-Supermarket-Product-Scraper
Jupyter notebook code to scrape Coles supermarket

This is a Jupyter notebook used to grab prices etc from the Coles website. There is CSV and SQL versions of the code.
It grabs the product description, price, product code and link and saves it to a CSV file for each category.
The SQL version uses sqlite3 and includes the product description, price, product code and category in a single table.
There is a random wait of between 1 & 5 seconds between page loads to avoid being temporarily blocked. 
The Tobacco category has an age restriction pop-up that I'm not interested in overcoming.
