import argparse
import massDownload, check

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
    user_dir = check.check_dir(args.PATH)

    # Lists websites to select from
    website = "https://nomads.ncdc.noaa.gov/data/ndfd/201809/20180908/"

    massDownload.massDownload(website, user_dir)

main()
