import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture
def driver():
    options = FirefoxOptions()
    # options.add_argument("--headless")  # Раскомментировать для headless-режима
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_purchase_flow(driver):
    url = "https://www.saucedemo.com/"
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # --- ШАГ 1: Авторизация ---
    wait.until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
    print("✅ Авторизация успешна.")

    # --- ШАГ 2: Добавление товаров ---
    products_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ]

    for product_name in products_to_add:
        add_button_locator = (
            By.XPATH, 
            f"//div[contains(@class, 'inventory_item') and .//*[contains(text(), '{product_name}')]]//button[contains(@class, 'btn_primary')]"
        )
        add_button = wait.until(EC.element_to_be_clickable(add_button_locator))
        add_button.click()
        print(f"   -> Добавлен товар: {product_name}")

    # --- ШАГ 3: Переход в корзину и Checkout ---
    cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
    cart_link.click()
    checkout_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout_button")))
    checkout_btn.click()

    # --- ШАГ 4: Заполнение формы ---
    first_name_input = wait.until(EC.element_to_be_clickable((By.ID, "first-name")))
    first_name_input.send_keys("Ivan")
    
    last_name_input = driver.find_element(By.ID, "last-name")
    last_name_input.send_keys("Ivanov")
    
    postal_code_input = driver.find_element(By.ID, "postal-code")
    postal_code_input.send_keys("123456")

    continue_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cart_button")))
    continue_btn.click()

    # --- ШАГ 5: Проверка итоговой суммы (БЕЗОПАСНЫЙ ПАРСИНГ) ---
    total_label_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label")))
    total_text = total_label_element.text
    print(f"🔍 Текст элемента с суммой: '{total_text}'")

    try:
        # Способ 1: ищем символ $ и берём всё после него
        if "$" in total_text:
            # Разделяем по $, берём вторую часть и убираем пробелы
            total_amount_str = total_text.split("$")[1].strip()
            # Убираем всё, что после числа (например, налог), оставляя только первое число
            total_amount_str = total_amount_str.split()[0]  # Берём только первое слово (число)
            total_amount = float(total_amount_str)
        else:
            # Фоллбэк: если нет $, пробуем искать по двоеточию
            if ":" in total_text:
                total_amount_str = total_text.split(":")[1].strip().replace("$", "")
                total_amount = float(total_amount_str)
            else:
                raise ValueError("Не удалось найти символ $ или : в тексте суммы")

        expected_total = 58.29
        assert total_amount == expected_total, f"Ошибка суммы Ожидалось ${expected_total}, но получено ${total_amount:.2f}"
        print(f"✅ Итоговая сумма верна: ${total_amount:.2f}")
        print("🎉 Тест пройден успешно!")

    except (IndexError, ValueError, AttributeError) as e:
        assert False, f"❌ Не удалось распарсить сумму из текста '{total_text}'. Ошибка: {e}"



