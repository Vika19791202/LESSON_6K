import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = ChromeOptions()
    # Можно добавить options.add_argument("--headless") для запуска без окна браузера
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_slow_calculator_fixed(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    driver.get(url)

    wait = WebDriverWait(driver, 60)

    # 1. Настройка задержки на 45 секунд
    delay_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#delay"))
    )
    delay_input.clear()
    delay_input.send_keys("45")
    print("✅ Поле задержки установлено на 45 сек.")

    # Вспомогательная функция для кликов (локальная для теста)
    def click_key(text):
        locator = (
            By.XPATH,
            f"//div[@id='calculator']//span[normalize-space()='{text}']"
        )
        btn = wait.until(EC.element_to_be_clickable(locator))
        btn.click()
        print(f"   -> Нажата кнопка: {text}")

    # 2. Последовательность нажатий
    click_key('7')
    click_key('+')
    click_key('8')
    click_key('=')

    # 3. Информирование пользователя в консоли
    print("✅ Все кнопки нажаты. Теперь ждем 45 секунд, пока калькулятор 'подумает'...")
    print(
        "   ⚠️ НЕ ПРЕРЫВАЙТЕ ТЕСТ В ЭТИ 45 СЕКУНД! "
        "Это не зависание, это работа страницы."
    )

    # 4. Проверка результата
    result_locator = (By.CSS_SELECTOR, "div.screen")
    
    # Явное ожидание появления текста "15". 
    # Если текста не будет 60 секунд, тест упадет с понятной ошибкой TimeoutException.
    wait.until(EC.text_to_be_present_in_element(result_locator, "15"))
    
    # Дополнительная проверка через assert (если требуется по заданию)
    actual_text = driver.find_element(*result_locator).text
    assert actual_text == "15", f"Ошибка: ожидалось '15', но получено '{actual_text}'"
    
    print("🎉 ТЕСТ ПРОЙДЕН! Результат верный: 15")

