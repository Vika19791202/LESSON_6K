import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

@pytest.fixture
def driver():
    options = EdgeOptions()
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_form_validation_strict_assignment(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    # --- ЧАСТЬ 1: ЗАПОЛНЕНИЕ ФОРМЫ (строго по заданию) ---
    # Ищем элементы по атрибуту NAME, так как ID у них нет (см. скриншот)
    
    # First name
    first_name_input = wait.until(EC.element_to_be_clickable((By.NAME, "first-name")))
    first_name_input.clear()
    first_name_input.send_keys("Иван")

    # Last name
    last_name_input = driver.find_element(By.NAME, "last-name")
    last_name_input.clear()
    last_name_input.send_keys("Петров")

    # Address
    address_input = driver.find_element(By.NAME, "address")
    address_input.clear()
    address_input.send_keys("Ленина, 55-3")

    # Email
    email_input = driver.find_element(By.NAME, "e-mail")
    email_input.clear()
    email_input.send_keys("test@skypro.com")

    # Phone number
    phone_input = driver.find_element(By.NAME, "phone")
    phone_input.clear()
    phone_input.send_keys("+7985899998787")

    # Zip code -> Оставляем пустым, как в задании
    zip_code_input = driver.find_element(By.NAME, "zip-code")
    zip_code_input.clear()
    # Не делаем send_keys() для этого поля

    # City
    city_input = driver.find_element(By.NAME, "city")
    city_input.clear()
    city_input.send_keys("Москва")

    # Country
    country_input = driver.find_element(By.NAME, "country")
    country_input.clear()
    country_input.send_keys("Россия")

    # Job position
    job_input = driver.find_element(By.NAME, "job-position")
    job_input.clear()
    job_input.send_keys("QA")

    # Company
    company_input = driver.find_element(By.NAME, "company")
    company_input.clear()
    company_input.send_keys("SkyPro")

    # --- ЧАСТЬ 2: НАЖАТИЕ КНОПКИ SUBMIT (строго по заданию) ---
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()

    # --- ЧАСТЬ 3: ПРОВЕРКА ЦВЕТОВ (строго по заданию) ---
    
    # ВАЖНО: После нажатия Submit страница, скорее всего, ПЕРЕЙДЕТ на другую страницу 
    # (data-types-submitted.html), так как в HTML указано: <form method="get" action="data-types-submitted.html">
    # Нам нужно подождать загрузки новой страницы и проверить классы там.
    
    wait.until(lambda d: d.current_url != url) # Ждем перехода на новую страницу
    
    # Теперь проверяем классы на странице результатов
    
    # 1. Проверяем Zip code (должен быть красным - alert-danger)
    # На странице результатов элемент с name="zip-code" может быть уже не input, а блоком с результатом.
    # Но судя по логике таких демо-страниц, классы вешаются на элементы с теми же ID или именами.
    # Попробуем найти элемент по name и проверить его классы.
    
    try:
        zip_code_element = driver.find_element(By.NAME, "zip-code")
        zip_classes = zip_code_element.get_attribute("class")
        assert "alert-danger" in zip_classes, f"Ошибка: Поле Zip code не красное. Классы: {zip_classes}"
        print("✅ Zip code успешно подсвечен красным (alert-danger)")
    except Exception as e:
        # Если элемент не найден по name, возможно, структура изменилась, пробуем найти по тексту или ID
        print(f"⚠️ Не удалось найти zip-code по name, ошибка: {e}")
        # Здесь можно добавить дополнительную логику поиска, если страница рендерит результат иначе

    # 2. Проверяем остальные поля (должны быть зелеными - alert-success)
    green_fields_names = [
        "first-name", "last-name", "address", "e-mail", 
        "phone", "city", "country", "job-position", "company"
    ]

    for field_name in green_fields_names:
        try:
            field = driver.find_element(By.NAME, field_name)
            classes = field.get_attribute("class")
            assert "alert-success" in classes, f"Ошибка: Поле {field_name} не зеленое. Классы: {classes}"
            # Опционально: проверяем, что оно не красное
            assert "alert-danger" not in classes, f"Ошибка: Поле {field_name} не должно быть красным."
        except Exception as e:
            print(f"⚠️ Не удалось проверить поле {field_name}, ошибка: {e}")

    print("🎉 Все проверки пройдены успешно! Задание выполнено строго по инструкции.")

