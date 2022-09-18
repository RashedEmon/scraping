from traceback import print_tb
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import string
from database import db, Label, Images, Hotel

option = Options()
option.headless = False
office = "/home/w3e103/web_drivers/geckodriver"
personal = "C:\\Users\\rashe\\src\\geckodriver.exe"
service = Service(executable_path=personal)
driver = webdriver.Firefox(service=service, options=option)
driver.fullscreen_window()


def getDestinationLink(destination: str):
    driver.get('https://www.kayak.co.in/?ispredir=true')
    elements = driver.find_elements(by=By.CLASS_NAME, value='P_Ok-wrapper')
    for element in elements:
        place = element.find_element(by=By.CLASS_NAME, value='P_Ok-title').text
        if (place.lower() == destination.lower()):
            anchor = element.find_element(
                by=By.CSS_SELECTOR, value='.P_Ok-header-links span:last-child a')
    return anchor.get_attribute(name='href')


def getHotelNameAndLink(url: str):
    try:
        driver.get(url)
    except:
        print('error while loading page')
        return None
    anchor = driver.find_element(by=By.CLASS_NAME, value='soom-name')
    hotelName = anchor.find_element(by=By.CSS_SELECTOR, value='span').text
    return (anchor.get_attribute(name='href'), hotelName)


def getAHotel(url):
    driver.get(url)
    for btn in driver.find_elements(by=By.TAG_NAME, value='button'):
        try:
            if 'view all photos'.lower() == btn.find_element(by=By.CSS_SELECTOR, value='.Iqt3-button-content').text.lower():
                btn.click()
                labelButtons = driver.find_element(
                    by=By.CLASS_NAME, value='DTct-categories-container').find_elements(by=By.TAG_NAME, value='button')
                buttonWithLabel = [(button.find_element(by=By.CSS_SELECTOR, value='div div div').text.rstrip(
                    string.digits), button) for button in labelButtons]
                return buttonWithLabel[1:]
        except:
            print('View all button not found')

    # for button in labelButtons:
 # take tuple list of button and label and return a dictionary containing label and corresponding image list
 # dict={
 # 'label1': [img1,img2],
 # 'label-2': [img1,img2,img3]
 # }


def getImageWithLabel(buttonWithLabel: list) -> dict:
    obj = {}
    # iterate on every button and click those button in every iteration
    for button in buttonWithLabel:
        print(button[0])
        label = button[0]
        labelFirstWord = button[0].split(' ')[0]
        try:
            button[1].click()
            time.sleep(3)
            obj[label] = []
        except:
            print('button is not clickable')
            continue

        try:
            firstListItem = driver.find_element(
                by=By.CSS_SELECTOR, value='.ZVFD-dots-wrapper')
            driver.execute_script(
                f'arguments[0].style.transform = "translateX(-0%)"', firstListItem)

        except:
            print('not found')

        try:
            buttons = driver.find_elements(
                by=By.CSS_SELECTOR, value='.ZVFD-dots-wrapper li button')
            # print(len(buttons))
            # firstButton = button[0]
            if len(buttons) > 0:
                for button in buttons:
                    # print(button)
                    button.click()
                    time.sleep(1)
                    image = button.find_element(
                        by=By.TAG_NAME, value='img').get_attribute('src')
                    obj[label] += [image]

            else:
                image = driver.find_element(
                    by=By.CSS_SELECTOR, value=f'img[alt*={labelFirstWord}]').get_attribute('src')
                obj[label] = [image]
        except:
            print('error happened')

    return obj


# program start executing from here
def main():
    # hotelName = ''
    # dest = getDestinationLink('kolkata')
    # hotel = getHotelNameAndLink(dest)
    # hotelName = hotel[1]
    # hotelUrl = hotel[0]
    # image = getImageWithLabel(getAHotel(hotelUrl))

    # print(image)
    time.sleep(5)
    driver.close()
    db.connect()
    db.create_tables([Hotel, Label, Images])

    res = Label.create(name="Bedroom")


main()
