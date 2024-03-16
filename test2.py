from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Run Firefox in headless mode (without GUI)

driver = webdriver.Firefox(options=options)
driver.get('https://google.com')
print(driver.title)

driver.quit()  # Don't forget to close the WebDriver when done
