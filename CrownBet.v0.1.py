import csv
from selenium import webdriver
from bs4 import BeautifulSoup,Comment

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


#Set website base url
base_url = "https://crownbet.com.au"
sports_url = base_url+"/sports-betting"

#Set output location
base_file = "C:\\Temp\\Results\\Crownbet\\"

#load browser driver
cb_driver = webdriver.Chrome()
cb_driver.maximize_window()

#WARNING
#THIS DOES NOT WORK
for i in range(5):
    cb_driver.find_element_by_tag_name("html").send_keys(Keys.CONTROL, Keys.SUBTRACT)



cb_driver.get(sports_url)

#parse the main page
new_soup = BeautifulSoup(cb_driver.page_source, 'lxml')
body_class = new_soup.find("body",class_="sports sports-allsports sports")

#remove troublesome comments from html
comments = body_class.find_all(text=lambda text:isinstance(text, Comment))
[comment.extract() for comment in comments]

#search for Soccer submenu and load
menu_soup = new_soup.find("a", text="Soccer")
sub_url = (menu_soup).get('href')
soccer_url = base_url+sub_url
cb_driver.get(soccer_url)
delay = 3

#search for all Soccer submenus (Country) and load 
#currently only loading first country
leagues_soup = BeautifulSoup(cb_driver.page_source, 'lxml')
leagues_soccer = leagues_soup.find("a",href=sub_url).parent.parent.find("div",class_="cb-accordion-item__content").find_all("a")
test_league_soccer = leagues_soccer[0]
league_url = base_url+test_league_soccer.get('href')
cb_driver.get(league_url)

try:
    element_present = EC.presence_of_element_located((By.ID, 'smartbanner-wrapper'))
    WebDriverWait(cb_driver, delay).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

#search for all Soccer games and load
#currently only loading first game
league_soup = BeautifulSoup(cb_driver.page_source, 'lxml')
matches_soccer = league_soup.find('div', id="sports-matches").find_all("span", class_="other-matches")
match_url = base_url+matches_soccer[0].a.get('href')
cb_driver.get(match_url)




#match_soup.find_all("div", class_="drop-down-header clearfix closed ")
cb_driver.get(match_url)
#cb_driver.find_element_by_class_name("sports-event-wrap").find_elements_by_css_selector(".drop-down-header.clearfix")
#cb_driver.find_element_by_xpath("//*[@id='middle-container']/div[3]/div[1]/div/div[1]").click()
#cb_driver.find_element_by_xpath("//*[@id='middle-container']/div[3]").find_element_by_xpath("//div[1]/div/div[1]").click()

#cb_driver.find_element_by_id("middle-container").click()

elements = cb_driver.find_elements_by_xpath("//*[@data-stateless='true']")
#elements = cb_driver.find_element_by_class_name("sports-event-wrap").find_elements_by_css_selector(".drop-down-header.clearfix")
#elements = cb_driver.find_element_by_class_name("sports-event-wrap").find_elements_by_tag_name("div")
length = len(elements)-1
for y in range(length):
    ele = length-y
    elements[ele].click()

#parses game page
match_soup = BeautifulSoup(cb_driver.page_source, 'lxml')

#gets bets and odds and writes to the file
#currently only returns submenus that are open - todo: automate opening submenus
odds_socc = match_soup.find_all("div", class_="match-type clearfix")
match_name = match_soup.find("span", class_="item match-name").text.strip()
#creates file name (game name)
file_name_socc =  (base_file +" " +match_name+".csv").replace("/","-")
with open(file_name_socc, 'w') as f:
    f.write("Section,Selection,Odds\n")


for odd_socc in odds_socc:
    sec_soccer_name=odd_socc.find("div",class_="title multiple-events").span.text.strip()
    lines_socc = odd_socc.find_all('span', class_="outcome-anchor-text")
    bets_socc = odd_socc.find_all('span', class_="single-bet-amount")
    for x in range(len(lines_socc) -1):
        with open(file_name_socc, 'a') as f:
            f.write(sec_soccer_name+","+lines_socc[x].text.strip()+","+bets_socc[x].text.strip()+"\n")

#fin