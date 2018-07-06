from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Grabs URL
my_url = 'https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=zwave&N=-1&isNodeId=1'

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
headers = "product_name, shipping, Current Price, Brand, Price Change \n"
f.write(headers)

# Loops through HTML containers to grab certain attributes: brand,
# name, and shipping. Could format to grab other attributes.
for container in containers:
    try:
        brand_container = container.findAll("div", {"class": "item-branding"})
        brand = brand_container[0].a.img["title"]

        title_container = container.findAll("a", {"class": "item-title"})
        name = title_container[0].text

        shipping_container = container.findAll("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip()

        price_container = container.findAll("li", {"class": "price-current"})
        price = price_container[0].strong.text
        price_change_container = container.findAll("span", {"class": "price-save-percent"})
        if price_change is None:
            continue
        else:
            price_change = price_change_container.text
            print(price_change)
        # try and grab url for next page so I can loop through all z-wave pages
    except(NameError, TypeError, AttributeError):
        print("Error")

    print(brand)
    print(name)
    print(shipping)
    print(price)
    f.write(name.replace(",", "|") + "," + shipping + "," + price + "," + brand + "\n")

f.close()
