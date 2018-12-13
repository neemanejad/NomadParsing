from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os

my_url = "https://nomads.ncdc.noaa.gov/data/ndfd/201809/20180908/"

# Opening the Client, grabbing the page
uClient = urlopen(my_url)

# Dumping html code into variable
page_html = uClient.read()

# Closing client
uClient.close()

# Does the html parsing
page_soup = soup(page_html, "html.parser")

# Organizes each link into an index
containers = page_soup.findAll("td",{"valign":"top"})

# Gets all the footers for the download links
footer_list = []
for container in containers[1:]:
    footer_url = container.a["href"]
    footer_list.append(footer_url)

# Notify the user where the files wll be downloaded
current_path = os.getcwd()
print("________________________________________________\n")
print("\n\n Files will be downloaded at", current_path, "\n\n")
print("    Disclaimer: due to there being")
print("   ", len(containers), "files, this is going to\n"
       "    take a while, the program will\n"
       "    notify you when the downloads have\n"
       "    finished.")
print("________________________________________________\n")

# Creating individual files under they're own name
for footer in footer_list[:1]:
    file = open(footer, "wb")
    link = my_url + footer
    source = urlopen(link).read()
    file.write(source)

# Notify the user that downloads have finished
print("________________________________________________\n")
print("\n\n  All downloads have completed.\n\n")
print("________________________________________________\n")
