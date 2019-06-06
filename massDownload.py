from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import os, sys, threading, urllib, time, check

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

def download(footer_list, user_url, user_dir):
    # Get total files
    total_files = len(footer_list)

    # Setting lock for multithreaded downloads
    lock = threading.Lock()

    # Creating individual files under they're own name
    for footer in enumerate(footer_list):
        # Checking if file is already in Directory and displaying progress
        with lock:
            if (os.path.isfile(footer[1]) == True):
                continue


        # Grabbing current file number
        with lock:
            file_num = footer[0] + 1

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
        with lock:
            numOfFiles = len(os.listdir(os.getcwd()))
            progress = (numOfFiles / float(total_files)) * 100
            sys.stdout.write("\r[Nomad]:   Downloading to %s: %d/%d | %0.2f%%" %
                (os.path.basename(os.getcwd()), numOfFiles, total_files, progress))
            sys.stdout.flush()

def download_stats(footer_list):
    # Get ending download count and size
    downloads = 0
    total_size = 0
    for footer in footer_list:
        if (os.path.isfile(footer) == True):
            downloads += 1
            file_size = os.path.getsize(footer)
            total_size += float(file_size) / 1000000
    return downloads, total_size

def end_summary(downloads, total_size, minutes, seconds):
    # Notify the user that downloads have finished
    print("\n\n\n    |All downloads to \"%s\" have completed|" % os.path.basename(os.getcwd()))
    print("_____________________________________________________\n")
    print("[Nomad]:   Files downloaded: %d" % downloads)
    print("[Nomad]:   Total download size: %.4f MB" % total_size)
    print("[Nomad]:   Elapsed time: %d:%.2d" % (minutes, seconds))
    print("_____________________________________________________\n")

def massDownload(userUrl, user_dir):
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
    containers = page_soup.findAll("td", {"valign": "top"})

    # Gets all the footers for the download links
    sys.stdout.write("[Nomad]:   Setting up download instance...\n\n")
    sys.stdout.flush()
    footer_list = footer(containers)

    # See how many files are indirectory before download
    existing_files, existing_size = existing(footer_list)

    # Starting time
    start_time = time.time()

    # Creating threads
    thread_list = []
    for i in range(10):
        t = threading.Thread(target=download, name="thread{}".format(i),
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