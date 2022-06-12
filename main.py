from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import re

# set up driver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# access to hello work
url = "https://www.hellowork.mhlw.go.jp/"
driver.get(url)
time.sleep(1)

# click 「求人情報検索」
driver.find_element_by_class_name("retrieval_icn").click()
time.sleep(1)

# click 「検索」
driver.find_element_by_id("ID_searchBtn").click()
time.sleep(1)

# Change the number of items displayed
element = driver.find_element_by_id("ID_fwListNaviDispBtm")
Select(element).select_by_value("50")
time.sleep(1)

# get offer data
soup = BeautifulSoup(driver.page_source, "html.parser")
jobs = soup.find_all("table", attrs={"class": "kyujin"})
for i, job in enumerate(jobs):
    job_name = str(job.find("td", attrs={"class": "m13"}).text.strip())
    salary_tags = job.find_all("tr",attrs={"class": "border_new"})[5].select(".disp_inline_block")
    for t, salary_tag  in enumerate(salary_tags):
        job_salary = salary_tag.text

    m = re.search('(〜)(\d{3}),(\d{3})', job_salary)
    highest = int(m.group(2) + m.group(3))

# driver close, quit
driver.close()
driver.quit()
