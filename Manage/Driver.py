from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from urllib3.exceptions import InsecureRequestWarning
import requests
import os


class CompDriver:
    @staticmethod
    def get_driver(ruta_descarga):
        print("\nComprobando la versión del navegador Edge ...\n")
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        options = EdgeOptions()

        prefs = {'download.prompt_for_download': False,
                 'safebrowsing.enabled': False,
                 "profile.default_content_setting_values.automatic_downloads": 1,
                 'download.default_directory': str(ruta_descarga),
                 "credentials_enable_service": False,
                 "profile.password_manager_enabled": False}

        options.use_chromium = True
        options.add_experimental_option("prefs", prefs)

        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation", 'disable-popup-blocking'])
        options.add_experimental_option('useAutomationExtension', False)

        os.environ['WDM_SSL_VERIFY'] = '0'
        os.environ['WDM_LOG_LEVEL'] = '0'
        #os.environ['WDM_LOCAL'] = '1'

        service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        return driver

    @staticmethod
    def get_local_driver_edge(dir_emission):
        print("\n\nComprobando la versión del navegador Edge ...\n")
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        drivername = 'msedgedriver.exe'

        options = EdgeOptions()

        prefs = {'download.prompt_for_download': False,
                 'safebrowsing.enabled': False,
                 "profile.default_content_setting_values.automatic_downloads": 1,
                 'download.default_directory': str(),
                 "credentials_enable_service": False,
                 "profile.password_manager_enabled": False}

        options.use_chromium = True
        options.add_experimental_option("prefs", prefs)

        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation", 'enable-logging',
                                                            'disable-popup-blocking'])
        options.add_experimental_option('useAutomationExtension', False)

        os.environ['WDM_SSL_VERIFY'] = '0'
        os.environ['WDM_LOG_LEVEL'] = '0'
        os.environ['WDM_LOCAL'] = '1'

        path_driver = dir_emission.parent.joinpath(drivername)
        return webdriver.Edge(options=options, executable_path=str(path_driver))
