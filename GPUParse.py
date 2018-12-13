from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

my_url = "https://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=graphics+cards&N=-1&isNodeId=1"

# Opening the Client, grabbing the page
uClient = urlopen(my_url)

# Dumping html code into variable
page_html = uClient.read()

# Closing client
uClient.close()

# Does the html parsing
page_soup = soup(page_html, "html.parser")

# Grabs each product
containers = page_soup.findAll("div",{"class":"item-container"})

# Access contents of a certain product
container = containers[3]
