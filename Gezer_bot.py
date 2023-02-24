import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import base64


class GezerBot:
    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")  # maximize window
        chrome_options.add_experimental_option("detach", True)  # prevent selenium from closing browser
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    def open(self) -> None:
        """
        Open Gezer website
        :return: None
        """
        self.driver.get('https://gezer1.bgu.ac.il/meser/login.php')

    def login(self, user_name: str, password: str, student_id: str) -> None:
        """
        Login to Gezer website
        :param student_id:
        :param password: Student's password
        :param user_name: Student's username
        :return: None
        """
        # --- Login ------
        self.driver.find_element(By.ID, value='username').send_keys(user_name)
        self.driver.find_element(By.ID, value='pass').send_keys(password)
        self.driver.find_element(By.ID, value='id').send_keys(student_id)
        self.driver.find_element(By.NAME, value="ok").click()
        self.driver.find_element(By.NAME, value="agree").click()

    def find_random_test(self) -> None:
        """
        Find a random test to send the re encoded message
        :return: None
        """
        table = self.driver.find_element(By.XPATH, value="/html/body/form[2]/table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 5:
                cells[5].click()
                break

    def get_test(self, course_id: str, moed: str) -> None:
        """
        Download the test
        :param moed: 1 2 3 depend on the test of the semester
        :param course_id: The desired course number
        :return: None
        """
        download_path = '/html/body/div[6]/div/div[1]/form/input[2]'
        download_bottom = self.driver.find_element(By.XPATH, value=download_path)
        # get the encoded message
        encoded_message = download_bottom.get_attribute("value")
        decoded_message = base64.b64decode(encoded_message).decode('utf-8')
        decoded_list = decoded_message.split(":")
        # insert the course you want to check
        decoded_list[-3] = course_id
        decoded_list[-1] = moed
        decoded_message = ":".join(decoded_list)
        # encode the new message
        encoded_message = base64.b64encode(decoded_message.encode('utf-8')).decode()
        # replace the message at the HTML
        self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", download_bottom, encoded_message)
        self.driver.find_element(By.XPATH, value="/html/body/div[6]/div/div[1]/form/input[1]").click()


def moed_validation(moed: str):
    if moed in {'1', 'a', 'A'}:
        return '1'
    if moed in {'2', 'b', 'B'}:
        return '2'
    if moed in {'3', 'c', 'C'}:
        return '3'
    raise Exception("illegal Moed")


def main():
    parser = argparse.ArgumentParser(description='Gezer script, insert <user_name> <password> <id> <course_id>')
    parser.add_argument("user_name", help="student username")
    parser.add_argument("password", help="student password")
    parser.add_argument("id", help="student id")
    parser.add_argument("course_id", help="course id")
    parser.add_argument("moed", help="insert 1 for moed A, 2 for moed B and 3 for moed C")
    args = parser.parse_args()
    bot = GezerBot()  # init bot
    bot.open()  # connect to Gezer website
    bot.login(args.user_name, args.password, args.id)  # login
    bot.find_random_test()
    bot.get_test(args.course_id, moed_validation(args.moed))  # download test


if __name__ == "__main__":
    main()
