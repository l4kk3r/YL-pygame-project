# Данный скрипт создан для парсинга картинок с сайта littlealchemy
from selenium import webdriver



DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER)
for i in range(566, 896):
    driver.get(f'https://littlealchemy2.com/static/icons/{i}.svg')
    screenshot = driver.save_screenshot(f'./icons/{i}.png')
driver.quit()
