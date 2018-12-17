from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os, sys, time, requests

def main():
    # Gives user the "help" prompt if no args exist
    check_anyargs()

    # Checks if there's too many arguments
    check_toomany()

    # Shows user how to use NomadParse
    check_help()

    # Gets user inputted directory
    user_dir = sys.argv[1]

    # Creates user inputted directory if it doesn't exist
    check_dir(user_dir)

    # Checks if user inputted a URL and if it exists or responds
    my_url = check_url()

    # Opening the Client, grabbing the page
    sys.stdout.write("[Nomad]:   Opening URL...\n")
    sys.stdout.flush()
    uClient = urlopen(my_url)

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
    footer_list = footer(containers)

    # Initializing some variables
    total_size = 0
    dwnld_num = 0
    exist = 0
    total_files = len(containers)

    # Creating individual files under they're own name
    download(containers, footer_list, my_url, user_dir)

main()

###############################################################



def check_anyargs():
    if (len(sys.argv) == 1):
        print("[Nomad]:   Try './NomadParse --help' for more information")
    sys.exit()

def check_toomany():
    if (sys.argv[1] == "--help"):
        print("[Nomad]:   Usage: ./NomadParse [PATH] [URL]")
    sys.exit()

def check_help():
    if (sys.argv[1] == "--help"):
        print("[Nomad]:   Usage: ./NomadParse [PATH] [URL]")
    sys.exit()

def check_dir(user_dir):
    if (os.path.isdir(user_dir) == False):
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

def check_url():
    try:
        my_url = sys.argv[2]
    except IndexError:
        print("[Nomad]:   URL is required\n"
            "[Nomad]:   Usage: ./NomadParse [PATH] [URL]")
        sys.exit()
    else:
        sys.stdout.write("[Nomad]:   Checking URL...\n")
        sys.stdout.flush()
        try:
            r = requests.get(sys.argv[2])
        except:
            print("[Nomad]:   URL does not exist or unreachable\n"
                "[Nomad]:   Usage: ./NomadParse [PATH] [URL]")
            sys.exit()
        if (r.status_code != 200):
            print("[Nomad]:   URL does not exist or unreachable\n"
                "[Nomad]:   Usage: ./NomadParse [PATH] [URL]")
            sys.exit()
    return my_url

def footer(containers):
    footer_list = []
    for container in containers[1:]:
        footer_url = container.a["href"]
        footer_list.append(footer_url)
    return footer_list

def download(containers, footer_list, my_url, user_dir):
    # Initializing some variables
    total_size = 0
    dwnld_num = 0
    exist = 0
    total_files = len(containers)

    # Creating individual files under they're own name
    start_time = time.time()
    for footer in enumerate(footer_list[:50], start=0):
        # Grabbing current file number
        file_num = footer[0] + 1

        # Checking if file is already in Directory and displaying progress
        if (os.path.isfile(footer[1]) == True):
            exist += 1
            progress = (float(file_num) / float(total_files)) * 100
            sys.stdout.write("[Nomad]:   Downloading to %s: %d/%d | %0.2f%%\r" % 
                (os.path.basename(user_dir), file_num, total_files, progress))
            sys.stdout.flush()
            continue

        # Display download progress to user
        progress = (float(file_num) / float(total_files)) * 100
        sys.stdout.write("[Nomad]:   Downloading to %s: %d/%d | %0.2f%%\r" % 
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
    print("\n\n\n    |All downloads to \"%s\" have completed|" % os.path.basename(os.getcwd()))
    print("_____________________________________________________\n")
    print("[Nomad]:   Files downloaded: %d" % dwnld_num)
    print("[Nomad]:   Files already in directory: %d" % (exist))
    print("[Nomad]:   Total download size: %.4f MB" % total_size)
    print("[Nomad]:   Elapsed time: %d:%.2d" % (elapsed_time_min, elapsed_time_sec))
    print("_____________________________________________________\n")
