from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup as soup
import os, sys, threading, urllib, check

def getMaxYear(userUrl):
    # open base url to get max year
    uClient = urlopen(userUrl)
    page_html = uClient.read()

    # Closing client
    uClient.close()

    # organize html source code
    page_soup = soup(page_html, "html.parser")

    containers = page_soup.find_all("select", {"id": "yyyy"})

    # get all listing years
    yearList = []
    for year in enumerate(containers[0].contents):
        try:
            # skip odd indices
            if year[0] % 2 == 0:
                continue
            yearList.append(year[1]["value"])
        except KeyError:
            continue

    return int(max(yearList))


def footer(containers):
    footer_list = []
    for container in containers:
        footer = container.string
        footer_list.append(footer)
    return footer_list

def getYearAndMonth(userUrl):
    maxYear = getMaxYear(userUrl)
    monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    while(1):
        try:
            print("\n==========SELECT DATE==========")
            month, year = input("[Nomad]:   Enter month (01-12) and year (2001-" + str(maxYear) + ") in the form (MM YYYY): ").split()
            month = int(month)
            if month < 1 or month > 12:
                print("[Nomad]:   ERROR - month must be between 01-12")
                continue
            elif int(year) < 2001 or int(year) > getMaxYear(userUrl):
                print("[Nomad]:   ERROR - year must be between 2001-" + str(maxYear))
                continue
        except ValueError:
            print("[Nomad]:   ERROR - date requires the month and year in the form (MM YYYY)")
            continue
        break


    month = monthList[month - 1]
    return month, year

def listAllProducts(userUrl, month, year):
    # make dictionary for all post request info
    post = {"theprod": "xxx", "yyyy": year, "mon": month, "view_all": "yes",
            "day1": "1", "day2": "31", "output": "single", "button": "  Search CNRFC Archive  "}

    # send post request to website
    encodedData = parse.urlencode(post).encode("utf-8")
    pageRequest = urllib.request.Request(userUrl)
    page = urlopen(pageRequest, data=encodedData, timeout=120)

    # Dumping html code into variable
    page_html = page.read()

    # Closing client
    page.close()

    # Does the html parsing
    page_soup = soup(page_html, "html.parser")

    # Organizes each link into an index
    containers = page_soup.findAll("optgroup", {"class": "searchtextul"})

    # get list of all product names
    productTitles = []
    products = []
    for container in containers:
        for content in enumerate(container.contents):
            try:
                # skip odd indices
                if content[0] % 2 == 0:
                    continue
                products.append(content[1]["value"])
                productTitles.append(content[1].string)
            except KeyError:
                continue

    # Display names of all products
    print("\n==============================PRODUCT LIST==============================")
    for product in enumerate(productTitles):
        print("%d.  %s" % (product[0] + 1, product[1]))

    # select all wanted products
    badVal = False
    while(1):
        wantedProductsIndices = []
        selectedProducts = input("\n[Nomad]:   Select all desired products (using numbers, i.g. 1 32 24): ").strip(" ").split(" ")
        for productNum in selectedProducts:
            try:
                if int(productNum) > len(products) or int(productNum) < 0:
                    print("[Nomad]:   ERROR - product number %d doesn't exist, it won't be downloaded" % int(productNum))
                    continue
                wantedProductsIndices.append(int(productNum) - 1)
            except ValueError:
                print("[Nomad]:   ERROR - please use numbers to select products")
                badVal = True
                break

        # Check if user input letters instead of numbers
        if badVal:
            badVal = False
            continue

        break

    wantedProducts = []
    for i in wantedProductsIndices:
        wantedProducts.append(products[i])

    return wantedProducts

def download(footer_list, user_url):
    # Get total files
    total_files = len(footer_list)

    # Creating individual files under they're own name
    for footer in enumerate(footer_list):

        # Display download progress to user
        fileNum = footer[0] + 1
        progress = (fileNum / float(total_files)) * 100
        sys.stdout.write("\r[Nomad]:   Downloading to %s: %d/%d | %0.2f%%" %
                         (os.path.basename(os.getcwd()), fileNum, total_files, progress))
        sys.stdout.flush()

        # Checking if file is already in Directory and displaying progress
        if (os.path.isfile(footer[1]) == True):
            continue

        # create full file url
        link = user_url + footer[1]

        # Writing files to current directory
        try:
            file = open(footer[1], "wb")
            source = urlopen(link, timeout=120).read()
            file.write(source)
            file.close()
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError:
            print("[Nomad]:   ERROR downloading %s                           \n", footer[1])
            continue
        except ConnectionResetError:
            print("\n[Nomad]:   ERROR - connection was forcibly closed by remote host")


def filteredDownload(userUrl, user_dir):
    month, year = getYearAndMonth(userUrl)

    wantedProducts = listAllProducts(userUrl, month, year)
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
        sys.stdout.write("[Nomad]:   Setting up download instance for \"%s\"...\n" % product)
        sys.stdout.flush()
        footer_list = footer(containers)

        # clear unwanted footers in footer list
        newFooterList = []
        for item in enumerate(footer_list):
            if "." in item[1]:
                newFooterList.append(item[1])

        # Create new url for files
        userUrlSplit = userUrl.rsplit('/', 1)
        baseUrl = userUrlSplit[0]
        fileUrl = baseUrl + "/archive/" + year + "/" + month + "/" + product + "/"

        # Creating threads
        thread_list = []
        for i in range(10):
            t = threading.Thread(target=download, name="thread{}".format(i),
                                 args=(newFooterList, fileUrl), daemon=True)
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()

        print("\n[Nomad]:   SUCCESS - Downloads done for %s\n" % product)

