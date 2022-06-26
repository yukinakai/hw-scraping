from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
from data import exclusion_element
from data import expect_element
from utils import various_licenses
from service import offer_to_csv

def main():
  # Webドライバーの設定
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  chrome_service = fs.Service(executable_path=ChromeDriverManager().install())
  driver = webdriver.Chrome(service=chrome_service, options=options)
  # 対象画面にアクセスし、初期操作を行う
  url = "https://www.hellowork.mhlw.go.jp/"
  driver.get(url)
  # 「求人情報検索」をクリック
  driver.find_element(by=By.CLASS_NAME, value='retrieval_icn').click()
  # 「検索」をクリック
  driver.find_element(by=By.ID, value='ID_searchBtn').click()
  # 表示件数を50件に設定
  element = driver.find_element(by=By.ID, value='ID_fwListNaviDispBtm')
  Select(element).select_by_value("50")

  errors = list() # エラーのリスト
  has_next = True # 次のページの有無フラグ
  is_1st_page = True # 1ページ目かのフラグ
  h = 0 #テスト用のカウンター
  # 求人詳細用に空のタブを開く
  driver.execute_script("window.open();")
  while has_next:
    # 求人テーブルのデータを取得
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("table", attrs={"class": "kyujin"})
    # 除外するelementのid
    exclusion_element_id = exclusion_element.exclusion_element()
    expect_element_id = set(expect_element.element_id_cols().keys())
    # 求人詳細用のタブに切り替え
    driver.switch_to.window(driver.window_handles[1])
    # 各求人のデータを取得
    for i, job in enumerate(jobs):
      # 検索結果一覧からタグを取得する
      ## 、で区切ったテキストデータにする
      tags = '、'.join([tag.text.strip() for tag in  job.find_all('span', attrs={'class': 'nes_label any'})])
      # 検索結果の上から順番に求人詳細のデータを取得
      detail_path = job.select('#ID_dispDetailBtn')[0].get("href")
      detail_link = "https://www.hellowork.mhlw.go.jp/kensaku" + detail_path[1:]
      driver.get(detail_link)
      time.sleep(0.5)
      soup = BeautifulSoup(driver.page_source, "html.parser")
      # 求人詳細の求人情報テーブルから全てのidとテキストを取得する
      job_details = soup.find_all("table", attrs={"class": "normal mb1"})
      _offer = dict()
      for table in job_details:
        for element in table.find_all(re.compile('.*'), id=re.compile('.*')):
          element_id = element.get('id')
          if element_id in exclusion_element_id:
            continue
          if element_id in ['ID_MenkyoSkkuMeisho', 'ID_MenkyoSkkuSel']:
            if element_id == 'ID_MenkyoSkkuMeisho':
              _offer[element_id] = various_licenses.get_various_licenses(soup)
            continue
          if element_id in _offer:
            e = {
              'offer_url': detail_link,
              'error': 'unknown duplicated element id',
              'detail': element_id
              }
            errors.append(e)
            print(e)
          _offer[element_id] = element.text.strip()
      all_element_id = set(_offer.keys())
      # 未知のカラムがないかチェック
      unknown_elemet_id = all_element_id.difference(exclusion_element_id).difference(expect_element_id)
      if len(unknown_elemet_id) > 0:
        e = {
          'offer_url': detail_link,
          'error': 'found unknown columns',
          'detail': unknown_elemet_id
          }
        errors.append(e)
        print(e)
      # 求人詳細のデータを整形し、CSVに落とす
      offer_to_csv.offer_to_csv(_offer, tags, is_1st_page)
    # 検索結果一覧用のタブに移動
    driver.switch_to.window(driver.window_handles[0])
    # 検索結果の次のページへ移動
    if driver.find_element(by=By.NAME, value='fwListNaviBtnNext').is_enabled():
      driver.find_element(by=By.NAME, value='fwListNaviBtnNext').click()
      is_1st_page = False
    else:
      has_next = False
    # テスト用のカウンターを更新。特定の回数でループを止める
    h = h +1
    print(h)
    if h > 5:
      break
  print(errors)
  # ドライバーを閉じる
  driver.close()
  driver.quit()

if __name__ == "__main__":
  main()
