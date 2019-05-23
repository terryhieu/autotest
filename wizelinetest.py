from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as Ex
import unittest
import logging, sys

logger = logging.getLogger()
logger.level = logging.INFO
logger.addHandler(logging.StreamHandler(sys.stdout))

class WizelineTest(unittest.TestCase):
    USERNAME = ''
    PASSWORD = ''
    URL = ''

    def setUp(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--test-type")        
        self.driver = webdriver.Chrome(chrome_options=self.options)

        self.startPage()

    def startPage(self):                
        strLoginLinkLoc = '/html/body/div[2]/div[1]/div[1]/div/form/input[3]' #Login locator

        logger.info('Open the web page with url: ' + self.URL)
        self.driver.get(self.URL)
        try:
            wait = WebDriverWait(self.driver, 20)
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, strLoginLinkLoc))
            )
        except:
            self.driver.close()
            raise Exception('Failed to start main page')
        
        logger.info('Finish open the page with url: ' + self.URL)

    def cleanup(self):        
        self.driver.quit()

    def tearDown(self):
        self.cleanup()

    def login(self):
        strLoginLinkLoc, login_link = '', ''
        strUsrLoc, strPwdLoc, strLoginBtnLoc = '', '', ''
        usr_text_box, pwd_text_box, login_btn = '', '', ''
        
        strUsrLoc = '//*[@id="user-name"]' #User xpath textbox
        strPwdLoc = '//*[@id="password"]' #Pwd xpath textbox
        strLoginBtnLoc = '//input[@type="submit"]' #/html/body/div[2]/div[1]/div[1]/div/form/input[3]' #login button        

        logger.info('Start login user: ' + self.USERNAME)
        
        #2. Enter username/password in login page
        usr_text_box = self.driver.find_element_by_xpath(strUsrLoc)
        usr_text_box.send_keys(self.USERNAME)

        pwd_text_box = self.driver.find_element_by_xpath(strPwdLoc)
        pwd_text_box.send_keys(self.PASSWORD)

        # click submit button
        login_btn = self.driver.find_elements_by_xpath(strLoginBtnLoc)[0]
        login_btn.click()

        #wait the page completely loaded
        # strLoginElementConfirmLoc = '/html/body/div[1]/div[2]/div[1]/div[2]/a/svg/path' #shopping cart
        # wait = WebDriverWait(self.driver, 20)
        # element = wait.until(
        #         EC.element element_to_be_clickable((By.XPATH, strLoginElementConfirmLoc))
        # )

        logger.info('Login successfully')

    def _navigate_inventory_page(self):
        self.driver.get('https://www.saucedemo.com/inventory.html')

    def _add_some_cart(self):
        strAddToCartLoc1, strAddToCartLoc2 = '', ''
        strAddToCartLoc1 = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[3]/button'
        login_btn = self.driver.find_elements_by_xpath(strAddToCartLoc1)[0]
        login_btn.click()
        

    def _checkout_cart(self):
        #click shopping cart icon
        # strShoppingCartLoc = '/html/body/div[1]/div[2]/div[1]/div[2]/a/svg/path'
        # shopping_cart_btn = self.driver.find_elements_by_xpath(strShoppingCartLoc)[0]
        # shopping_cart_btn.click()
        # Go to checkout page
        self.driver.get('https://www.saucedemo.com/cart.html')

        strCheckOutLoc = '/html/body/div[1]/div[2]/div[3]/div/div[2]/a[2]'
        checkout_btn = self.driver.find_elements_by_xpath(strCheckOutLoc)[0]
        checkout_btn.click()

        strLoc = '//*[@id="first-name"]'
        text_box = self.driver.find_element_by_xpath(strLoc)
        text_box.send_keys('Hieu')
                
        strLoc = '//*[@id="last-name"]'
        text_box = self.driver.find_element_by_xpath(strLoc)
        usr_text_box.send_keys('Phan')

        strLoc = '//*[@id="postal-code"]'
        text_box = self.driver.find_element_by_xpath(strLoc)
        usr_text_box.send_keys('70000')
        
        #Continue
        strLoc = '/html/body/div[1]/div[2]/div[3]/div/div[2]/a[2]'
        action_btn = self.driver.find_elements_by_xpath(strLoc)[0]
        action_btn.click()

        #Finish
        strLoc = '/html/body/div[1]/div[2]/div[3]/div/div[2]/div[8]/a[2]'
        action_btn = self.driver.find_elements_by_xpath(strLoc)[0]
        action_btn.click()

    
    def test_user_order(self):        
        strThankYouLoc = '/html/body/div[1]/div[2]/div[3]/h2'
        confirm_order_text = 'THANK YOU FOR YOUR ORDER' 

        self.login()
        self._navigate_inventory_page()
        self._add_some_cart()
        self._checkout_cart()

        #4. finally assert if the note add successfully        
        element = self.driver.find_element_by_xpath(strThankYouLoc)
        thank_you_title = element.get_attribute('innerHTML')   

        logger.info('Finish to test user add note')            
        self.assertIn(confirm_order_text, thank_you_title, 'Failed to order')

if __name__ == '__main__':
    WizelineTest.USERNAME = 'standard_user'
    WizelineTest.PASSWORD = 'secret_sauce'
    WizelineTest.URL = 'https://www.saucedemo.com/index.html'
    
    unittest.main(verbosity=2)