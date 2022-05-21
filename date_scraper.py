from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import date

# for this to work a geckodriver binary must be placed in the PATH

def get_semester_start_and_end_dates(driver):
    start = ''
    end = ''

    delay = 3 #seconds

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'cdk-column-name')))
    except TimeoutException:
        print("Loading the page took too much time!")

    trows = driver.find_elements(By.TAG_NAME, 'tr')

    i = 0
    while (start == '' or end == ''):
        tdate, text = trows[i].text.split('\n')

        if text == 'Õppeaasta ja sügissemestri algus':
            start = tdate
        if text == 'Kevadsemestri arvestuslik lõpp, moodulite valimise tähtaeg esimese semestri üliõpilastele':
            end = tdate

        i += 1

    # convert date strings to datetime objects
    sD, sM, sY = [int(a) for a in start.split(".")]
    eD, eM, eY = [int(a) for a in end.split(".")]

    startdate = date(sY, sM, sD)
    enddate = date(eY, eM, eD)

    return [startdate, enddate]

def main():
    driver = webdriver.Firefox()
    driver.get("https://ois2.ut.ee/#/academic-calendar")
    
    start, end = get_semester_start_and_end_dates(driver)
    
    driver.quit()

    return [start, end]

if __name__ == '__main__':
    main()
