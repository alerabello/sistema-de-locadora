import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SeleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")

    def test_login_invalido(self):
        driver = self.driver
        email_input = driver.find_element(By.NAME, "email")
        senha_input = driver.find_element(By.NAME, "senha")

        email_input.send_keys("teste@invalido.com")
        senha_input.send_keys("senhaerrada")
        senha_input.send_keys(Keys.RETURN)

        time.sleep(1)
        self.assertIn("Login inválido", driver.page_source)

    def test_login_valido(self):
        driver = self.driver

        email_input = driver.find_element(By.NAME, "email")
        senha_input = driver.find_element(By.NAME, "senha")

        email_input.send_keys("admin@email.com")
        senha_input.send_keys("admin123")
        senha_input.send_keys(Keys.RETURN)

        time.sleep(1)
        self.assertIn("Bem-vindo", driver.page_source)

    def tearDown(self):
        self.driver.quit()