# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

@pytest.fixture
def driver():
    # Указываем путь к скачанному драйверу
    service = Service("msedgedriver.exe")  # ← Имя файла, если он в той же папке
    
    # Опции браузера (можно оставить пустыми или добавить --headless)
    options = Options()
    # options.add_argument("--headless")  # Раскомментируй, если хочешь скрытый режим

    # Запускаем Edge с нужным драйвером
    driver = webdriver.Edge(service=service, options=options)
    
    yield driver  # Отдаём драйвер в тест
    driver.quit()  # Закрываем браузер после теста
