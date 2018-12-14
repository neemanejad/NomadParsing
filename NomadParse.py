from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os, sys

my_url = "https://nomads.ncdc.noaa.gov/data/ndfd/201809/20180908/"

# Asks user for a directory to dump files in
user_dir = input("Download destination (full path): ")
os.chdir(user_dir)

# Opening the Client, grabbing the page
sys.stdout.write("Accessing URL...\n")
sys.stdout.flush()
uClient = urlopen(my_url)

# Dumping html code into variable
sys.stdout.write("Grabbing URL source code...\n")
sys.stdout.flush()
page_html = uClient.read()

# Closing client
uClient.close()

# Does the html parsing
page_soup = soup(page_html, "html.parser")

# Organizes each link into an index
sys.stdout.write("Organizing desired URL elements...\n")
sys.stdout.flush()
containers = page_soup.findAll("td",{"valign":"top"})

# Gets all the footers for the download links
sys.stdout.write("Setting up download instance...\n")
sys.stdout.flush()
footer_list = []
for container in containers[1:]:
    footer_url = container.a["href"]
    footer_list.append(footer_url)

# Notify the user where the files wll be downloaded
print("Files will be downloaded at \"%s\"\n" % user_dir)
sys.stdout.flush()


# Creating individual files under they're own name
for footer in enumerate(footer_list, start=0):
    # Grabbing current file number
    file_num = footer[0] + 1

    # Display download progress to user
    total_files = len(containers)
    progress = (float(file_num) / float(total_files)) * 100
    sys.stdout.write("Download progress: %0.2f%%  \r" % progress)
    sys.stdout.flush()

    # Writing files to current directory
    file = open(footer[1], "wb")
    link = my_url + footer[1]
    source = urlopen(link).read()
    file.write(source)
    
    

# Notify the user that downloads have finished
print("________________________________________________\n")
print("\n\n         All downloads have completed\n\n")
print("________________________________________________\n")

