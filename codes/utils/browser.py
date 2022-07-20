from webdriver_manager.firefox import GeckoDriverManager
import platform
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common import desired_capabilities
import socket
from selenium import webdriver
import time

import requests
import logging
logger = logging.getLogger(__name__)


def get_driver(platform, browser):
    if platform == "Windows":
        if browser == "chrome":
            return
            # return webdriver.Chrome(ChromeDriverManager().install())
        elif browser == "firefox":
            return webdriver.Firefox(
                executable_path=GeckoDriverManager().install())
    return get_driver_with_captcha(local=True)


def get_driver_with_captcha(local=False):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # XXX Fix...
    # plugin = '/chrome-plugin/anticaptcha-plugin_v0.3007.crx'
    # if local:
    #    plugin = './chrome-plugin/anticaptcha-plugin_v0.3007.crx'

    # chrome_options.add_extension(
    #    plugin
    # )

    if local:
        driver = webdriver.Chrome(options=chrome_options)
        config_anti_captcha(driver)
    else:
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            chrome_options.to_capabilities()
        )

    return driver


def alive(url):
    while True:
        logger.error("Checking if selenium is up... %s" % url)
        try:
            req = requests.get("%s/status" % url)
            if req.status_code == 404:
                req = requests.get("%s/wd/hub" % url)

            if req.status_code == 200:
                logger.error("Alive break!")
                return
            logger.error("selemium ret %s" % req.status_code)
        except Exception:
            logger.error("selemium is not up up...")
            print("Waiting on: %s" % url)
        time.sleep(2)


def get_driver_firefox(platform=None, proxy=None):
    # fp = webdriver.FirefoxProfile()
    # fp.add_extension('./firefox-plugin/anticaptcha-plugin_v0.3101.xpi')
    options = Options()
    caps = desired_capabilities.DesiredCapabilities.FIREFOX.copy()
    # caps['marionette'] = False
    caps.update(options.to_capabilities())

    # XXX make configurable with env var for dev setup and prod deploy
    if socket.gethostname() in [
        'arosen-laptop', 'merih.local', 'hassans-MacBook-Pro-2.local',
        'arosen-ZenBook-UX434IQ-Q407IQ', 'zano-Vostro-3558',
        'zano-ASUS-TUF-Gaming-A15-FA506II-FA506II'
    ]:
        command_executor = 'http://127.0.0.1:4444/wd/hub'
        alive_url = 'http://127.0.0.1:4444'
        fp = webdriver.FirefoxProfile('./codes/jmi439mu.captcha-firefox')
        options.binary = '/opt/firefox/firefox'
    else:
        command_executor = 'http://selenium-hub:4444/wd/hub'
        alive_url = 'http://selenium-hub:4444'
        fp = webdriver.FirefoxProfile(
            '/home/web/codes/jmi439mu.captcha-firefox')

    # fp.set_preference('permissions.default.image', 2)
    fp.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

    alive(alive_url)
    if proxy:
        print("configuring to use proxy=%s" % proxy)
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.socks", '')
        fp.set_preference("network.proxy.socks_port", "")
        fp.set_preference(
            "network.proxy.http", proxy.split(":")[0])
        fp.set_preference("network.proxy.http_port",
                          int(proxy.split(":")[1]))

        fp.set_preference(
            "network.proxy.ssl", proxy.split(":")[0])
        fp.set_preference(
            "network.proxy.ssl_port", int(proxy.split(":")[1]))

    driver = webdriver.Remote(
        browser_profile=fp,
        command_executor=command_executor,
        desired_capabilities=caps,
    )
    logger.error("got driver")
    driver.set_page_load_timeout(30)
    logger.info("set page load timeout")
    return driver


def init_driver(browser, proxy=None):
    os_platform = platform.system()
    if browser == 'firefox':
        return get_driver_firefox(os_platform, proxy)
    elif browser == 'local_firefox':
        return get_driver(os_platform , "firefox")
    elif browser == 'chrome':
        return get_driver(os_platform , "chrome")

    raise Exception('There is no valid browser')

def config_anti_captcha(driver):
    driver.get(
        'chrome-extension://lncaoejhfdpcafpkkcddpjnhnodcajfg/options.html'
    )
    # driver.implicitly_wait(1)
    # driver.find_element_by_name('account_key').send_keys(APP_KEY)
    # driver.find_element_by_name('auto_submit_form').click()

    # driver.implicitly_wait(1)
    # driver.find_element_by_xpath(
    #     "//input[@class='save_button']"
    # ).click()
    # driver.implicitly_wait(1)


