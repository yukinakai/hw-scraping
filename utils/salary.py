# 給与のテキスト情報から最大最小の給与額を数値で抽出する
def min_max_salary(salary):
  if '〜' in salary:
    salary = salary.split('〜')
    _min_salary = salary[0].replace('円', '').replace('¥', '').replace('￥', '').replace(',', '')
    _max_salary = salary[1].replace('円', '').replace('¥', '').replace('￥', '').replace(',', '')
  else:
    _min_salary = salary.replace('円', '').replace('¥', '').replace('￥', '').replace(',', '')
    _max_salary = salary.replace('円', '').replace('¥', '').replace('￥', '').replace(',', '')

  if _min_salary.isdecimal():
    min_salary = int(_min_salary)
  else:
    min_salary = ''
  if _max_salary.isdecimal():
    max_salary = int(_max_salary)
  else:
    max_salary = ''
  return min_salary, max_salary
