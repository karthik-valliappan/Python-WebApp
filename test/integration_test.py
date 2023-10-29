import subprocess
import time
import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def driver():
    # Start the Streamlit application as a separate process
    app_process = subprocess.Popen(["streamlit", "run", "trade_data_visualizer.py"])

    # Wait for the Streamlit app to start
    time.sleep(2)

    driver = webdriver.Chrome()
    yield driver

    driver.quit()

    # Stop the Streamlit application process after the test
    app_process.terminate()
    app_process.wait()

def test_home_title(driver):
    driver.get("http://localhost:8501")

    # Wait for the page to load
    time.sleep(1)

    assert driver.title == "Home"
