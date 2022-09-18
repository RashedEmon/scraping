from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import string

# import from local module
from database import db, Label, Images, Hotel


def startBrowser():
    option = Options()
    option.headless = False
    office = "/home/w3e103/web_drivers/geckodriver"
    personal = "C:\\Users\\rashe\\src\\geckodriver.exe"
    service = Service(executable_path=personal)
    global driver
    driver = webdriver.Firefox(service=service, options=option)
    driver.fullscreen_window()

# it takes destination place name and find and return the link of the destination
def getDestinationLink(destination: str):
    driver.get('https://www.kayak.co.in/?ispredir=true')
    elements = driver.find_elements(by=By.CLASS_NAME, value='P_Ok-wrapper')
    for element in elements:
        place = element.find_element(by=By.CLASS_NAME, value='P_Ok-title').text
        if (place.lower() == destination.lower()):
            anchor = element.find_element(
                by=By.CSS_SELECTOR, value='.P_Ok-header-links span:last-child a')
            return anchor.get_attribute(name='href')
        else:
            print('destination not found')

#it takes a destination link. find first hotel of the destination and return a tuple containing link and hotel name. 
def getHotelNameAndLink(url: str):
    try:
        driver.get(url)
    except:
        print('error while loading page')
        return None
    anchor = driver.find_element(by=By.CLASS_NAME, value='soom-name')
    hotelName = anchor.find_element(by=By.CSS_SELECTOR, value='span').text
    return (anchor.get_attribute(name='href'), hotelName)

#takes url of a specific hotel and return list of tuple containing label and button element
def getButtonAndLabel(url:str):
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


 # take list of tuple of button and label and return a dictionary containing label and corresponding image list
 # dict={
 # 'label1': [img1,img2],
 # 'label-2': [img1,img2,img3]
 # }
def getImageWithLabel(buttonWithLabel: list) -> dict:
    obj = {}
    # iterate on every button and click those button in every iteration
    for button in buttonWithLabel:
        # print(button[0])
        label = button[0]
        labelFirstWord = button[0].split(' ')[0]
        try:
            button[1].click()
            time.sleep(2)
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
            print('Element not found')

        try:
            buttons = driver.find_elements(
                by=By.CSS_SELECTOR, value='.ZVFD-dots-wrapper li button')
            if len(buttons) > 0:
                for button in buttons:
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
            print('No Such Element Exist')

    return obj

#takes hotel name and dictionary of image label and image. Save data to database
def SaveToDatabase(hotelName: str, labelAndImage: dict):
    print(hotelName)
    print(labelAndImage)
    db.connect()
    try:
        db.create_tables([Hotel, Label, Images])
    except:
        print('already created')

    hotelId = 0
    try:
        hotelId = Hotel.create(name=hotelName)
    except:
        hotelId = Hotel.get(name=hotelName)

    for label in labelAndImage.keys():
        labelid = ''
        try:
            labelid = Label.create(name=label)
        except:
            labelid = Label.get(name=label)
            print(labelid)
            print('label already exist')

        for image in labelAndImage[label]:
            if image:
                Images.create(hotel=hotelId, image=image, label=labelid)

    db.close()
# program start executing from here
def main():
    startBrowser()
    if driver == None:
        print('driver is none')
        return
    destination='mumbai'
    hotelName = ''
    dest = getDestinationLink(destination)
    hotel = getHotelNameAndLink(dest)

    if hotel:
        hotelName = hotel[1]
        hotelUrl = hotel[0]
    else:
        return
    image = getImageWithLabel(getButtonAndLabel(hotelUrl))

    print(image)
    time.sleep(5)
    driver.close()
    print(hotelName)
    # res = Label.create(name="Bedroom")
    # SaveToDatabase(hotelName=hotelName, labelAndImage=image)


main()
