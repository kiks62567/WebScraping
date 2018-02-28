from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Grabs URL
my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards'

# Opening connection, grab the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# parse
page_soup = soup(page_html, "html.parser")

# get specific part of html
containers = page_soup.findAll("div", {"class": "item-container"})

# Specific file for file writer
filename = "product.csv"
f = open(filename, "w")

# Head of CSV files
headers = "brands, product_name, shipping \n"
f.write(headers)

# Loops through HTML containers to grab certain attributes: brand,
# name, and shipping. Could format to grab other attributes.
for container in containers:
    try:
       # brand = container.div.div.a.img["title"]
        title_container = container.findAll("a", {"class": "item-title"})
        name = title_container[0].text
        shipping_container = container.findAll("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip()
    except(NameError, TypeError):
        print("Error")

   # print(brand)
    print(name)
    print(shipping)
    f.write(name.replace(",", "|") + "," + shipping + "\n")

f.close()
