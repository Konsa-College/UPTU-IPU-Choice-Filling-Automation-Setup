from win10toast import ToastNotifier
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

TARGET_URL = "https://uptac.admissions.nic.in/"
DESIRED_URL = "https://admissions.nic.in/UPTAC/Applicant/Choice/ChoiceFilling.aspx"
CSV_FILE_PATH_FW = "choice_filling_fw.csv"
CSV_FILE_PATH_NON_FW = "choice_filling.csv"


def send_notification(title, message):
    """
    Sends a notification with a given title and message.
    Also plays a sound notification.
    """
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10, sound=True)


def open_chrome_tab_with_debugging(url):
    """
    The function opens a new Chrome tab with debugging enabled and navigates to the specified URL.

    :param url: The `url` parameter is the URL of the webpage that you want to open in a new Chrome tab
    for debugging
    :return: a WebDriver object if it is successfully initialized, or None if there is an error.
    """

    try:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {str(e)}")
        return None


def find_tab_by_url(driver, desired_url):
    """
    The function `find_tab_by_url` takes a Selenium WebDriver instance and a desired URL as input, and
    switches to the tab that contains the desired URL if it exists, returning True if successful and
    False otherwise.

    :param driver: The "driver" parameter is an instance of a web driver, such as Selenium's WebDriver,
    that is used to control the web browser. It allows you to interact with the web page, navigate
    between different pages, and perform various actions
    :param desired_url: The desired_url parameter is a string that represents the URL you want to find
    in the open tabs
    :return: a boolean value. It returns True if the desired URL is found in any of the open tabs, and
    False if the desired URL is not found in any of the open tabs.
    """

    try:
        # Execute JavaScript to get all open window handles
        window_handles = driver.window_handles

        # Iterate through window handles and switch to the tab with the desired URL
        for handle in window_handles:
            driver.switch_to.window(handle)
            current_url = driver.current_url
            if desired_url in current_url:
                return True

        # If the desired URL is not found in any tabs, return False
        return False
    except Exception as e:
        print(f"Error while switching tabs: {str(e)}")
        return False


def iterate_table_and_click_add(driver, college_list):
    """
    The function iterates through a table on a web page, searches for a specific college and branch, and
    clicks the "Add" button if found.

    :param driver: The `driver` parameter is an instance of a web driver, such as Selenium's WebDriver,
    that is used to interact with a web page
    :param college_list: The college_list parameter is a list of tuples. Each tuple contains three
    elements:
    """
    try:
        # Wait for the table to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#avlChoiceContainer"))
        )

        for cl in college_list:
            serial, college, branch = cl

            found = False  # Flag to track if the pair is found

            rows = driver.find_elements(By.CSS_SELECTOR, "#avlChoiceContainer tr")

            for row in rows:  # No need to skip the header row in this structure
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 4:  # Check if there are enough cells in the row
                    inst_name = cells[1].text
                    br_name = cells[3].text

                    if college == inst_name and branch == br_name:

                    try:
                        try:
                            # Wait for the 'Add' button to be present in the row
                            add_button = WebDriverWait(row, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='Add']"))
                            )
                        except TimeoutException:
                            # Send a notification if the 'Add' button is not available within the specified time
                            send_notification("Action Required", "The 'Add' button is not available. Please check the webpage.")
                            raise

                        # Click the 'Add' button
                        add_button.click()

                        # Set the flag to True indicating that the 'Add' button has been clicked
                        is_button_clicked = True

                        print(f"Serial No. {serial}. Successfully clicked 'Add' for {college} - [{branch}]")
                        break

                    except Exception as e:
                        # Print an error message if the 'Add' button is not found or not accessible
                        print(f"Unable to access the 'Add' button for {college} - [{branch}]. Please ensure that the webpage is loaded correctly. Error: {str(e)}")
                        continue

                                if not found:
                                    print(f"S.No. - {serial} SKIPPED [{college}] - [{branch}]")

                        except Exception as e:
                            print(f"Error in iterate_table_and_click_add: {str(e)}")


def read_colleges_from_csv(file_path):
    """
    The function reads data from a CSV file and returns a list of colleges with their serial numbers,
    names, and branches.

    :param file_path: The file path is the location of the CSV file that you want to read. It should be
    a string that specifies the path to the file on your computer. For example,
    "C:/Users/username/Documents/colleges.csv"
    :return: a list of lists, where each inner list represents a college and contains the serial number,
    college name, and college branch.
    """

    college_list = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                college_list.append(
                    [row["Serial"], row["CollegeName"], row["CollegeBranch"]]
                )
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
    return college_list


def countdown_timer(countdown):
    """
    The function `countdown_timer` takes an input `countdown` and prints a countdown from that number to
    1, then prints "Starting tasks now!".

    :param countdown: The parameter "countdown" is the number of seconds to count down from before
    starting the tasks
    """

    print(f"Starting tasks in {countdown} seconds...")
    for i in range(countdown, 0, -1):
        print(i, end=" ", flush=True)
        time.sleep(0.5)
    print("\nStarting tasks now!")


def main():
    """
    The main function performs automation tasks for choice filling in a college admission website.
    :return: The main function is returning an integer value of 0.
    """

    try:
        # You can add your college and branch data to this list
        csv_file_path = "choice_filling.csv"
        if input("Is the candidate eligible for Fee Wavier? (no/yes): ").lower() == "yes":
            csv_file_path = CSV_FILE_PATH_FW
            print("Using FW Sheet")
        else:
            csv_file_path = CSV_FILE_PATH_NON_FW
            print("Using Non-FW Sheet")

        # Read the list of colleges from the CSV file
        college_list = read_colleges_from_csv(csv_file_path)

        # Open a new Chrome tab with debugging
        driver = open_chrome_tab_with_debugging(TARGET_URL)

        # Find and switch to the desired tab
        find_desired_url = input("Have you logged in succesfully? (yes/no): ").lower()

        if find_desired_url:
            if not find_tab_by_url(driver, DESIRED_URL):
                print("Desired URL not found in any open tabs.")
                return

            while True:
                start_tasks = input("Do you want to start the tasks? (yes/no): ").lower()

                if start_tasks == "yes":
                    countdown = 4
                    countdown_timer(countdown)

                    # Perform table iteration and clicking on "Add" buttons
                    iterate_table_and_click_add(driver, college_list)

                    send_notification(
                        "Choice Filling Task Completed",
                        "All choices are filled now. The automation task has been completed.",
                    )

                    if input("Do you want to CLOSE this tasks? (no/yes): ").lower() == "yes":
                        return 0
                    else:
                        print("Close Chrome Window Manually")
                        print("Close Terminal Manually")
                        while True:
                            print("-", end="")

                else:
                    print("Tasks not started.")
                    send_notification(
                        "Task Failed",
                        "Error Occurred! This automation task has not been completed.",
                    )
                    return 0

    except Exception as e:
        # Handle exceptions gracefully, e.g., log them
        print("Main function broke! Now you need to restart!")
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
