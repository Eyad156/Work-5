from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def download_img(url):
     # Set up Firefox options    
    firefox_options = Options()
    firefox_options.add_argument('--headless')

    driver = Firefox(options=firefox_options)
    # Run Firefox in headless mode (no GUI)        
    driver.get(url)
    with open('pic.png', 'wb') as file:
        file.write(driver.find_element(By.TAG_NAME,'img').screenshot_as_png)
