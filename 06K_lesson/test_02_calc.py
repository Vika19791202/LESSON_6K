import pytest
import time
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
    # Не используй headless, пока отлаживаешь, чтобы видеть процесс
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_slow_calculator_fixed(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    driver.get(url)
    
    # Таймаут ставим с запасом. 
    # 45 сек (задержка) + время на загрузку страницы + небольшой буфер
    wait = WebDriverWait(driver, 60)

    # --- ШАГ 1: Поле задержки (#delay) ---
    delay_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#delay")))
    delay_input.clear()
    delay_input.send_keys("45")
    print("✅ Поле задержки установлено на 45 сек.")

    # --- ШАГ 2: Кнопки ---
    # Кнопки находятся внутри div.keys. Это <span> с текстом.
    # Используем normalize-space() для надежности.
    
    def click_key(text):
        # Локатор: внутри #calculator ищем span с нужным текстом
        locator = (By.XPATH, f"//div[@id='calculator']//span[normalize-space()='{text}']")
        btn = wait.until(EC.element_to_be_clickable(locator))
        btn.click()
        print(f"   -> Нажата кнопка: {text}")

    click_key('7')
    click_key('+')
    click_key('8')
    click_key('=')
    
    print("✅ Все кнопки нажаты. Теперь ждем 45 секунд, пока калькулятор 'подумает'...")
    print("   ⚠️ НЕ ПРЕРЫВАЙТЕ ТЕСТ В ЭТИ 45 СЕКУНД! Это не зависание, это работа страницы.")

    # --- ШАГ 3: Проверка результата ---
    # Согласно скриншоту, результат лежит в <div class="screen">
    result_locator = (By.CSS_SELECTOR, "div.screen")
    
    # Ждем, пока в тексте элемента появится "15"
    # Мы ждем именно text, а не value, так как это div
    wait.until(EC.text_to_be_present_in_element(result_locator, "15"))
    
    # Финальная проверка
    result_element = driver.find_element(*result_locator)
    actual_text = result_element.text
    
    assert actual_text == "15", f"Ошибка: ожидалось '15', но получено '{actual_text}'"
    
    print("🎉 ТЕСТ ПРОЙДЕН! Результат верный: 15")
    #Updated test on 03.08.2025 to verify form stability




