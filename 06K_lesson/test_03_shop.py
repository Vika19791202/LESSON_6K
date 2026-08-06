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
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_purchase_flow(driver):
    url = "https://www.saucedemo.com/"
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys("secret_sauce")
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
    print("✅ Авторизация успешна.")

    products_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
    ]

    for product_name in products_to_add:
        add_button_locator = (
            By.XPATH,
            f"//div[contains(@class, 'inventory_item') "
            f"and .//*[contains(text(), '{product_name}')]]"
            f"//button[contains(@class, 'btn_primary')]"
        )
        add_button = wait.until(EC.element_to_be_clickable(add_button_locator))
        add_button.click()
        print(f"   -> Добавлен товар: {product_name}")

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout_button"))).click()

    wait.until(EC.element_to_be_clickable((By.ID, "first-name"))).send_keys("Ivan")
    wait.until(EC.element_to_be_clickable((By.ID, "last-name"))).send_keys("Ivanov")
    wait.until(EC.element_to_be_clickable((By.ID, "postal-code"))).send_keys("123456")
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cart_button"))).click()

    total_locator = (By.CLASS_NAME, "summary_total_label")
    wait.until(EC.text_to_be_present_in_element(total_locator, "$58.29"))

    total_element = driver.find_element(*total_locator)
    total_text = total_element.text
    print(f"🔍 Текст элемента с суммой: '{total_text}'")

    assert total_text == "Total: $58.29", (
        f"Ошибка суммы: ожидалось 'Total: $58.29', но получено '{total_text}'"
    )

    print("✅ Итоговая сумма верна: $58.29")
    print("🎉 Тест пройден успешно!")
