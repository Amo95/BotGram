from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys
import subprocess
import getpass


def info():
    """Code by DummyCoder
    Instagram: dummycod3r
    Twitter: @dummyCod3r_
    Github: amo95
    """

    print(info.__doc__)

def print_same_line(text):
    while True:
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()

def spin():
        while True:
            for cursor in '|/-\\':
                yield cursor


def start_spin():
    spinner = spin()
    for _ in range(10):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')


def main():
    info()

    opt = ["Login", "Close/Logout Browser", "Help", "Quit"]

    for num, op in enumerate(opt, start=1):
        print(f"[{num}] {op}")

    print("\nEnter option: ", end=" ")
    option = int(input())

    if option == (opt.index("Login") + 1):

        if sys.platform == "linux" or sys.platform == "linux2":
            subprocess.call("clear", shell=True)
        else:
            subprocess.call("cls", shell=True)

        print(f"\n{Color.BOLD}Login{Color.END}")
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        print("Wait a moment", end=" ")
        start_spin()

        hasht = input("\nEnter hashtag/s (separate multiple tags with space): ")
        hasht_split = hasht.split(" ")
        hashtags = hasht_split[:]


        ig = InstagramBot(username, password)
        ig.login()


        while True:
            try:
                # Choose a random tag from the list of tags
                tag = random.choice(hashtags)
                ig.like_photo(tag)

            except Exception:
                ig.closeBrowser()
                time.sleep(60)
                ig = InstagramBot(username, password)
                ig.login()

    elif option == (opt.index("Close/Logout Browser") + 1):
        pass

    elif option == (opt.index("Help") + 1):
        pass
    elif option == (opt.index("Quit") + 1):
        InstagramBot.quit()



class Color(object):
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class InstagramBot(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

        if sys.platform == "linux" or sys.platform == "linux2":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        try:
            @staticmethod
            def log():
                login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/']")
                login_button.click()
                time.sleep(2)

        except:
            login_button = driver.find_element_by_xpath("//a[@href='/accounts/emailsignup/']")
            login_button.click()
            time.sleep(2)
            log()

        username_element = driver.find_element_by_xpath("//input[@name='username']")
        username_element.clear()
        username_element.send_keys(self.username)

        passwd_element = driver.find_element_by_xpath("//input[@name='password']")
        passwd_element.clear()
        passwd_element.send_keys(self.password)
        passwd_element.send_keys(Keys.RETURN)

        
        time.sleep(3)


    def like_photo(self, hashtag):

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos

        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')

                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]

                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                time.sleep(random.randint(2, 4))
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(1)

            except Exception as e:
                time.sleep(2)
            unique_photos -= 1

    @staticmethod
    def quit():
        print("\nExiting...")
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except:
        sys.stdout()
        InstagramBot.quit()