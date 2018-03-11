class SeleniumConfig():
    crome_path = ''
    webdriver_path = ''
    app_path = ''

    def __init__(self, chrome, webdriver, app_path):
        self.crome_path = chrome
        self.webdriver_path = webdriver
        self.app_path = app_path
