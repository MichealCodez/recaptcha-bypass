from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

browser = webdriver.Chrome()


#def captcha():
delay_time = 2
audio_to_text_delay = 10
website = 'https://www.beverlygrovedentistry.com/contactus'
# text_to_speach = 'https://speech-to-text-demo.ng.bluemix.net'
option = webdriver.ChromeOptions()
option.add_argument('--disable-notifications')
option.add_argument("--mute-audio")
option.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 "
                    "(KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")

driver = webdriver.Chrome(options=option)


def audio_to_text(path):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://speech-to-text-demo.ng.bluemix.net")
    time.sleep(3)
    # root = browser.find_element(By.ID, 'root').find_elements_by_class_name('dropzone _container '
    #                                                                        '_container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(path)
    # Audio to text is processing
    time.sleep(5)
    text = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[7]/div/div/div/span').text
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return text


def save_file(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


driver.get(website)
driver.maximize_window()
time.sleep(5)
recaptcha = driver.find_element(By.XPATH, '//*[@id="recaptcha1"]')
time.sleep(2)
recaptcha_click = recaptcha.find_element(By.TAG_NAME, 'iframe')
time.sleep(1)
recaptcha_click.click()
time.sleep(2)
all_iframes_len = driver.find_elements(By.TAG_NAME, 'iframe')
time.sleep(1)
audio_btn_found = False
audio_btn_index = -1
for index in range(len(all_iframes_len)):
    driver.switch_to.default_content()
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delay_time)
    try:
        audio_btn = driver.find_element(By.ID, 'recaptcha-audio-button') or \
                   driver.find_element(By.ID, 'recaptcha-anchor')
        audio_btn.click()
        audio_btn_found = True
        audio_btn_index = index
        break
    except Exception as e:
        pass
if audio_btn_found:
    try:
        href = driver.find_element(By.ID, 'audio-source').get_attribute('src')
        audio_file = requests.get(href, stream=True)
        save_file(audio_file, "audio.mp3")
        audio_text = audio_to_text("C:/Users/hp specter/Desktop/Indianproj/audio.mp3")
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[audio_btn_index]
        driver.switch_to.frame(iframe)
        respond = driver.find_element(By.ID, 'audio-response')
        respond.send_keys(audio_text)
        respond.send_keys(Keys.ENTER)
    except:
        pass
"""
time.sleep(3)

doctor = Select(driver.find_element(By.XPATH, '//*[@id="form-doctor"]'))
doctor.select_by_value(2)
time.sleep(1)
name = driver.find_element(By.XPATH, '//*[@id="form-name"]')
name.send_keys("Micheal David")
time.sleep(1)
email = driver.find_element(By.XPATH, '//*[@id="form-email"]')
email.send_keys("madtech@gmail.com")
time.sleep(1)
phone = driver.find_element(By.XPATH, '//*[@id="form-phone-number"]')
phone.send_keys("0923467687865")
time.sleep(1)
text = driver.find_element(By.XPATH, '//*[@id="form-comments"]')
text.send_keys("good job")
time.sleep(1)
send = driver.find_element(By.XPATH, '//*[@id="contact-form"]/div[2]/div[6]/button')
send.click()
"""
"""
word = "dentist los angeles"
browser = webdriver.Chrome()
browser.get("https://www.google.com")
search = browser.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
search.send_keys(word)
search.send_keys(Keys.ENTER)
browser.maximize_window()
more_websites = browser.find_element(By.XPATH, "//*[contains(text(), 'More places')]")
more_websites.click()
website = browser.find_element(By.XPATH, "//*[contains(text(), 'Website')]")
website.click()
contact = browser.find_element(By.XPATH, "//*[contains(text(), 'Contact')]")
contact.click()
"""
