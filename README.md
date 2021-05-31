# Digimon Scraper

Scraper for downloading Digimon images from http://digidb.io/digimon-list/.

Required Python modules are listed in `requirements.txt`. Note that the script utilizes f-strings, thus requiring Python 3.6+.

Start the process by executing `digimon_scraper.py`.
* If the directories `pixel_images` and `regular_images` do not exist in the same directory that the file is run from, it will create them.
* If the file `digimon_scraped_data.csv` does not exist, the script will create one with extracted information for all Digimon.
* The script will then begin downloading images into the `pixel_images` and `regular_images` directories, printing a status in the terminal as it progresses.

## Notes
* The script is intended to function properly on Windows and Unix-like systems, but has currently only been tested on Windows.
* `DEVELOPER_MODE`: When set to `True`, the script will create a file `homepage_response.txt` containing the homepage `request` response in text form. Useful to debug and work without needed to repeatedly make live requests.
* After downloading the two images for a Digimon, the script will sleep for 0.5 seconds. The website's `robots.txt` page does not specify an amount of time to sleep between requests; this is just my attempt to be respectful to the site. The last full run of the script for me took just under 6 minutes to complete. If you'd like to remove the sleeps, take a look at the constant `LONGER_SLEEP`.

## TO-DO
* Implement a Digimon class instead of using a dictionary.
* Implement in the form of a cron job which will download images in batches over an extended period of time.