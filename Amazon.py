from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Grabs URL
my_url = 'https://www.amazon.com/s?me=A1O77D5UJY7IVU'

# Opening connection, grab the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# parse
page_soup = soup(page_html, "html.parser")

# get specific part of html
containers = page_soup.findAll("div", {"class": "s-item-container"})

# Specific file for file writer
filename = "amazon.csv"
f = open(filename, "w")

# Head of CSV files
headers = "Product Name, Price, Shipping, Rating \n"
f.write(headers)

# Loops through HTML containers to grab certain attributes: brand,
# name, and shipping. Could format to grab other attributes.
for container in containers:
    try:
        name = container.a.img["alt"]

        price_container = container.findAll("span", {"class": "a-offscreen"})
        price = price_container[0].text

        # shipping_container = container.findAll("span", {"class": "a-size-base-plus a-color-secondary"})
        # shipping = shipping_container[0].text

        rating_container = container.findAll("span", {"class": "a-icon-alt"})
        rating = rating_container[0].text
    except(NameError, TypeError, IndexError, AttributeError):
        print("Error")

    print("name " + name)
    print("price " + price)
    # print("shipping" + shipping)
    print("rating " + rating)

    f.write(name.replace(",", "|") + "," + price + "," + rating + "\n")

f.close()
