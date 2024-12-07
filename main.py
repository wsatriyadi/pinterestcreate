import pandas as pd
from playwright.sync_api import sync_playwright
import json

filecsv = "create.csv"
foldercookies = "cookies"

list = pd.read_csv(filecsv)
for index, row in list.iterrows():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.pinterest.com/business/create/",timeout=5000)
        page.get_by_placeholder("Email").fill(row['email'])
        page.get_by_placeholder("Password").fill(row['password'])
        page.locator("[data-test-id=\"signup-birthdate-field\"]").get_by_label("Birthdate").fill(row['birthdate'])
        page.get_by_role("button", name="Create account").click(timeout=1000)
        page.wait_for_url("**/hub/")

        all_cookies = context.cookies()
        print("Sukses, simpan cookies")
        file_path = foldercookies+"/"+row['email']+".json"
        with open(file_path, 'w') as file:
            json.dump(all_cookies, file)
        browser.close()
    print("Selesai")