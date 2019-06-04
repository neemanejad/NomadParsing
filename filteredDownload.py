from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup as soup
import os, sys, threading, urllib, check

def footer(containers):
    footer_list = []
    for container in containers:
        footer = container.string
        footer_list.append(footer)
    return footer_list

def getYearAndMonth():
    monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month, year = input("[Nomad]:   Enter month (01-12) and year (2001-2019) in the form (MM/YYYY): ").split()
    month = int(month)

    month = monthList[month - 1]
    return month, year

# def listAllProducts(userUrl):
#     # get year and month
#     month, year = getYearAndMonth()
#
#     # make dictionary for all post request info
#     post = {"theprod": "xxx", "yyyy": year, "mon": month, "view_all": "yes",
#             "day1": "1", "day2": "31", "output": "single", "button": "  Search CNRFC Archive  "}
#     encodedData = parse.urlencode(post).encode("utf-8")
#     print("[Nomad]:   Sending request to %s" % userUrl)
#     pageRequest = urllib.request.Request(userUrl)
#     print("[Nomad]:   Opening %s" % userUrl)
#     page = urlopen(pageRequest, data=encodedData, timeout=120)
#
#     # Dumping html code into variable
#     page_html = page.read()
#
#     # Closing client
#     page.close()
#
#     # Does the html parsing
#     page_soup = soup(page_html, "html.parser")
#
#     # Organizes each link into an index
#     containers = page_soup.findAll("td", {"valign": "top"})
#     productList = footer(containers)
#     dummy = 0

def download(footer_list, user_url, user_dir):
    # Get total files
    total_files = len(footer_list)

    # Creating individual files under they're own name
    for footer in enumerate(footer_list):
        # Checking if file is already in Directory and displaying progress
        if (os.path.isfile(footer[1]) == True):
            continue

        # Writing files to current directory
        try:
            file = open(footer[1], "wb")
            link = user_url + footer[1]
            source = urlopen(link).read()
            file.write(source)
            file.close()
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError:
            print("[Nomad]:   Error downloading %s                           \n", footer[1])
            continue

        # Display download progress to user
        numOfFiles = len(os.listdir(os.getcwd()))
        progress = (numOfFiles / float(total_files)) * 100
        sys.stdout.write("\r[Nomad]:   Downloading to %s: %d/%d | %0.2f%%" %
                         (os.path.basename(user_dir), numOfFiles, total_files, progress))
        sys.stdout.flush()

def filteredDownload(userUrl, user_dir):
    #products = listAllProducts(userUrl)
    month, year = getYearAndMonth()
    wantedProducts = ["netcdfqpe", "netcdfqpf", "netcdfMaxT", "	netcdfMinT", "netcdfot"]
    for product in wantedProducts:
        # Create and open url for product
        userUrl = userUrl + "?myyear=" + year + "&mymon=" + month + "&output=single&myprod=" + product
        uClient = urlopen(userUrl)

        # Dumping html code into variable
        sys.stdout.write("[Nomad]:   Grabbing URL source code for \"%s\"...\n" % product)
        sys.stdout.flush()
        page_html = uClient.read()

        # Closing client
        uClient.close()

        # Does the html parsing
        page_soup = soup(page_html, "html.parser")

        # Organizes each link into an index
        sys.stdout.write("[Nomad]:   Organizing desired URL elements...\n")
        sys.stdout.flush()
        containers = page_soup.find_all("td", {"class": "table-listing-content"})

        # Gets all the footers for the download links
        sys.stdout.write("[Nomad]:   Setting up download instance for \"%s\"...\n\n" % product)
        sys.stdout.flush()
        footer_list = footer(containers)

        # clear unwanted footers in footer list
        newFooterList = []
        for item in enumerate(footer_list):
            if "." in item[1]:
                newFooterList.append(item[1])


        download(newFooterList, userUrl, user_dir)




