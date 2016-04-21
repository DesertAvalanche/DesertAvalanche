# http://selenium-python.readthedocs.org/getting-started.html
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from server import app_db

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    # http://stackoverflow.com/questions/5387299/python-unittest-testcase-execution-order
    # Test Title present
    def test_1(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        self.assertIn("Desert Avalanche", driver.title)

    # Test Sign up
    def test_2(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_1')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_1@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_password')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test 3 - Log in
    def test_3(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Log in').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_1')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test Make a new group
    def test_4(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Log in').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_1')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password')
        driver.find_element_by_class_name('btn-lg').click()
        driver.find_element_by_link_text('Manage Your Groups').click()

        driver.find_element_by_id('groupname').send_keys('mygroup')
        # http://sqa.stackexchange.com/a/2697
        driver.find_element_by_xpath("//button[contains(.,'Add')]").click()
        self.assertIn("mygroup</a>", driver.page_source)

    # Test Make a new group
    def test_5(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Log in').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_1')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password')
        driver.find_element_by_class_name('btn-lg').click()
        driver.find_element_by_link_text('Manage Your Groups').click()

        driver.find_element_by_link_text('mygroup').click()

        self.assertIn("Events:", driver.page_source)

    # Test Make a new event
    def test_6(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Log in').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_1')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password')
        driver.find_element_by_class_name('btn-lg').click()
        driver.find_element_by_link_text('Manage Your Groups').click()

        driver.find_element_by_link_text('mygroup').click()

        driver.find_element_by_id('eventname').send_keys('Cool party')
        # http://sqa.stackexchange.com/a/2697
        driver.find_element_by_xpath("//button[contains(.,'Add')]").click()
        self.assertIn("Cool party</a>", driver.page_source)

    # Test Sign up a second user
    def test_7(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_2')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_2@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password2')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_password2')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test Add user to group
    def test_8(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Log in').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_1')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password')
        driver.find_element_by_class_name('btn-lg').click()
        driver.find_element_by_link_text('Manage Your Groups').click()

        driver.find_element_by_link_text('mygroup').click()

        driver.find_element_by_id('username').send_keys('user_2')
        # http://sqa.stackexchange.com/a/2697
        # http://stackoverflow.com/questions/15788679/selenium-xpath-how-to-select-last-matching-element-in-a-table
        # http://stackoverflow.com/a/11958692/2033574
        driver.find_element_by_xpath("(//button[contains(.,'Add')])[last()]").click()
        self.assertIn("user_2</a>", driver.page_source)

    # Test Vote
    def test_9(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Log in').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_1')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_password')
        driver.find_element_by_class_name('btn-lg').click()
        driver.find_element_by_link_text('Manage Your Groups').click()

        driver.find_element_by_link_text('mygroup').click()
        driver.find_element_by_link_text('Cool party').click()
        driver.find_element_by_link_text('Vote Now').click()
        driver.find_element_by_id('choice').send_keys('McDonalds')

        # http://sqa.stackexchange.com/a/2697
        driver.find_element_by_xpath("//button[contains(.,'Submit choice')]").click()
        self.assertIn("has chosen <strong>McDonalds</strong>", driver.page_source)

    # Test Sign up as user u3
    def test_u3(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_u3')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_u3@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_passwordu3')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_passwordu3')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test Sign up as user u4
    def test_u4(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_u4')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_u4@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_passwordu4')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_passwordu4')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test Sign up as user u5
    def test_u5(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_u5')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_u5@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_passwordu5')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_passwordu5')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test Sign up as user u6
    def test_u6(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_u6')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_u6@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_passwordu6')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_passwordu6')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test Sign up as user u7
    def test_u7(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_u7')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_u7@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_passwordu7')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_passwordu7')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    # Test Sign up as user u8
    def test_u8(self):
        driver = self.driver
        driver.get("http://localhost:5000/")
        driver.find_element_by_link_text('Sign up').click()
        elem = driver.find_element_by_id('username')
        elem.send_keys('user_u8')
        elem = driver.find_element_by_id('email')
        elem.send_keys('user_u8@user.com')
        elem = driver.find_element_by_id('password')
        elem.send_keys('secret_passwordu8')
        elem = driver.find_element_by_id('repeat_password')
        elem.send_keys('secret_passwordu8')
        driver.find_element_by_class_name('btn-lg').click()
        self.assertIn("Manage Your Groups", driver.page_source)

    def tearDown(self):
        self.driver.close()
        pass

if __name__ == "__main__":
    app_db.drop_all()
    app_db.create_all()
    unittest.main()

# Test 2 - User 'a' can log in
# Click Log in
# 
# elem = driver.find_element_by_name("q")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
print driver.page_source
driver.close()