from selenium import webdriver
import time
import constants
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
# import update_logs
import os

class Facebook():
    # def __init__(self):
    #     print('Hello World')

    #     # Create FirefoxOptions object
    #     firefox_options = webdriver.FirefoxOptions()

    #     # Add options for Firefox
    #     # firefox_options.add_argument("--start-maximized")
    #     # firefox_options.add_argument('--headless')
    #     firefox_options.add_argument('--disable-dev-shm-usage')
    #     firefox_options.add_argument('--disable-gpu')
    #     firefox_options.add_argument('--no-sandbox')
    #     firefox_options.add_argument('--disable-notifications')

    #     # Initialize the Firefox WebDriver with the specified options
    #     self.driver = webdriver.Firefox(options=firefox_options)
    #     url = 'https://www.facebook.com/'        
    #     self.driver.get(url) 
    #     print('INFO - Started chrome')

    def __init__(self):
        print('Hello Wolrd')
        # Create ChromeOptions object
        chrome_options = webdriver.ChromeOptions()
        # Add the --disable-notifications option        
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-notifications')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        url = 'https://www.facebook.com/'        
        self.driver.get(url) 
        print('INFO - Started chrome')       

    def login_fb(self, mail, word,campaignId):        
        # WebDriverWait(self.driver,5).until(
        #     EC.presence_of_element_located(())
        # )

        email = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,'email'))
        )        
        email.send_keys(mail)

        password = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.ID,'pass'))
        )        
        password.send_keys(word)

        login = WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable((By.NAME,'login'))
        )        
        login.click()
        # update_logs.update_logs('Trying to login',campaignId)
        time.sleep(10)

    def open_group_people(self, key):

        new_url = f'https://www.facebook.com/groups/{str(key)}/members'

        # self.driver.execute_script("window.open('');")
        # self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(new_url)
        time.sleep(5)

    def sendMessage(self,mess,limit,groupd_ids,campaignId):        
        login_status = True
        for i in groupd_ids:
            
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(1)            
            self.open_group_people(i)
            print(f'OPENED : {str(i)}')        
            prev = 0
            while True:

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                # try:
                # mylist = [my_elem.get_attribute("href") for my_elem in WebDriverWait(self.driver, 10).until(
                #     EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='xt0psk2']/a[@href]")))]
                mylist = [my_elem.get_attribute("href") for my_elem in WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span.xt0psk2 a[href]")))]

                # except Exception as e:
                #     print(f'COULD NOT LOGIN : {str(e)}')
                #     # update_logs.update_logs('Failed to login',campaignId)
                #     break

                if login_status:
                    # update_logs.update_logs('Logged In',campaignId)
                    login_status = False             
                mylist = list(dict.fromkeys(mylist))

                print(mylist)
                
                if len(mylist) > limit or len(mylist) == prev:
                    break
                prev = len(mylist)     
                time.sleep(5)
                        
            
            for link in mylist:
                # new_link = mylist[index]
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[2])
                self.driver.get(link)

                try:                    
                    time.sleep(2)
                    message_button = WebDriverWait(self.driver,10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,'div[aria-label="Message"]'))
                    )                    
                    self.driver.execute_script('arguments[0].click()', message_button)

                    print('Clicked Message Button')
                    time.sleep(5)
                    # write_area = WebDriverWait(self.driver, 10).until(
                    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'p.xat24cr.xdj266r')))
                    
                    popup = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.__fb-light-mode.x78zum5.xdt5ytf.x1iyjqo2.xs83m0k.x193iq5w')))
                                                                            
                    paragrapgh_element = WebDriverWait(popup, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'p.xat24cr.xdj266r')))

                    # xat24cr xdj266r
                    # for i in write_area:                        
                    time.sleep(1)
                    paragrapgh_element.send_keys(mess)                    
                    
                    click_send = WebDriverWait(popup, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,'div[aria-label="Send"]'))
                    )                    
                    self.driver.execute_script('arguments[0].click()', click_send)
                    
                    time.sleep(2)
                    print(f'MESSAGED : {link}')

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[1])
                except Exception as e:
                    print('Could not message')
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    continue
            
            self.driver.close()            
            self.driver.switch_to.window(self.driver.window_handles[0])
        
        self.driver.quit()
        # update_logs.update_logs('Processing Finished',campaignId)

    def open_group(self,key):
        new_url = f'https://www.facebook.com/groups/{str(key)}'
                
        self.driver.get(new_url)    

    def write_comment(self,limit,text,pic_status,pic_path,groupd_ids,campaignId):
        login_status = True
        
        for post in groupd_ids:    
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(1)
            self.open_group(post)
            time.sleep(2)

            prev = 0
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)                                
                
                try:
                    feed_posts = WebDriverWait(self.driver,5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z'))
                    )                                
                
                except Exception as e:
                    print(f'Failed to login : {str(e)}')
                    # update_logs.update_logs('Failed to login',campaignId)
                    break

                if login_status:
                    # update_logs.update_logs('Logged In',campaignId)
                    login_status = False      
                print(len(feed_posts))
                if len(feed_posts) > limit or len(feed_posts) == prev:
                    break
                prev = len(feed_posts)
                        
            iteration = 0
            for post in feed_posts:                
                if post.text == '':
                    continue               

                iteration += 1
                if iteration == 1:                    
                    continue
                if iteration > limit + 2:
                    break
                try:
                    popup_status = False
                    comment_area = post.find_element(By.CSS_SELECTOR,'div.xzsf02u.x1a2a7pz.x1n2onr6.x14wi4xw.notranslate')                    
                    print('Comment area found')                    
                except Exception as e:                    
                    print('Could not find comment area')                    
                    print('Clicking comment button to open the popup')                                        
                    
                    comment_button = WebDriverWait(post,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'div[aria-label="Leave a comment"]'))
                    )
                    self.driver.execute_script('arguments[0].click()', comment_button)
                    time.sleep(2)
                    comment_popup = WebDriverWait(self.driver,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'div.x1n2onr6.x1ja2u2z.x1afcbsf.xdt5ytf.x1a2a7pz.x71s49j.x1qjc9v5.x1qpq9i9.xdney7k.xu5ydu1.xt3gfkd.x78zum5.x1plvlek.xryxfnj.xcatxm7.xrgej4m.xh8yej3[role="dialog"]'))
                    )

                    comment_area = WebDriverWait(comment_popup,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'div.xzsf02u.x1a2a7pz.x1n2onr6.x14wi4xw.notranslate'))
                    )

                    input_picture_tag = WebDriverWait(comment_popup,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'input.x1s85apg[type="file"]'))
                    )
                                        
                    popup_status = True

                else:                    
                    input_picture_tag = WebDriverWait(post,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'input.x1s85apg[type="file"]'))
                    )                    
                
                try:      
                    input_picture_tag.send_keys(pic_path)
                    time.sleep(1)
                    print('ATTACHED PICTURE')                    
                except Exception as e:
                    print('Could not attach picture')
                    print(e)
                
                try:
                    comment_area.send_keys(text)
                    time.sleep(1)
                    print('MESSAGED WRITTEN')
                except Exception as e:
                    print('Could not message')
                    print(e)
                
                if popup_status:
                    post_button = WebDriverWait(comment_popup,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'#focused-state-composer-submit div'))
                    )
                else:
                    post_button = WebDriverWait(post,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'#focused-state-composer-submit div'))
                    )

                try:
                    self.driver.execute_script('arguments[0].click()', post_button)
                    time.sleep(2)
                    print('CLICKED SEND COMMENT BUTTON')
                except Exception as e:                                            
                    print(f'CANT CLICK SEND COMMENT BUTTON : {str(e)}')            
            
                if popup_status:                
                    close_button = WebDriverWait(comment_popup,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'div[aria-label="Close"][role="button"]'))
                    )
                    self.driver.execute_script('arguments[0].click()', close_button)
                    popup_status = False
            
            if pic_status:
                os.remove(pic_path) 
            time.sleep(5)

            self.driver.close()            
            self.driver.switch_to.window(self.driver.window_handles[0])                

        self.driver.quit()
        # update_logs.update_logs('Processing Finished',campaignId)

    def publish_post(self,text,groupd_ids,campaignId,picture_status,picture_path):
        # xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe
        login_status = True
        for i in groupd_ids:
            
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(2)
            self.open_group(i)

            try:
                write_something = WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'div.xi81zsa.x1lkfr7t.xkjl1po.x1mzt3pk.xh8yej3.x13faqbe'))
                )
            except Exception as e:
                print(f'Failed to login : {str(e)}')
                # update_logs.update_logs('Failed to login',campaignId)
            
            else:
                
                write_something.click()
                if login_status:
                    # update_logs.update_logs('Logged In',campaignId)
                    login_status = False
                        
                time.sleep(2)
                # _1mf _1mj
                pop_up_write_something = WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'div._1mf._1mj'))
                )

                pop_up_write_something.send_keys(text)
                time.sleep(2)
                
                if picture_status:
                    post_pop_up = WebDriverWait(self.driver,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'div.x1n2onr6.x1ja2u2z.x1afcbsf.x78zum5.xdt5ytf.x1a2a7pz.x6ikm8r.x10wlt62.x71s49j.x1jx94hy.x1qpq9i9.xdney7k.xu5ydu1.xt3gfkd.x104qc98.x1g2kw80.x16n5opg.xl7ujzl.xhkep3z.x193iq5w[role="dialog"]'))
                    )

                    picture_button = post_pop_up.find_element(By.CSS_SELECTOR,'div[aria-label="Photo/video"][role="button"]')

                    self.driver.execute_script('arguments[0].click()', picture_button)
                    time.sleep(2)
                    
                    input_picture_tag = WebDriverWait(post_pop_up,5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'input.x1s85apg[type="file"]'))
                    )
                    input_picture_tag.send_keys(picture_path)                    
                
                    time.sleep(2)

                # aria-label="Post"
                post_button = WebDriverWait(self.driver,5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,'div[aria-label="Post"]'))
                )

                post_button.click()

                time.sleep(3)
                print(f'POSTED {str(i)}')
                self.driver.close()            
                self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.quit()
        # update_logs.update_logs('Processing Finished',campaignId)

if __name__ == '__main__':    
    inst = Facebook()
    inst.login_fb('Ayoub_ouahmane@outlook.fr','vamoscasa2005',True)
    # inst.login_fb(constants.FACEBOOK_EMAIL, constants.FACEBOOK_PASSWORD,True)        
    # inst.write_comment(12,'TESTING 12 images',True,r'C:\\Users\\junaid\\ss.jpg',[3264777000474266],True)
    # inst.publish_post('FAHAD ZAHEER',[3264777000474266,601675118132406])
    # inst.sendMessage('Hello',45,[2695021857482902],True)    
    inst.sendMessage('Hello',5,[3610841002567395],True)


    # inst.attach_picture()
    # inst.publish_post('Ola')
    # inst.write_comment('1921958148057880') #711691828950789
    # inst.open_group('3264777000474266')
    # inst.publish_post()


# <input accept="video/*,  video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv, image/*, image/heic, image/heif" class="x1s85apg" type="file">
# <div aria-label="Attach a photo or video" class="x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x3nfvp2 xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x3ajldb x194ut8o x1vzenxt xd7ygy7 xt298gk x1xhcax0 x1s928wv x10pfhc2 x1j6awrg x1v53gu8 x1tfg27r xitxdhh" role="button" tabindex="0"><i data-visualcompletion="css-img" class="x1b0d499 x1d69dk1" style="background-image: url(&quot;https://static.xx.fbcdn.net/rsrc.php/v3/yV/r/3Sd4hjvXASJ.png?_nc_eui2=AeGe4F9dBrgDNVlVyU47irx5RLm7nzju851EubufOO7znffXTqLVrY80Uc2BaHPXHHdA-eTCt3lzb93CWjv-N0La&quot;); background-position: 0px -1288px; background-size: 26px 1636px; width: 16px; height: 16px; background-repeat: no-repeat; display: inline-block;"></i><div class="x1ey2m1c xds687c xg01cxk x47corl x10l6tqk x17qophe x13vifvy x1ebt8du x19991ni x1dhq9h x1wpzbip x14yjl9h xudhj91 x18nykt9 xww2gxu" data-visualcompletion="ignore" role="none" style="inset: -8px;"></div></div>

# <input dir="ltr" aria-invalid="false" id=":r2:" class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4" type="text" value="" name="email">
# <input dir="ltr" aria-invalid="false" id=":r4:" class="x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x1uxerd5 x1fcty0u x132q4wb x1a8lsjc x1pi30zi x1swvt13 x9desvi xh8yej3 x15h3p50 x10emqs4" type="password" value="" name="pass">
    #span class = x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84

    # xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x1iyjqo2 x1gh3ibb xisnujt xeuugli x1odjw0f notranslate
    # xzsf02u x1a2a7pz x1n2onr6 x14wi4xw notranslate
