# Chrome needs to be installed
# Driver version needs to be the same as chrome installed

import json
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def get_user_credentials():
    file = open('credentials.json')
    credentials = json.load(file)
    file.close()
    return credentials

def get_chromedriver_fullpath():
    this_directory_name = path.dirname(__file__)
    full_path_file_name = path.join(this_directory_name, 'chrome_driver/chromedriver-96-0-4664-45')
    return full_path_file_name

if __name__ == '__main__':
    service = Service(get_chromedriver_fullpath())
    options = webdriver.ChromeOptions()
    chrome_drive = webdriver.Chrome(service=service, options=options)

    chrome_drive.get('https://www.linkedin.com/uas/login')

    username_input = chrome_drive.find_element(By.XPATH, '//input[@id="username"]')
    password_input = chrome_drive.find_element(By.XPATH, '//input[@id="password"]')
    submit_input = chrome_drive.find_element(By.XPATH, '//button[@class="btn__primary--large from__button--floating"]')

    credentials = get_user_credentials()
    username_input.send_keys(credentials['username'])
    password_input.send_keys(credentials['password'])
    submit_input.click()
    
    chrome_drive.get('https://www.linkedin.com/sales/ssi')

    page_source = chrome_drive.page_source

    first_part = page_source[page_source.index('{"activeSeat"'):]
    second_part = first_part[:first_part.index('</code>')]

    data_dict = json.loads(second_part)

    my_perc_overall = data_dict['memberScore']['overall']
    my_perc_professional_brand = data_dict['memberScore']['subScores'][0]['score']
    my_perc_find_right_people = data_dict['memberScore']['subScores'][1]['score']
    my_perc_insight_engagement = data_dict['memberScore']['subScores'][2]['score']
    my_perc_strong_relationship = data_dict['memberScore']['subScores'][3]['score']

    print(my_perc_overall)
    print(my_perc_professional_brand)
    print(my_perc_find_right_people)
    print(my_perc_insight_engagement)
    print(my_perc_strong_relationship)
    
    chrome_drive.close()
