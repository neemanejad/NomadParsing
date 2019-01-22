from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os, sys, time, requests, argparse, threading, urllib, ssl, multiprocessing


def check_dir(user_dir):
    if not os.path.isdir(user_dir):
        try:
            os.mkdir(user_dir)
        except PermissionError:
            print("[Nomad]:   Permission denied, check permission settings")
            sys.exit()
        except FileNotFoundError:
            print("[Nomad]:   Can't create multiple subdirectories")
            sys.exit()
        else:
            os.chdir(user_dir)
    else:
        os.chdir(user_dir)
    return user_dir


def check_url(user_url):
    sys.stdout.write("[Nomad]:   Checking \"{}\"\n".format(user_url))
    sys.stdout.flush()
    r = requests.get(user_url)
    if r.status_code != 200:
        print("[Nomad]:   URL does not exist or unreachable\n"
              "[Nomad]:   Usage: ./NomadParse [PATH] [URL]")
        sys.exit()
    return user_url


def footer(containers):
    footer_list = []
    for container in containers[1:]:
        footer_url = container.a["href"]
        footer_list.append(footer_url)
    return footer_list


def existing(footer_list):
    # Count how many files already exist in directory
    exist = 0
    total_size = 0
    for footer in footer_list:
        if (os.path.isfile(footer) == True):
            exist += 1
            file_size = os.path.getsize(footer)
            total_size += float(file_size) / 1000000
    return exist, total_size


def file_progress_count(footer_list):
    # Get ending download count and size
    downloads = 0
    for footer in footer_list:
        if os.path.isfile(footer):
            downloads += 1
    return downloads


def del_file(file):
    while True:
        try:
            os.remove(file)
            break
        except FileNotFoundError:
            break


def download(footer_list, user_url, user_dir):
    # Get total files
    total_files = len(footer_list)

    i = 0 

    # Creating individual files under they're own name
    for footer in enumerate(footer_list):
        # Checks if any network errors were raised
        if i != 0:
            break

        # Checking if file is already in Directory and displaying progress
        if os.path.isfile(footer[1]):
            continue

        # Bypass SSL error
        context = ssl._create_unverified_context()

        # Writing files to current directory
        try:
            file = open(footer[1], "wb")
            link = user_url + footer[1]
            source = urlopen(link, context=context).read()
            file.write(source)
            file.close()
        except urllib.error.HTTPError:
            del_file(footer[1])
            continue
        except OSError:
            del_file(footer[1])
            i = 1
            continue
        except urllib.error.URLError:
            del_file(footer[1])
            i = 1
            continue

        # Grabbing current file number
        dwnld_count = file_progress_count(footer_list)

        # Display download progress to user
        progress = (float(dwnld_count) / float(total_files)) * 100
        sys.stdout.write('[Nomad]:   Downloading to %s: %d/%d | %0.2f%%           \r' %
                         (os.path.basename(user_dir), dwnld_count, total_files, progress))
        sys.stdout.flush()


def download_stats(footer_list):
    # Get ending download count and size
    downloads = 0
    total_size = 0
    for footer in footer_list:
        if os.path.isfile(footer):
            if os.path.getsize(footer) == 0:
                os.remove(footer)
                continue

            else:
                downloads += 1
                file_size = os.path.getsize(footer)
                total_size += float(file_size) / 1000000
    no_download = len(footer_list) - downloads
    return downloads, total_size, no_download


def end_summary(downloads, total_size, no_downloads, minutes, seconds):
    # Notify the user that downloads have finished
    print("       |Download Statistics for \"%s\"|              " % os.path.basename(os.getcwd()))
    print("_____________________________________________________\n")
    print("[Nomad]:   Files downloaded: %d" % downloads)
    print("[Nomad]:   Total download size: %.4f MB" % total_size)
    if no_downloads > 0:
        print("[Nomad]:   Files failed to download: {}".format(no_downloads))
    print("[Nomad]:   Elapsed time: %d:%.2d" % (minutes, seconds))
    print("_____________________________________________________\n")


def main():
    # Command-line input validation
    parser = argparse.ArgumentParser()
    parser.add_argument("PATH", help="where you want the files to be downloaded", type=str)
    parser.add_argument("URL", help="URL you want to download files from", type=str)
    args = parser.parse_args()

    # Creates user inputted directory if it doesn't exist
    user_dir = check_dir(args.PATH)

    # Checks if user inputted a URL and if it exists or responds
    user_url = check_url(args.URL)

    # Opening the Client, grabbing the page
    sys.stdout.write("[Nomad]:   Opening URL\n")
    sys.stdout.flush()
    context = ssl._create_unverified_context()
    uClient = urlopen(user_url, context=context)

    # Dumping html code into variable
    sys.stdout.write("[Nomad]:   Grabbing URL source code\n")
    sys.stdout.flush()
    page_html = uClient.read()

    # Closing client
    uClient.close()

    # Does the html parsing
    page_soup = soup(page_html, "html.parser")

    # Organizes each link into an index
    sys.stdout.write("[Nomad]:   Organizing desired URL elements\n")
    sys.stdout.flush()
    containers = page_soup.findAll("td", {"valign": "top"})

    # Gets all the footers for the download links
    sys.stdout.write("[Nomad]:   Setting up download instance\n\n")
    sys.stdout.flush()
    footer_list = footer(containers)

    # See how many files are in directory before download
    existing_files, existing_size = existing(footer_list)

    # Starting time
    start_time = time.time()

    # Creating threads
    thread_list = []
    for i in range(15):
        p = multiprocessing.Process(target=download, args=(footer_list, user_url, user_dir))
        thread_list.append(p)
        p.start()

    # Ending threads
    for p in thread_list:
        p.join()

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
    downloads, total_size, no_downloads = download_stats(footer_list)
    net_downloads = downloads - existing_files
    net_size = total_size - existing_size

    # Show download summary
    end_summary(net_downloads, net_size, no_downloads, minutes, seconds)


main()
#End