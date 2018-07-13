from bs4 import BeautifulSoup as soup
import requests
import time

entered_URL = input("Enter URL for Scraping: ")

start_time = time.time()

# Grabs HTML from specified URL
r = requests.get(entered_URL)
page_soup = soup(r.text, 'html.parser')

# Grabs URL for the next page in order to start process over again
URL_container = page_soup.findAll("span", {"class": "pagnLink"})

# Opens file writer and makes a specific file for file writer
amazon = str('0')
filename = str("amazon" + amazon + ".csv")
f = open(filename, "w")

for x in range(len(URL_container)+1):
    # Gets item container at specific part of html
    containers = page_soup.findAll("div", {"class": "s-item-container"})

    # Headers of CSV files
    headers = "Brand, Product Name, Price, Rating, # of Ratings, Stock, Is It On Sale? \n"
    f.write(headers)

    # Initializing variables that will be written onto CSV
    name = ""
    price = ""
    rating = ""
    brand = ""
    stock = ""
    og_price = ""
    number_reviews = ""
    # Loops through HTML containers to grab certain attributes: brand,
    # name, and shipping. Could format to grab other attributes.
    for container in containers:
        try:
            name = container.a.img["alt"]

            brand_container = container.findAll("span", {"class": "a-size-small a-color-secondary"})
            brand = brand_container[1].text

            price_container = container.findAll("span", {"class": "a-offscreen"})
            price = price_container[0].text

            rating_container = container.findAll("i", {"class": "a-icon-star"})
            rating = rating_container[0].span.text

            number_rating_containers = container.findAll("a", {"class": "a-size-small a-link-normal a-text-normal"})
            number_rating = number_rating_containers[0].text

            stock_container = container.findAll("span", {"class": "a-size-small a-color-price"})
            stock = stock_container[0].text

            og_price_container = container.findAll("span", {"class": "a-size-base-plus a-color-secondary a-text-strike"})
            og_price = og_price_container[0].text
            if og_price != price:
                og_price = "On Sale"
            else:
                og_price = "Not on Sale"
        except(NameError, TypeError, IndexError, AttributeError):
            print("Error")

        # Small debug block that prints values that are pulled from HTML
        print("name " + name)
        print("price " + price)
        print("rating " + rating)
        print("brand " + brand)

        # Writer that adds variables to the CSV file
        f.write(brand + "," + name.replace(",", "|") + "," + price + "," + rating + "," + number_rating.replace(",", "")
               + "," + stock + "," + og_price + "," + "\n")

        # Resets variable value
        og_price = ""
        stock = ""

    try:
        placeholder_URL = URL_container[x].a.attrs['href']
        entered_URL = 'https://www.amazon.com' + str(placeholder_URL)
        print("Link # " + str(x) + " " + entered_URL)
        r = requests.get(entered_URL)
        page_soup = soup(r.text, 'html.parser')
    except(IndexError):
        continue

# Closes writer
f.close()

print("--- %s seconds ---" % round((time.time() - start_time), 2))
