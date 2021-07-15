from selenium import webdriver
from PIL import Image
from dotenv import load_dotenv
import os
import time
import pytesseract
import urllib

load_dotenv(encoding='utf-8')
doctorName = os.getenv('DOCTOR_NAME')
UserROCID = os.getenv('USER_ROCID')

# 使用 Chrome 的 WebDriver
browser = webdriver.Chrome()

while True: 
    browser.get(
        'https://www2.ndmctsgh.edu.tw/NewWebReg/Register/Doctors?pos=B&DeptCode=110&DeptGroup=1')

    # get var _schedules
    _schedules = browser.execute_script('return _schedules')

    # print(_schedules)
    # print(type(_schedules))
    RowId = []
    for week in _schedules:
        # print(week)
        # print(type(week))

        for Dates in week['Dates']:
            # print(Dates)
            # print(type(Dates))

            if bool(Dates['SegTimes']):

                for Doctor in Dates['SegTimes'][0]['Doctors']:

                    if Doctor['Name'] == doctorName and bool(Doctor['RowId']):
                        RowId.append(Doctor['RowId'])
                        print(Doctor)
                        # print(type(Doctor))
                        # print('------------------------------')
                        print(f'\n')

    print('預約[]=> ', RowId)
    if bool(RowId):
        break


browser.get('https://www2.ndmctsgh.edu.tw/NewWebReg/')
next_button = browser.find_element_by_xpath(
    '/html/body/div/div/p[11]/a[1]')
next_button.click()
time.sleep(1)
for id in RowId:
    id = urllib.parse.urlencode({'id': id})
    browser.get(
        'https://www2.ndmctsgh.edu.tw/NewWebReg/Register/RegData?' + id)
    print('https://www2.ndmctsgh.edu.tw/NewWebReg/Register/RegData?' + id)

    with open('filename.jpg', 'wb') as file:
        file.write(browser.find_element_by_xpath(
            '/html/body/div/div[2]/div/form/div[3]/div[2]/img').screenshot_as_png)

    img = Image.open(r'.\filename.jpg')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    config = '--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(img, config=config)
    print(text)
    VerificationCode = browser.find_element_by_xpath(
        '/html/body/div/div[2]/div/form/div[3]/div[2]/input')
    VerificationCode.clear()
    VerificationCode.send_keys(text)
    ROCID = browser.find_element_by_xpath(
        '/html/body/div/div[2]/div/form/div[1]/div[2]/input')
    ROCID.clear()
    ROCID.send_keys(UserROCID)
    while True:
        if browser.current_url == ('https://www2.ndmctsgh.edu.tw/NewWebReg/Register/RegData?id=' + id):
            print('WAIT')
            time.sleep(1)
        else:
            print('FINISH')
            print(browser.current_url)
            break
# browser.close()