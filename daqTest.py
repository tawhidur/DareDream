import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Setup
def test_setup():
    global mydriver
    global wait
    mydriver = webdriver.Chrome()
    mydriver.get("http://")
    mydriver.maximize_window()
    wait = WebDriverWait(mydriver, 5)


# Login
def test_login():
    #Locate user name and type name
    mydriver.find_element(By.NAME, "username").send_keys("testloginbro!")
    #Locate password and type password
    mydriver.find_element(By.ID, "password_field").send_keys("****")
    #Click on login button
    mydriver.find_element(By.XPATH, "//button[normalize-space()='Login']").click()
    #Sleep time to load content
    time.sleep(3)


# Shopfloor
def test_shopfloor():
    #Locate and click shopfloor
    mydriver.find_element(By.XPATH, "(//*[contains(text(),'shop')])[2]").click()
    #Store current URL
    string_url = mydriver.current_url
    #Valided with actual URL
    assert (string_url, "http://192.168.14.6/shopfloor/")
    time.sleep(3)
    print("Shopfloor link has loaded")


#Machine
def test_machine():
    #Swith to iframe
    mydriver.switch_to.frame("page_iframe")
    #locate machine use xpath
    mydriver.find_element(By.XPATH, "//*[contains(text(),' Test Machine Bohai ')]").click()
    #sleep time to load machine status
    time.sleep(3)
    #Back to default
    mydriver.switch_to.default_content()
    mydriver.get("http://111.22.11/daq_config/")
    time.sleep(3)
    mydriver.switch_to.frame("page_iframe")
    mydriver.find_element(By.XPATH, "//input[@aria-label='Maschine']").send_keys("0352")
    mydriver.find_element(By.XPATH, "//input[@aria-label='Maschine']").click()
    ip_element = mydriver.find_element(By.XPATH, "//div[normalize-space()='192.168.13.94']")
    ip = ip_element.text
    mydriver.execute_script("window.open('about:blank', 'new_window')")
    mydriver.switch_to.window(mydriver.window_handles[1])
    mydriver.get("http://" + ip)
    time.sleep(5)
    mydriver.find_element(By.XPATH, "/html/body/div/center/button[1]").click()
    mydriver.switch_to.default_content()
    time.sleep(3)
    try:
        # Wait for the element to be located
        canvas_element = WebDriverWait(mydriver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="myCanvas"]')))
        # If the element is found, print a success message
        print("myCanvas element found on the webpage.")
    except:
        # If the element is not found within the specified time, print an error message
        print("myCanvas element not found on the webpage.")

    # Get the value of myCanvas S1:0V
    # Get the value of myCanvas S1:0V
    canvas_value_str = canvas_element.get_attribute("innerText")
    canvas_value_str = canvas_value_str.strip()

    # Check if the string is empty before attempting to convert it to a float
    if canvas_value_str:
        try:
            canvas_value = float(canvas_value_str)
            # Convert the value to float and compare if it's more than 0
            if canvas_value > 0:
                print("Machine is in production")
            else:
                print("Machine is not in production")
        except ValueError:
            print("Error: Could not convert string to float")
    else:
        print("Error: The string is empty")

def test_mesvisu():
    try:
        mydriver.get("http://19.222.22.2/shopfloor/")
        mydriver.switch_to.frame("page_iframe")
        mesvisu_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='MESVisu']")))
        mesvisu_button.click()

        standstill_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Standstill']")))
        standstill_button.click()

        print("MESVisu Standstill page loaded successfully.")
    except TimeoutException:
        print("Error: MESVisu Standstill page did not load within the specified time.")

def test_tabledata():
    # Open the webpage containing the table
    mydriver.get("http://182.111.22.2/mes_visu/stillstand/?bdr_nr=0352&m=3&id=null&halle=12&logged=true&halle_bez=Gie%C3%9Ferei")

    # Wait for the table header for "Duration" to be visible
    duration_header = WebDriverWait(mydriver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'Duration')]")))

    # Get the index of the "Duration" header
    duration_index = int(duration_header.get_attribute("data-index"))

    # Find all rows in the table
    rows = mydriver.find_elements(By.XPATH, "//tr")

    # Initialize a flag to check for negative data
    has_negative_data = False

    # Iterate over each row (starting from the second row assuming the first row is header)
    for row in rows[1:]:
        # Get the cell in the "Duration" column for the current row
        duration_cell = row.find_elements(By.XPATH, f"./td[{duration_index + 1}]")[0]

        # Get the text from the "Duration" cell
        duration_text = duration_cell.text.strip()

        # Check if the duration is negative
        if duration_text.startswith("-"):
            has_negative_data = True
            break

    # Check the result and print the outcome
    if has_negative_data:
        print("Test failed: Negative data found in 'still_diffrence' field.")
    else:
        print("Test passed: No negative data found in 'still_diffrence' field.")

def test_teardown():
    mydriver.close()
    mydriver.quit()
    print("Test execution has completed! Please collect your report")
