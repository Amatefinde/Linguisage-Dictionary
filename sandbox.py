from seleniumbase import Driver

# Создаём один экземпляр браузера
driver = Driver(uc=True, headless=True)

def get_html(url):
    driver.open(url)
    return driver.get_page_source()

try:
    for i in range(10):
        word = "dog"
        url = f"https://quizlet.com/webapi/3.2/images/search?query={word}&perPage=5"
        html = get_html(url)
        print(type(html))
        print(html)
finally:
    driver.quit()