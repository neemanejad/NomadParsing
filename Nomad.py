import sys, time, argparse, threading
import massDownload, filteredDownload, check

def selectURL(websiteList):
    while (1):
        print("==========WEBSITE LIST==========")

        numOfWebsites = 0
        # Print list of currently supported websites
        for website in enumerate(websiteList):
            print(str(website[0] + 1) + ". " + website[1])
            numOfWebsites += 1

        # input validation for user given directory
        check.check_dir(sys.argv[1])

        choice = input("[Nomad]:   Select website (type number): ")
        choice = int(choice) - 1
        if choice > numOfWebsites - 1 or choice < 0:
            print("[Nomad]:   Error, type a number that exists in the list\n")
            continue
        else:
            break

    return websiteList[choice]

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
    user_dir = massDownload.check.check_dir(args.PATH)

    # Lists websites to select from
    websiteList = ["https://nomads.ncdc.noaa.gov/data/ndfd/201809/20180908/",
                   "https://www.cnrfc.noaa.gov/arc_search.php"]
    userUrl = selectURL(websiteList)

    if (userUrl == websiteList[0]):
        massDownload.massDownload(userUrl, user_dir)
    else:
        filteredDownload.filteredDownload(userUrl, user_dir)

main()

### ERRORS ###
# urllib.error.HTTPError