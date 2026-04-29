from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def before_scenario(context, scenario):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    context.driver = webdriver.Chrome(service=Service(), options=options)
    context.driver.implicitly_wait(2)


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
