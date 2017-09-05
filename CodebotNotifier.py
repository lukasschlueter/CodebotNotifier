import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from win10toast import ToastNotifier


def check_for_phantomjs() -> bool:
    return "phantomjs.exe" in os.listdir(".")


def main():
    if not check_for_phantomjs():
        raise RuntimeError("Could not find the phantomjs.exe!\n"
                           "Please download it from http://phantomjs.org/download.html and add it to this directory!")
    username = input("Username: ")
    password = input("Passwort: ")

    toaster = ToastNotifier()
    driver = webdriver.PhantomJS()

    driver.get("https://www.codebot.de")
    login(driver, username, password)

    driver.get("https://www.codebot.de/find-new/posts")

    old_conversations = False
    old_alerts = False
    old_unread_threads = []
    while True:
        driver.get("https://www.codebot.de/find-new/posts")
        new_conversations = check_conversations(driver)
        conversations_changed = new_conversations and (new_conversations is not old_conversations)
        print(new_conversations)
        new_alerts = check_alerts(driver)
        alerts_changed = new_alerts and (new_alerts is not old_alerts)
        print(new_alerts)

        unread_threads = get_unread_threads(driver)
        print(unread_threads)
        print(old_unread_threads)
        threads_changed = False

        toast = ""
        if conversations_changed:
            toast += "Ungelesene Unterhaltung!\n"
        if alerts_changed:
            toast += "Neuer Hinweis!\n"
        if len(unread_threads):
            threads = "Neue Beiträge:\n"
            for a in unread_threads:
                if a in old_unread_threads:
                    break
                threads += " - {}\n".format(a[0])
                threads_changed = True
            if threads_changed:
                toast += threads

        if conversations_changed or alerts_changed or threads_changed:
            toaster.show_toast("Codebot.de", toast)

        old_conversations = new_conversations
        old_alerts = new_alerts
        old_unread_threads = unread_threads
        sleep(10)


def login(driver, username, password):
    driver.find_element_by_css_selector("a.linkLogin").click()
    form = driver.find_element_by_css_selector("form")

    username_element = form.find_element_by_css_selector("input#LoginControl")
    password_element = form.find_element_by_css_selector("input#ctrl_password")

    WebDriverWait(driver, 10).until(EC.visibility_of(username_element))

    username_element.send_keys(username)
    password_element.send_keys(password)
    form.submit()

    if "Der zweite Schritt der Anmeldung" in driver.title:
        form = driver.find_element_by_css_selector("form.xenForm")
        code_input = form.find_element_by_css_selector("input#ctrl_totp_code")
        code = input("Two-Factor-Authorization: ")
        code_input.send_keys(code)
        form.submit()

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#ConversationsMenu_Counter")))


def check_conversations(driver):
    counter = driver.find_element_by_css_selector("#ConversationsMenu_Counter")
    return not has_class(counter, "Zero")


def check_alerts(driver):
    counter = driver.find_element_by_css_selector("#AlertsMenu_Counter")
    return not has_class(counter, "Zero")


def get_unread_threads(driver):
    post_elements = driver.find_elements_by_css_selector("a.PreviewTooltip")
    post_titles = [x.text for x in post_elements]

    time_elements = driver.find_elements_by_css_selector("a.dateTime abbr.DateTime")
    times = [x.get_attribute("data-time") for x in time_elements]

    results = []
    for index, post in enumerate(post_titles):
        if index < len(times):
            time = times[index]
        else:
            time = "old"
        results.append([post, time])
    return results


def has_class(element, class_name):
    return class_name in element.get_attribute("class")


if __name__ == "__main__":
    main()
