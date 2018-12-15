import urllib3
import re
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

usr = ''
pwd = ''

# Initialize a firefox browser
driver = webdriver.Firefox()

# open fb
driver.get('https://www.facebook.com/')
print('Opened Facebook')
sleep(1)

# inserts username
username_box = driver.find_element_by_id('email')
username_box.send_keys(usr)
print('Email Entered')
sleep(1)

# inserts password
pwd_box = driver.find_element_by_id('pass')
pwd_box.send_keys(pwd)
print('Password Entered')
sleep(1)

# login
login_box = driver.find_element_by_id('loginbutton')
login_box.click()
print('Done')


driver.get('') # insert photo url

# smash that motherfucking like button
like_button = driver.find_element_by_class_name('_3t54')
like_button.click()
print('Done')


# scrape the names and links to their profiles
html = driver.page_source
soup = BeautifulSoup(html)
links = []
for link in soup.find_all('a', href=re.compile("^https://.{1,70}(profile_browser)$")):
    links.append(link.get('href'))

names = []
for link in soup.find_all('img', style='width:40px;height:40px'):
    names.append(link.get('aria-label'))

# unite names and links in one dictionary
name_link = dict(zip(names, links))

# iterate over names and get their pictures
for name, link in name_link.items():
    # open a given profile and parse its html
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html)
    
    # open the photo separetly
    photo = soup.find('a', id='u_0_v').get('href')
    driver.get(photo)
    html = driver.page_source
    soup = BeautifulSoup(html)
    
    # find the path of the photo to download
    image_path = soup.find('img', class_='spotlight').get('src')
    urllib.request.urlretrieve(image_path, 'pics/{}.jpg'.format(name.replace(' ', '_')))
    sleep(1)

