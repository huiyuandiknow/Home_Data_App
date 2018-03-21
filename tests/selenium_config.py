from selenium_config_Class import SeleniumConfig

crome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
webdriver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
app_path = "http://127.0.0.1:5000/"


def get_path():
    path = SeleniumConfig(crome_path, webdriver_path, app_path="https://hom-es.herokuapp.com/")
    return path
