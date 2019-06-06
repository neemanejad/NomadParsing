import os, sys, requests

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