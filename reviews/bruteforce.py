from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

s = Service(executable_path="/usr/bin/local/geckodriver")
driver = webdriver.Chrome(service=s)

website = "http://127.0.0.1:5000/login"

driver.get(website)

title = ""

passwords = ["sdf", "sdfsdf", "pass", "xyz"]
i = 0

for passw in passwords:
    print(f"Aktuelles Passwort: {passw}")
    
    time.sleep(0.1)
    
    res = driver.find_elements(By.CLASS_Name, "form-control")
    print(f"Die Länge ist: {len(res)}")
    assert(len(res) == 2)
    
    res[0].clear()
    res[0].send_keys("Derk")
    res[1].clear()
    res[1].send_keys(passw)
    
    button = driver.find_elements(By.CLASS_NAME, "btn")
    button[0].click()
    
    print("Title page is: ", driver.title)
    
    if driver.title != "Login":
        print(f"Password found: {passw}")
        break
    
    driver.quit()