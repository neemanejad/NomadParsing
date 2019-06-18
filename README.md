## NomadParsing
NomadParse is a program that allows a user to 
download large amounts of files with ease through 
automation. The program only 
downoads files from: https://nomads.ncdc.noaa.gov/data/ndfd/201809/20180908/

## Usage
As soon as the program begins, you'll be asked for input. You're input arguments should be these items in this particular order:
1. Which of the currently supported websites you'd like to download from.
2. If second website is chosen, then user will be asked for month and year of the desired files and the project(s) to download from. 

If these input arguments are not met, the program will display an error message with the correct usage and exit. One thing to note is that if the indicated path doesn't exist, NomadParse will attempt to create it. 

## Setup Nomad
1. Confirm that the latest version of 'pip' is installed on your machine.
2. Install the 'BeautifulSoup' module by typing `pip install bs4` on a terminal/command line.
3. Install the 'Requests' module by typing `pip install requests` on a terminal/command line.
## Synopsis of Operations
Using the user given path and URL, NomadParse will access the website and organize its contents regarding download links in the HTML source code. Once the certain elements that contain the download link information within the HTML source code have been identified and organized by a module called "BeautifulSoup4", a list is made of all the download link suffixes concatenated at the end of the given URL. What's left is a whole list of download links ready to be downloaded at the given path. Using the "multiprocessing" module, ten individual threads are asked to perform the download operation, which consists of opening and writing files in binary from the links read from the website. "multiprocessing" was used because during earlier builds of the program, downloading over five-thousand files would take a little over an hour to complete. With multi-threading, the program only takes about twenty minutes to download over 5300 files, which is a huge improvement. After the threads have completed the download operation, a statistics menu is displayed on the screen, showing how many files were downloaded, how many MB of space were used, and the time it took for the whole download process. 
