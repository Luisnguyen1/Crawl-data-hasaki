from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from concurrent.futures import ThreadPoolExecutor

# Hàm để lấy thông tin sản phẩm
def get_product_info(url):
    driver = webdriver.Chrome(service=Service('chromedriver-win64/chromedriver.exe'))
    driver.get(url["link"])
    comments = []

    def get_reviews():
        try:
            reviews = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "review-details-wrap"))
            )
            for review in reviews:
                comment = review.find_element(By.XPATH, ".//div[@itemprop='description']").text
                comments.append(comment)
        except Exception as e:
            print("Không thể lấy đánh giá:", e)

    get_reviews()
    view_more_button = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'desc-viewmore')]/span[text()='Xem thêm thông tin']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", view_more_button)
    time.sleep(1)
    view_more_button.click()

    product_name = driver.find_element(By.CLASS_NAME, 'page-title').text

    try:
        price_sale = driver.find_element(By.CLASS_NAME, 'price-wrapper').text
    except:
        price_sale = None

    try:
        price_original = driver.find_element(By.CLASS_NAME, 'old-price').text
    except:
        price_original = None

    try:
        brand = driver.find_element(By.CSS_SELECTOR, 'span.brand-name').text
    except:
        brand = None

    try:
        image_link = driver.find_element(By.CSS_SELECTOR, 'img.fotorama__img').get_attribute('src')
    except:
        image_link = None

    try:
        loai = driver.find_element(By.XPATH, "//div[contains(@class, 'ecom-title-variant')]/span").text
    except:
        loai = None

    try:
        description = driver.find_element(By.ID, 'description').text
    except:
        description = None

    try:
        rating = driver.find_element(By.CLASS_NAME, 'amreview-summary').text
    except:
        rating = None

    try:
        info_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tab-label-additional-title"))
        )
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", info_button)
        time.sleep(1)

        try:
            info_button.click()
        except Exception as e:
            print(f"Lỗi khi click: {e}")
            driver.execute_script("arguments[0].click();", info_button)

        additional_info = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "additional"))
        )

        try:
            skin_type = additional_info.find_element(By.XPATH, "//th[contains(text(), 'Dành cho da')]/following-sibling::td").text
        except Exception as e:
            print("Không thể lấy thông tin loại da:", e)
            skin_type = ""
    except Exception as e:
        print("Không thể tìm thấy nút 'Thông tin thêm':", e)
        skin_type = None

    product_info = {
        "name": product_name,
        "price": price_sale,
        "price_raw": price_original,
        "link": url["link"],
        "classify": loai,
        "specifications": brand,
        "img": image_link,
        "description": description,
        "skin_type": skin_type,
        "rating": rating,
        "comments": comments
    }

    # Đóng driver sau khi lấy dữ liệu
    driver.quit()

    return product_info

# Đọc đường link từ file JSON
with open('products-link.json', 'r', encoding='utf-8') as f:
    links = json.load(f)

# Ghi dữ liệu vào file JSON
with open('product_data.json', 'w', encoding='utf-8') as f:
    with ThreadPoolExecutor(max_workers=5) as executor:
        for product_info in executor.map(get_product_info, links):
            json.dump(product_info, f, ensure_ascii=False, indent=4)
            f.write('\n')  # Thêm dòng mới sau mỗi sản phẩm