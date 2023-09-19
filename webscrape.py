import time
import pymsgbox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# WORKS ONLY FOR GOOGLE CHROME FOR NOW

# Initialize the WebDriver
driver = webdriver.Chrome()

YOUR_USERNAME="write_your_usos_username_here(PESEL)"

YOUR_PASSWORD = "write_your_password_to_usos_here"

INTERVAL=3600 # default interval is set to 1 hour
# Example: INTERVAL=120  means interval is set to 2 minutes
 
# URL for the course page
course_url = "Paste in course's https://... address here"
# Example: course_url = "https://rejestracja.usos.uw.edu.pl/course.php?rg=0000-2023-OG-UN&group=0000-FOREIGN-OG&subject=0000-UEC-OG&cdyd=2023Z&course_id=517462&gr_no=1"


# Function to log in if not already logged in
def login():
    # Check if already logged in by looking for a logout button
    try:
        logout_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Wyloguj')]")
        print("Already logged in.")
        return  # No need to log in again
    except NoSuchElementException:
        pass  # Not logged in, continue with login process

    login_url = "https://logowanie.uw.edu.pl/cas/login?service=https%3A%2F%2Frejestracja.usos.uw.edu.pl%2Fcaslogin.php&locale=pl"
    driver.get(login_url)

    # Find the username and password input fields
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    # Enter username and password
    username_field.send_keys("YOUR_USERNAME")
    password_field.send_keys("YOUR_PASSWORD")

    # Submit the form
    password_field.send_keys(Keys.RETURN)

    # Wait for a few seconds to ensure the login is successful (you can adjust the time)
    time.sleep(1)  # Adjust the sleep time as needed

    # Explicitly navigate back to the specified course page
    driver.get(course_url)

def is_user_logged_in():
    try:
        user_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Zalogowany użytkownik:')]/b[@class='casmenu']")
        user_name = user_element.text
        print(f"Logged in as: {user_name}")
        return True
    except NoSuchElementException:
        print("Not logged in.")
        return False

# Function to check the website and display a popup message
def check_website():
    driver.get(course_url)

    # Check if the user is logged in
    if not is_user_logged_in():
        login()

    # Find the availability element
    try:
        availability_element = driver.find_element(By.XPATH, "//td[contains(@class, 'moregrey') and .//span[@class='registered']]")
        availability_text = availability_element.text.strip()
        availability_parts = availability_text.split("/")
        if len(availability_parts) == 2:
            registered_count = int(availability_parts[0])
            availability_threshold = int(availability_parts[1])
        else:
            print("Failed to parse availability text.")
            return
    except NoSuchElementException:
        print("Failed to find availability element.")
        return

    # Handle any alerts (notifications) that may appear
    try:
        alert = Alert(driver)
        alert.accept()
    except:
        pass

    # Check if there are vacancies (a < b) and display a popup message
    if registered_count < availability_threshold:
        # Automatically sign up the user
        sign_up()

        # Calculate available places including the user (-1 stands for the user)
        available_places = availability_threshold - registered_count - 1

        pymsgbox.alert(f"You have been signed up for the class! {available_places} places are now available.", "Class Availability", "OK")
    else:
        pymsgbox.alert(f"There are no available places for the class. ({registered_count} available)", "Class Availability", "OK")

# Function to click the button
def sign_up():
    try:
        button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-status='NOT_REGISTERED_ACTIVE']//button"))
        )
        button_element.click()
    except Exception as e:
        print("Error clicking the button:", str(e))

# Main loop that runs every hour
while True:
    check_website()
    time.sleep(INTERVAL)  # Interval sets up time after which the vacancy is checked again 