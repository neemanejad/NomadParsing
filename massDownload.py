from urllib.request import urlopen
import os, sys, time, requests, threading, urllib

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
        print("[Nomad]:   URL does not exist or unreachable\n")
        sys.exit()
    if (r.status_code != 200):
        print("[Nomad]:   URL does not exist or unreachable\n")
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
            continue

        # Grabbing current file number
        with lock:
            file_num = footer[0] + 1

        # Display download progress to user
        with lock:
            progress = (float(file_num) / float(total_files)) * 100
            sys.stdout.write("\r[Nomad]:   Downloading to %s: %d/%d | %0.2f%%" %
                (os.path.basename(user_dir), file_num, total_files, progress))
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