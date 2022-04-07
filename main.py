import time
import datetime

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import telebot
# from telebot import types

from auth_data import token

# Дравер работы прасинга
def Driver(url):

    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")

    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
                                           )
    driver = webdriver.Chrome(executable_path='C:\\Users\\User\\Documents\\ALL FOLDS\\FLASK_PROJECTS\\SOME_PROJECT\\pars_work_1\\chromedriver.exe', options=chrome_options)
    driver.get(url=url)

    action = ActionChains(driver)

    #Auth
    auth(driver, '065110421', 'zaschita24')
    #hestory
    hestory(driver, action)

    driver.close()
    driver.quit()

def auth(driver, numberphone, password):
    #логин
    login_input = driver.find_element_by_name('phone')
    login_input.clear()
    login_input.send_keys(numberphone)
    #пароль
    password_input = driver.find_element_by_name('password')
    password_input.clear()
    password_input.send_keys(password)
    #капча
    img = driver.find_element_by_id('captcha').screenshot(f'cap.png')
    cap = str(input())
    cap_img = driver.find_element_by_name('captcha:captchaText')
    cap_img.clear()
    cap_img.send_keys(cap)
    time.sleep(2)
    #Кнопка войти
    driver.find_element_by_id("id4").click()
    time.sleep(3)

# Самая близкая датам
def best_date(dates, time_now):
    offset = datetime.timezone(datetime.timedelta(hours=3))
    current_datetime = datetime.datetime.now(offset)
    result = []
    for i in dates:
        date = datetime.datetime.strptime(i.text.strip(), '%d.%m.%Y')
        delta = date - current_datetime.replace(tzinfo=None)
        result.append((abs(delta.days), date))
    result.sort(key=lambda x: x[0])

    best_date_num = datetime.datetime.strptime(str(result[0][1]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
    result.clear()
    same_time = datetime.datetime.strptime(time_now.text.strip(), '%d.%m.%Y - %H:%M').strftime('%d.%m.%Y')

    if same_time == best_date_num:
        return 'back'
    else:
        return best_date_num

def hestory(driver, action):
    a = driver.find_elements_by_class_name("action")
    k = 0
    for i in a:
        #забирание настоящего времени приёма
        soup = BeautifulSoup(driver.page_source, 'lxml')
        time.sleep(2)
        times = soup.find_all('a', class_='action')
        time_now = times[k]

        time.sleep(2)
        i.click()
        time.sleep(5)

        #Изменить [кнопка] (работает только таким образом)
        for p in range(2):
            action.send_keys(Keys.TAB)
        action.send_keys(Keys.ENTER)
        action.perform()
        time.sleep(2)

        driver.find_element_by_xpath('//*[@title="ДД.ММ.ГГГГ"]').click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        dates = soup.find_all('li', class_='option')


        #Лучшая дата
        best_date_num = best_date(dates, time_now)
        if best_date_num == 'back':
            driver.find_elements_by_tag_name('button')[1].click()
        else:
            driver.find_element_by_xpath(f'//*[@title="{best_date_num}"]').click()
            time.sleep(2)

            #Самое раннее время
            driver.find_element_by_xpath('//*[@title="ЧЧ:ММ"]').click()
            action.send_keys(Keys.TAB)
            action.send_keys(Keys.ENTER)
            action.perform()

            #Завершение, забратие талона
            driver.find_elements_by_tag_name('button')[2].click()
            time.sleep(2)
            #cкрин талона
            driver.find_elements_by_class_name('ng-star-inserted')[1].screenshot('talon.png')
            driver.find_elements_by_class_name('logo-wrapper')[0].click()

            time.sleep(10)

        k += 1


# Main
def main():
    Driver('https://mmc.mos.ru/client-office/security/auth-rvg/login/check?6&service=http://mmc.mos.ru/client-office/auth/signin-cas')


class Bot:
    def __init__(self, TOKEN):
        bot = telebot.TeleBot(TOKEN)


        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id, '*Привет 👋*')

        bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()







