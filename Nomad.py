from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import sys, time, argparse, threading
import massDownload, filteredDownload

def selectURL(websiteList):
    while (1):
        print("==========WEBSITE LIST==========")

        numOfWebsites = 0
        # Print list of currently supported websites
        for website in enumerate(websiteList):
            print(str(website[0]) + ". " + website[1])
            numOfWebsites += 1

        choice = input("[Nomad]:   Select website (type number): ")
        if int(choice) > numOfWebsites - 1 or int(choice) < 0:
            print("[Nomad]:   Error, type a number that exists in the list\n")
            continue
        else:
            break

    return websiteList[int(choice)]

def massDownloader():
    # perform mass download configuration

    return

def filteredDownloader():
    # perform filtered download configuration

    return

def main():
    # Command-line input validation
    parser = argparse.ArgumentParser()
    parser.add_argument("PATH", help="where you want the files to be downloaded", type=str)
    args = parser.parse_args()

    # Creates user inputted directory if it doesn't exist
    user_dir = massDownload.check_dir(args.PATH)

    # Lists websites to select from
    websiteList = ["https://nomads.ncdc.noaa.gov/data/ndfd/201809/20180908/",
                   "https://www.cnrfc.noaa.gov/arc_search.php"]
    userUrl = selectURL(websiteList)

    # # Check if URL is responsive
    # userUrl = massDownload.check_url(userUrl)

    # Opening the Client, grabbing the page
    sys.stdout.write("[Nomad]:   Opening URL...\n")
    sys.stdout.flush()
    uClient = urlopen(url=userUrl, timeout=120)

    # Dumping html code into variable
    sys.stdout.write("[Nomad]:   Grabbing URL source code...\n")
    sys.stdout.flush()
    page_html = uClient.read()

    # Closing client
    uClient.close()

    # Does the html parsing
    page_soup = soup(page_html, "html.parser")

    # Organizes each link into an index
    sys.stdout.write("[Nomad]:   Organizing desired URL elements...\n")
    sys.stdout.flush()
    containers = page_soup.findAll("td",{"valign":"top"})

    # Gets all the footers for the download links
    sys.stdout.write("[Nomad]:   Setting up download instance...\n\n")
    sys.stdout.flush()
    footer_list = massDownload.footer(containers)

    # See how many files are indirectory before download
    existing_files, existing_size = massDownload.existing(footer_list)

    # Starting time
    start_time = time.time()

    # Creating threads
    thread_list = []
    for i in range(10):
        t = threading.Thread(target=massDownload.download, name="thread{}".format(i),
            args=(footer_list, userUrl, user_dir), daemon=True)
        thread_list.append(t)
        t.start()
        
    for t in thread_list:
        t.join()

    # Ending time
    end_time = time.time()

    # Calculate elapsed time post download
    elapsed_time = end_time - start_time

    # Unit conversions for final statistics
    minutes = elapsed_time / 60
    seconds = elapsed_time 
    if (elapsed_time >= 60):
        seconds = elapsed_time % minutes

    # Get downloads statistics
    downloads, total_size = massDownload.download_stats(footer_list)
    net_downloads = downloads - existing_files
    net_size = total_size - existing_size

    # Show download summary
    massDownload.end_summary(net_downloads, net_size, minutes, seconds)

main()

### ERRORS ###
# urllib.error.HTTPError