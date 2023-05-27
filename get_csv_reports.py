import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Prompt user for login credentials
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Set up Chrome WebDriver in headless mode
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get("https://sicredi.signanywhere.com/Account/Login")

# Find the username and password input fields and enter the credentials
username_field = driver.find_element(By.ID, "Email")
password_field = driver.find_element(By.ID, "Password")

username_field.send_keys(username)
password_field.send_keys(password)

# Delay before clicking the login button
print("Thank you, trying to log in...")
time.sleep(5)

# Submit the login form
login_button = driver.find_element(By.ID, "loginButton")
login_button.click()

# Wait for the "Documentos" button to be clickable
documentos_button_locator = (By.CSS_SELECTOR, "a[href='/Inbox/Index']")
WebDriverWait(driver, 6).until(EC.element_to_be_clickable(documentos_button_locator))

# Click on the "Documentos" button
print("Successfully logged. Wait for just 10 more seconds...")
documentos_button = driver.find_element(*documentos_button_locator)
documentos_button.click()

# Wait for the Inbox page to load
inbox_page_locator = (By.ID, "buttonExportAsCsv")
WebDriverWait(driver, 7).until(EC.presence_of_element_located(inbox_page_locator))

# Delay before clicking the exportar button
time.sleep(5)

# Click the "Exportar como CSV" button
export_button = driver.find_element(*inbox_page_locator)
export_button.click()

# Delay before closing the webdriver
time.sleep(3)

# Close the browser
driver.quit()

# Print success message
print("Automation completed successfully!")
