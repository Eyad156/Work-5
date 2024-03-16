from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import update_logs
#  auto install webdriver
class Insta():
    def __init__(self):
        try:            
            chrome_options = webdriver.ChromeOptions()            
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument('headless')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-notifications')     
            
            self.driver = webdriver.Chrome(options=chrome_options)
            url = 'https://www.instagram.com/'
            self.driver.get(url) 
            print('INFO - Started chrome')       
        except Exception as e:
            print('ERROR - Exception while opening chrome')
            print('INFO - Make sure you have chrome installed in your system')

    def login(self,user,pas,campaignId):
        # try:

        usernameField = WebDriverWait(self.driver,15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'input._aa4b._add6._ac4d[name="username"]'))
        )

        usernameField.send_keys(user)

        passwordField = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'input._aa4b._add6._ac4d[name="password"]'))
        )

        passwordField.send_keys(pas)

        loginButton = WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'button._acan._acap._acas[type="submit"]'))
        )
        time.sleep(2)
        loginButton.click()
        update_logs.update_logs('Trying to login',campaignId)
        time.sleep(20)
        print('INFO - Logged in')
        # except Exception as e:
        #     print('ERROR - Exception occured while login : ')
        #     print('ERROR - Failed to login')

    def openNewTab(self,link,new_tab_number):

        # opening another tab in chrome
        self.driver.execute_script("window.open('');")
        # switiching to the new tab
        self.driver.switch_to.window(self.driver.window_handles[new_tab_number])
        # passing location link to new tab
        self.driver.get(link)

    def search_by_hashtag(self,hashtag):        
        url = f'https://www.instagram.com/explore/tags/{hashtag}/'
        self.openNewTab(url,1)
        time.sleep(5)

    def comment_post(self,comment_status,limit,comment_words,dm_status,dm_words,campaignId):
        try:
            if comment_status:

                picture_link = []
                loop_range = 0
                if limit > 12:
                    loop_range = limit % 12
                print(loop_range)

                for i in range(loop_range+1):            
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)

                try:
                    picture_div = self.driver.find_elements(By.CSS_SELECTOR,'div._aabd._aa8k._al3l a')
                    update_logs.update_logs('Logged in',campaignId)
                except Exception as e:
                    update_logs.update_logs('Failed to login',campaignId)
                    print(f'FAILED TO LOGIN : {str(e)}')
                
                else:
                
                    for pic in picture_div:
                        picture_link.append(pic.get_attribute("href"))        

                    print(picture_link)
                    # opening new tab, this tab would be third tab with index = 2
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[2])
                                
                    for i in picture_link:
                    
                        self.driver.get(i)
                        time.sleep(2)                

                        if comment_status:              
                            # when clicked on comment section , it loads new html
                            # when try to access this element again to pass keys
                            # it raises stale element exception. to resolve this issue 
                            # here's a workaround to avoid this
                            try:
                                comment_textarea = WebDriverWait(self.driver,5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'textarea[aria-label="Add a comment…"]'))
                                )
                                comment_textarea.send_keys(comment_words)
                                print('Commented')
                            except StaleElementReferenceException:                        
                                try:
                                    comment_textarea = WebDriverWait(self.driver,5).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR,'textarea[aria-label="Add a comment…"]'))
                                    )
                                    comment_textarea.send_keys(comment_words)
                                    print('Commented')
                                except StaleElementReferenceException:                          
                                    pass
                            
                            time.sleep(2)        

                            post_comment_button = WebDriverWait(self.driver,5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR,'div._aidp div'))
                            )
                            post_comment_button.click()

                            time.sleep(3)  

                        if dm_status:
                            # span cass = xt0psk2 > div > a
                            account_span = WebDriverWait(self.driver,5).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR,'span.xt0psk2 div a'))
                            )
                            # account_span = self.driver.find_element(By.CSS_SELECTOR,'span.xt0psk2 div a')
                            # account_link = account_span.get_attribute("href")
                            username = account_span.text

                            self.driver.get(f"https://www.instagram.com/{username}")
                            time.sleep(5)
                            # self.driver.get(account_link)

                            try:
                                message_button = WebDriverWait(self.driver,5).until(
                                    EC.presence_of_element_located((By.XPATH,'//div[text()="Message"]'))
                                )
                                message_button.click()
                                time.sleep(7)
                                
                                message_text_area = WebDriverWait(self.driver,5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'div[aria-label="Message"]'))
                                )
                                message_text_area.send_keys(dm_words)
                                time.sleep(3)

                                send_button = WebDriverWait(self.driver,5).until(
                                    EC.element_to_be_clickable((By.XPATH,'//div[text()="Send"]'))
                                )
                                send_button.click()
                                print('Messaged')
                                time.sleep(3)
                            except Exception as e:
                                print('User cant be messaged')
                                continue
                            # # check if notification shows up
                            # # only check first time
                            # if notification_check:
                            #     try:
                            #         not_now_button = WebDriverWait(self.driver,5).until(
                            #             EC.presence_of_element_located((By.CSS_SELECTOR,'button._a9--._ap36._a9_1'))
                            #         )
                            #         not_now_button.click()
                            #         notification_check = 0
                            #         print('Not Now Notification appeared and clicked not now')
                            #     except:
                            #         print('Not Now Notification does not appear')


                            # # send_dm_button = WebDriverWait(self.driver,5).until(
                            # #     EC.element_to_be_clickable((,''))
                            # # )
            self.driver.quit()                
            update_logs.update_logs('Processing Finished',campaignId)

        except Exception as e:
            print('EXCEPTION OCCUERED')
            print(e)
