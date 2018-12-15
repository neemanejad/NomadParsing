from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os, sys, time

my_url = "https://nomads.ncdc.noaa.gov/data/ndfd/201809/20180908/"

# Asks user for a directory to dump files in
print("_____________________________________________________\n")
user_dir = input("Download destination (full path): ")
# Input validation
while (os.path.isdir(user_dir) == False):
    user_dir = input("Invalid path, try again: ")

os.chdir(user_dir)

# Line for separation
print("_____________________________________________________\n")

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
sys.stdout.write("Setting up download instance...\n\n")
sys.stdout.flush()
footer_list = []
for container in containers[1:]:
    footer_url = container.a["href"]
    footer_list.append(footer_url)

# Creating individual files under they're own name
total_size = 0
dwnld_num = 0
exist = 0
start_time = time.time()
for footer in enumerate(footer_list[:100], start=0):

    # Checking if file is already in Directory
    if (os.path.isfile(footer[1]) == True):
        exist += 1
        continue

    # Grabbing current file number
    file_num = footer[0] + 1

    # Display download progress to user
    total_files = len(containers)
    progress = (float(file_num) / float(total_files)) * 100
    sys.stdout.write("Downloading to %s: %d/%d | %0.2f%%\r" % 
        (os.path.basename(user_dir), file_num, total_files, progress))
    sys.stdout.flush()

    # Writing files to current directory
    file = open(footer[1], "wb")
    link = my_url + footer[1]
    source = urlopen(link).read()
    file.write(source)
    file.close()

    # Getting total size of download
    file_abs_path = os.path.abspath(footer[1])
    file_size = os.path.getsize(file_abs_path)
    total_size += file_size

    # Counts how many files were downloaded
    dwnld_num += 1
end_time = time.time()

# Calculate elapsed time post download
elapsed_time = end_time - start_time

# Unit conversions for final statistics
total_size = float(total_size) / (1000000)
elapsed_time_min = elapsed_time / 60
elapsed_time_sec = elapsed_time 
if (elapsed_time >= 60):
    elapsed_time_sec = elapsed_time % elapsed_time_min

# Notify the user that downloads have finished
print("\n\n\n    |All downloads to \"%s\" have completed|" % os.path.basename(user_dir))
print("_____________________________________________________\n")
print(" - Files downloaded: %d" % dwnld_num)
print(" - Files already in %s: %d" % (os.path.basename(user_dir), exist))
print(" - Total download size: %.4f MB" % total_size)
print(" - Elapsed time: %d:%.2d" % (elapsed_time_min, elapsed_time_sec))
print("_____________________________________________________\n")
