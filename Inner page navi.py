from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
import pandas as pd
from fake_useragent import UserAgent
from time import sleep
from selenium.common.exceptions import NoSuchElementException

base_url='https://www.flipkart.com'
driver = webdriver.Chrome(r'C:\Users\User\Downloads\chromedriver_win32\chromedriver')
def login():
    driver.get('https://www.flipkart.com/account/login')
    usr_name_input = driver.find_element_by_xpath("//div[@id='container']//form/div[@class='_39M2dM JB4AMj']/input[@class='_2zrpKA _1dBPDZ']")
    usr_name_input.send_keys('USER_NAME')
    pwd_input = driver.find_element_by_xpath("//div[@id='container']//form/div[@class='_39M2dM JB4AMj']/input[@class='_2zrpKA _3v41xv _1dBPDZ']")
    pwd_input.send_keys('PASSWORD')
    pwd_input.submit()

login()
soup=BeautifulSoup(driver.page_source,'lxml')
category = [li.a['href'] for li in soup.find_all('li',class_='_1KCOnI _3ZgIXy')]
sub_cat=[base_url+links for links in category]

inner_pg = requests.get(sub_cat[0]).text
inner_soup = BeautifulSoup(inner_pg,'lxml')
product= [a['href'] for a in inner_soup.find_all('a',href=True, attrs={'class':'_31qSD5'})]
final_pg=[base_url+links for links in product]

driver = webdriver.Chrome(r'C:\Users\User\Downloads\chromedriver_win32\chromedriver')
prod_name=[]
del_result=[]
for i in final_pg:
    driver.get(i)
    try:
        pinbar = driver.find_element_by_xpath("//div[@class='col col-12-12']//form[@class='EJrIpC']/input[@id='pincodeInputId']")
        pinbar.send_keys('9999')
        pinbar.submit()
        sleep(1)
        prod_name.append(driver.find_element_by_xpath( "//div[@class='_1HmYoV _35HD7C col-8-12']//h1[@class='_9E25nV']//span").text)
        del_result.append(driver.find_element_by_xpath( "//div[@id='container']//div[@class='col col-12-12']//div[@class='_3l12t9']/div").text)

    except NoSuchElementException: pass
df = pd.DataFrame(data=list(zip(prod_name, del_result)), columns=['Name', 'Delivery Info'])
print(df)
driver.close()










