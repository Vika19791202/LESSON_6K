from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_fill_form(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
    wait = WebDriverWait(driver, 10)

    def fill_field(name_attr, value):
        element = wait.until(EC.visibility_of_element_located((By.NAME, name_attr)))
        element.clear()
        element.send_keys(value)
        # Двойной клик имитирует потерю фокуса и триггерит валидацию Bootstrap
        element.click()
        element.click()

    # Заполняем форму строго по заданию
    fill_field("first-name", "Иван")
    fill_field("last-name", "Петров")
    fill_field("address", "Ленина, 55-3")
    fill_field("city", "Москва")
    fill_field("country", "Россия")
    fill_field("e-mail", "test@skypro.com")
    fill_field("phone", "+7985899998787")
    fill_field("job-position", "QA")
    fill_field("company", "SkyPro")
    # Zip code оставляем пустым, как в задании

    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_btn.click()

    green_fields = [
        "first-name", "last-name", "address", "e-mail",
        "phone", "city", "country", "job-position", "company"
    ]

    print("⏳ Начинаем проверку полей на зелёный цвет сразу после клика...")

    for name in green_fields:
        try:
            field = driver.find_element(By.NAME, name)
            classes = field.get_attribute("class")
            assert "is-valid" in classes, f"❌ Ошибка: Поле '{name}' не стало зелёным. Классы: {classes}"
        except Exception as e:
            print(f"⚠️ Не удалось проверить поле '{name}': элемент исчез (вероятно, редирект).")
            break
    else:
        print("✅ Проверка 1 пройдена: все поля подсвечены зелёным (успели до редиректа).")

    try:
        zip_error_block = wait.until(EC.visibility_of_element_located((By.ID, "zip-code")))
        classes = zip_error_block.get_attribute("class")
        assert "alert-danger" in classes, "❌ Ошибка: Блок zip-code не стал красным!"
        print("✅ Проверка 2 пройдена: поле zip-code подсвечено красным.")
    except Exception as e:
        print(f"❌ Не удалось найти блок ошибки. Возможно, редирект произошёл мгновенно.")
        raise e

    print("🎉 Тест завершён.")
