# Chrome needs to be installed
# Driver version needs to be the same as chrome installed

import json
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def get_username():
    file = open('credentials.json')
    credentials = json.load(file)
    file.close()
    return credentials['username']


def get_password():
    file = open('credentials.json')
    credentials = json.load(file)
    file.close()
    return credentials['password']


def get_chromedriver_fullpath():
    this_directory_name = path.dirname(__file__)
    full_path_file_name = path.join(this_directory_name, 'chrome_driver/chromedriver-96-0-4664-45')
    return full_path_file_name


def set_input_fields(chrome_drive):
    username_input = chrome_drive.find_element(By.XPATH, '//input[@id="username"]')
    password_input = chrome_drive.find_element(By.XPATH, '//input[@id="password"]')

    username_input.send_keys(get_username())
    password_input.send_keys(get_password())


def submit_form(chrome_drive):
    submit_input = chrome_drive.find_element(By.XPATH, '//button[@class="btn__primary--large from__button--floating"]')

    submit_input.click()


def show_data(data_dict):
    my_perc_overall = data_dict['memberScore']['overall']
    my_perc_professional_brand = data_dict['memberScore']['subScores'][0]['score']
    my_perc_find_right_people = data_dict['memberScore']['subScores'][1]['score']
    my_perc_insight_engagement = data_dict['memberScore']['subScores'][2]['score']
    my_perc_strong_relationship = data_dict['memberScore']['subScores'][3]['score']

    print(f'Overall: {my_perc_overall} de 100')
    print(f'Estabelecer sua marca profissional: {my_perc_professional_brand} de 20')
    print(f'Localizar as pessoas certas: {my_perc_find_right_people} de 20')
    print(f'Interagir oferecendo insights: {my_perc_insight_engagement} de 20')
    print(f'Criar relacionamentos: {my_perc_strong_relationship} de 20')

    my_top_percent_of_sector = data_dict['groupScore'][0]['rank']
    my_industry = data_dict['groupScore'][0]['industry']

    print(f'Principais {my_top_percent_of_sector}% no setor de {my_industry}')


def get_data(chrome_drive):
    page_source = chrome_drive.page_source

    first_part = page_source[page_source.index('{"activeSeat"'):]
    second_part = first_part[:first_part.index('</code>')]

    data_dict = json.loads(second_part)

    return data_dict


def get_linkedin_login_url():
    return 'https://www.linkedin.com/uas/login'


def get_linked_ssi_url():
    return 'https://www.linkedin.com/sales/ssi'


if __name__ == '__main__':
    chrome_drive = webdriver.Chrome(service=Service(get_chromedriver_fullpath()), options=webdriver.ChromeOptions())

    chrome_drive.get(get_linkedin_login_url())

    set_input_fields(chrome_drive)

    submit_form(chrome_drive)

    chrome_drive.get(get_linked_ssi_url())

    show_data(get_data(chrome_drive))
    
    chrome_drive.close()
