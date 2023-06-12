"""
                    Goal: get all bill .pdf files from the site
"""

import configparser
from os.path import join, exists
from os import makedirs
from os import getlogin
from time import sleep
from datetime import date
# coloroma import and initalization
from colorama import init
init()

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# ======================================  CLASS STARTER  ===============================================================


# todo: add the following grep command to check if the bill is already downloaded
# todo: according to the Számlaszám e.g 121100321463
# todo: make a method to check this.
# todo: instead of allways creating new folders like e.g. DijnetSzamlak_2023-06-12-ig there should be only one file
# todo: that is always updated. + a .txt file should be created and then updated that keeps track when was this done.

class BillDownloader(object):
    """ Class for handling the bill download """

    bill_list = 0
    provider_list = []
    provider_list_bill_row_count = 0
    folder_name = "DijnetSzamlak"

    def __init__(self, url, driver_path, user_name, passwd, base_folder_path):
        self.driver_path = driver_path
        self.url = url
        self.user_name = user_name
        self.passwd = passwd
        self.base_folder_path = base_folder_path
        # self.wait = WebDriverWait(self.driver, 60)

    def starter_driver(self):                                                                                           #1
        """driver is used to get the provider list to be able to set the down load folder later"""
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        print("starter_driver: ", self.driver)

    def driver(self):
        """"""
        options = Options()
        options.add_experimental_option('prefs', {"download.default_directory": self.provider_folder_path})
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def open(self):                                                                                                     #2
        print("self.driver: ", self.driver)
        self.driver.get(self.url)
        self.driver.maximize_window()

    def close(self):                                                                                                    #8
        self.driver.close()

    def wait(self):                                                                                                     #3
        self.wait = WebDriverWait(self.driver, 60)

    def login(self):                                                                                                    #4
        sleep(1)
        login_button = self.wait.until(EC.visibility_of(self.driver.find_element(By.ID, "login-btn")))
        login_button.click()
        sleep(1)
        username_field = self.wait.until(EC.visibility_of(self.driver.find_element(By.NAME, "username")))
        username_field.send_keys(self.user_name)
        pwd_field = self.driver.find_element(By.NAME, "password")
        pwd_field.send_keys(self.passwd)
        pwd_field.send_keys(Keys.ENTER)

    def cookie_ok(self):                                                                                                #5
        try:
            sleep(1)
            self.wait.until(EC.visibility_of(self.driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection")))        # PROBLEMA: nem mindig jelenik meg a cookie. Hogyan lehet
            cookie = self.driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection")
            cookie.click()
        except NoSuchElementException as e:
            print("There is no cookie: ", e)

    def got_to_bills(self):                                                                                             #6
        sleep(1)
        bills_button = self.wait.until(EC.visibility_of(self.driver.find_element(By.XPATH, '//*[@id="logged_menu"]/li[3]/a')))
        bills_button.click()

    def get_provider_list(self):                                                                                        #7
        """gets all the providers currently listed for the user in Dijnet.hu"""
        # self.wait.until(EC.element_to_be_clickable)
        sleep(1)
        select_text = self.driver.find_elements(By.NAME, "szlaszolgnev")
        self.provider_list = select_text[0].text.split('\n')

    def create_provider_folder(self, base_folder_path, folder_name, provider_name):
        """Create a new directory because it does not exist"""
        self.provider_folder_path = join(base_folder_path, folder_name, provider_name.strip(" "))
        if not exists(self.provider_folder_path):
            makedirs(self.provider_folder_path)
        return

    def provider_selecter(self, provider):
        """ Selects the provider from the provider dropdown list """
        sleep(1)
        dropdown_option = self.wait.until(EC.visibility_of(
            self.driver.find_element(By.XPATH, '//*[contains(@value, "{}")]'.format(provider))))
        dropdown_option.click()
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

    def bill_row_counter(self):
        """returns the bill_row_count of how many bills belong to a provider (in a table). Will be used as rows after this."""
        self.bill_row_count = len(self.driver.find_elements(By.XPATH, '//table/tbody/tr'))
        print("self.bill_row_count", self.bill_row_count)

    def individual_bill_downloader(self, number):
        sleep(1)
        self.driver.implicitly_wait(1)
        # self.wait.until(
        #     EC.presence_of_element_located(self.driver.find_element(By.XPATH, "//table/tbody/tr[{}]/td[6]".format(number))))
        individual_bill = self.driver.find_element(By.XPATH, "//table/tbody/tr[{}]/td[6]".format(number))
        self.driver.execute_script("arguments[0].click();", individual_bill)
        # print("{} bill no. {} found".format(provider, number))
        sleep(1)
        # self.wait.until(EC.visibility_of(
        #     self.driver.find_element(By.XPATH, '//*[contains(@href, "/ekonto/control/szamla_letolt")]')))
        download_nav_link = self.driver.find_element(By.XPATH, '//*[contains(@href, "/ekonto/control/szamla_letolt")]')
        download_nav_link.click()
        sleep(1)
        # self.wait.until(EC.visibility_of(
        #     self.driver.find_element(By.XPATH, '//*[contains(@href, "szamla_pdf")]')))
        download_bill = self.driver.find_element(By.XPATH, '//*[contains(@href, "szamla_pdf")]')
        download_bill.click()

    def downloader(self, count, provider):
        """This is the actual bill downloader"""
        print("provider: ", provider)
        print("count: ", count)
        for number in range(1, (count + 1)) :
            # self.wait.until(EC.element_to_be_clickable -t is meg lehet csinálni saját methodusnak
            self.individual_bill_downloader(number)
            self.got_to_bills()
            self.provider_selecter(provider.strip(" "))


    def download_controller(self):
        """ Controlls the   1. folder structure creation (if needed)    2. actual bill downloading """
        print("self.provider_list: ", self.provider_list)
        #[' BKM NONPROFIT Zrt.', 'DFaktorház Zrt.', 'Díjbeszedő Zrt.', 'FCSM Zrt.', 'FV Zrt.','Társ.díj felosz', 'Vodafone Cégcsoport']
        for provider in self.provider_list:
            print(provider)
            BillDownloader.create_provider_folder(self, self.base_folder_path, self.folder_name, provider.strip(' '))
            BillDownloader.driver(self)
            self.open()
            self.login()
            self.cookie_ok() # The cookie not always appears, and this causes an element not found error
            self.got_to_bills()
            self.provider_selecter(provider.strip(" "))
            self.bill_row_counter()
            self.downloader(self.bill_row_count, provider)
            self.driver.close()

    def controller(self):
        """Gets the list of the provider and then closes the driver, so the path for the different providers can be
        set with """
        BillDownloader.starter_driver(self)
        BillDownloader.wait(self)
        self.open()
        self.login()
        self.cookie_ok()
        self.got_to_bills()
        self.get_provider_list()
        self.close()
        self.download_controller()



def get_info(ini_path, section, key):
    """
    Gets the information needed from the ini files. Needed because the chromedriver has different paths on different
    machines
    """
    config = configparser.ConfigParser()
    config.read(ini_path)
    Key = config[section]
    value = Key[key]
    return value

# ===================================================================
# =================  Main part starts here  =========================
# ===================================================================

ini_path = r'./bill_getter.ini'
url_path = r"https://www.dijnet.hu/"
# ini_path = r'C:\Users\A87484215\PycharmProjects\IndividualScripts\IndividualScripts\billingProvider\billingProvider.ini'   # for console run

# todo: get the path for the Work and Win machine too.
# todo: correct the bill_getter.ini with the above mentioned paths.
user = getlogin()
""" set driver path and basefolder path """
if user == 'zsolt':
    base_folder_path = r"/home/zsolt/Desktop/Dijnet/DijnetSzamlak_{}-ig".format(date.today())
    driver_path = get_info(ini_path, 'chromeDriver', user)
# elif user == 'zsolt':
#     base_folder_path = r"".format(date.today())
# else:
#     base_folder_path = r"".format(date.today())
print("User: ", user)
print("driver path: ", driver_path)

login_passwd = get_info(ini_path, 'userInfo', "passwd")
login_user = get_info(ini_path, 'userInfo', "user")

if __name__ == "__main__":
    my_instance = BillDownloader(url_path, driver_path, login_user, login_passwd, base_folder_path)
    my_instance.controller()
