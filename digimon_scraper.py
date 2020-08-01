from bs4 import BeautifulSoup
from platform import system
from time import sleep
import csv
import os
import requests

DEVELOPER_MODE = True
BASE_URL = 'http://digidb.io/digimon-list/'

sep = '\\' if system() == "Windows" else '/'
if not os.path.exists('.' + sep + 'regular_images'):
    os.mkdir('.' + sep + 'regular_images')
if not os.path.exists('.' + sep + 'pixel_images'):
    os.mkdir('.' + sep + 'pixel_images')

if DEVELOPER_MODE:
    if not os.path.isfile('.' + sep + 'homepage_response.txt'):
        homepage_response_request = requests.get(BASE_URL)
        sleep(1)
        with open('homepage_response.txt', 'w') as file:
            file.write(homepage_response_request.text)
    with open('homepage_response.txt', 'r') as file:
        homepage_response = file.read()
    homepage_soup = BeautifulSoup(homepage_response, 'html.parser')
else:
    homepage_response = requests.get(BASE_URL)
    sleep(1)
    homepage_soup = BeautifulSoup(homepage_response.text, 'html.parser')

all_digimon_rows = homepage_soup.select('tbody > tr')
all_digimon = []

for digimon_row in all_digimon_rows:
    row_columns = digimon_row.select('td')
    extracted_digimon_data = {
        "Number": row_columns[0].select_one('b').get_text().strip(), 
        "Name": row_columns[1].select_one('a').get_text(), 
        "Stage": row_columns[2].select_one('center').get_text(), 
        "Type": row_columns[3].select_one('center').get_text(), 
        "Attribute": row_columns[4].select_one('center').get_text(), 
        "Memory": row_columns[5].select_one('center').get_text(), 
        "Equip Slots": row_columns[6].select_one('center').get_text(), 
        "HP": row_columns[7].select_one('center').get_text(), 
        "SP": row_columns[8].select_one('center').get_text(), 
        "Atk": row_columns[9].select_one('center').get_text(), 
        "Def": row_columns[10].select_one('center').get_text(), 
        "Int": row_columns[11].select_one('center').get_text(), 
        "Spd": row_columns[12].select_one('center').get_text(), 
        "URL": row_columns[1].select_one('a')['href']
    }
    all_digimon.append(extracted_digimon_data)

if not os.path.isfile('.' + sep + 'digimon_scraped_data.csv'):
    with open('digimon_scraped_data.csv', 'w', newline='') as csv_file:
        csv_headers = ("Number", "Name", "Stage", "Type", "Attribute", "Memory",
                        "Equip Slots", "HP", "SP", "Atk", "Def", "Int", "Spd", "URL")
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        csv_writer.writeheader()
        for digimon in all_digimon:
            csv_writer.writerow(digimon)


def sanitize_digimon_name(name):
    strip_chars = ('.', '(', ')')
    for char in strip_chars:
        safe_name = name.replace(char, '')
    return safe_name.replace(' ', '_')


for digimon in all_digimon[0:1]:
    print(f"Gathering images for {digimon['Name']}...")
    safe_name = sanitize_digimon_name(digimon['Name'])
    digimon_page = requests.get(digimon['URL'])
    sleep(1)

    digimon_page_soup = BeautifulSoup(digimon_page.text, 'html.parser')
    digimon_info_table = digimon_page_soup.select_one('table:is(#infotable)')

    reg_img_url = digimon_info_table.select_one('tr > td > img:is(.topimg)')['src']
    reg_img_data = requests.get(reg_img_url).content
    sleep(1)
    reg_img_filename = f"{digimon['Number'].zfill(3)}_{safe_name}_reg.jpg"
    reg_img_path = '.' + sep + 'regular_images' + sep + reg_img_filename
    with open(reg_img_path, 'wb') as img_file:
        img_file.write(reg_img_data)

    pxl_img_url = digimon_info_table.select_one('tr > td > img:is(.dot)')['src']
    pxl_img_data = requests.get(pxl_img_url).content
    sleep(1)
    pxl_img_filename = f"{digimon['Number'].zfill(3)}_{safe_name}_pxl.jpg"
    pxl_img_path = '.' + sep + 'pixel_images' + sep + pxl_img_filename
    with open(pxl_img_path, 'wb') as img_file:
        img_file.write(pxl_img_data)
