from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os, sys, time, requests, argparse, threading

# Global Variables for download statistics
dwnld_num = 0
total_size = 0
total_size_mb = 0
minutes = 0
seconds = 0
lock = threading.Lock()

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
    return user_dir

def check_url(user_url):
    sys.stdout.write("[Nomad]:   Checking URL...\n")
    sys.stdout.flush()
    try:
        r = requests.get(user_url)
    except:
        print("[Nomad]:   URL does not exist or unreachable\n"
            "[Nomad]:   Usage: ./NomadParse [PATH] [URL]")
        sys.exit()
    if (r.status_code != 200):
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
    
def download(footer_list, user_url, user_dir):
    # Set variables
    global dwnld_num, total_size, total_size_mb
    total_files = len(footer_list)
    
    # Creating individual files under they're own name
    for footer in enumerate(footer_list[:50]):
        # Checking if file is already in Directory and displaying progress
        with lock:
            if (os.path.isfile(footer[1]) == True):
                continue

        # Writing files to current directory
        file = open(footer[1], "wb")
        link = user_url + footer[1]
        source = urlopen(link).read()
        file.write(source)
        file.close()

        # Grabbing current file number
        with lock:
            file_num = footer[0] + 1

        # Counts how many files were downloaded
        with lock:
            dwnld_num += 1

        # Getting total size of download
        file_abs_path = os.path.abspath(footer[1])
        with lock:
            file_size = os.path.getsize(file_abs_path)
            total_size += file_size
        with lock:
            total_size_mb = float(total_size) / (1000000)

        # Display download progress to user
        with lock:
            progress = (float(file_num) / float(total_files)) * 100
            sys.stdout.write("[Nomad]:   Downloading to %s: %d/%d | %0.2f%%\r" % 
                (os.path.basename(user_dir), file_num, total_files, progress))
            sys.stdout.flush()

    # Download size conversion to MB
        #with lock:
            #total_size_mb = float(total_size) / (1000000)
    
def end_summary():
    # Declaring global variables
    global dwnld_num, total_size, total_size_mb, minutes, seconds

    # Notify the user that downloads have finished
    print("\n\n\n    |All downloads to \"%s\" have completed|" % os.path.basename(os.getcwd()))
    print("_____________________________________________________\n")
    print("[Nomad]:   Files downloaded: %d" % dwnld_num)
    print("[Nomad]:   Total download size: %.4f MB" % total_size_mb)
    print("[Nomad]:   Elapsed time: %d:%.2d" % (minutes, seconds))
    print("_____________________________________________________\n")

def main():
    global dwnld_num, total_size, total_size_mb, minutes, seconds

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
    sys.stdout.write("[Nomad]:   Opening URL...\n")
    sys.stdout.flush()
    uClient = urlopen(user_url)

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

    # Starting time
    start_time = time.time()

    # Creating threads
    thread_list = []
    for i in range(10):
        t = threading.Thread(target=download, name="thread{}".format(i),
            args=(footer_list, user_url, user_dir), daemon=False)
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
        elapsed_time_sec = elapsed_time % minutes

    # Show download summary
    end_summary()

main()