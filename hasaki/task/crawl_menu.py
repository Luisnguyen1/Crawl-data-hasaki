import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver_path = 'chromedriver-win64/chromedriver.exe'

service = Service(driver_path)
driver = webdriver.Chrome(service=service)

try:
    driver.get('https://hasaki.vn/')

    submenus = driver.find_elements(By.CLASS_NAME, 'sub_item_menu')
    data = []

    for submenu in submenus:
        sub_item = submenu.find_element(By.TAG_NAME, 'a')
        submenu_data = {
            'parent_menu': sub_item.text,
            'parent_href': sub_item.get_attribute('href'),
            'submenus': []
        }

        try:
            col_hover_submenus = submenu.find_elements(By.CLASS_NAME, 'col_hover_submenu')
            for col_hover_submenu in col_hover_submenus:
                links = col_hover_submenu.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    submenu_data['submenus'].append({
                        'text': link.text,
                        'href': link.get_attribute('href')
                    })
        except:
            pass

        data.append(submenu_data)

    # Save the data to a JSON file
    with open('menu_links.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

finally:
    driver.quit()
