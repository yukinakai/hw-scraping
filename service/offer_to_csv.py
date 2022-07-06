from data import expect_element
from utils import salary
import csv

def offer_to_csv(_offer, tags, is_1st_page):
  offer = dict()
  element_id_cols = expect_element.element_id_cols()
  for element_id, col_name in element_id_cols.items():
    if element_id == 'ID_MenkyoSkkuSel':
      continue
    if element_id in _offer:
      offer[col_name] = _offer[element_id]
      if col_name == 'total_salary':
        offer['min_total_salary'], offer['max_total_salary'] = salary.min_max_salary(_offer[element_id])
      elif col_name == 'salary_type_salary':
        offer['min_salary_type_salary'], offer['max_salary_type_salary'] = salary.min_max_salary(_offer[element_id])
    else:
      offer[col_name] = ''
      if col_name == 'total_salary':
          offer['min_total_salary'] = ''
          offer['max_total_salary'] = ''
      elif col_name == 'salary_type_salary':
        offer['min_salary_type_salary'] = ''
        offer['max_salary_type_salary'] = ''
  offer['tags'] = tags

  if is_1st_page:
    with open('./output/offers.csv', 'w') as f:
      cols = list(offer.keys())
      writer = csv.DictWriter(f, cols)
      writer.writeheader()
      writer.writerow(offer)
  else:
    with open('./output/offers.csv', 'a') as f:
      cols = list(offer.keys())
      writer = csv.DictWriter(f, cols)
      writer.writerow(offer)
