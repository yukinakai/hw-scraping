def get_various_licenses(soup):
    license_names =  soup.select('#ID_MenkyoSkkuMeisho')
    license_required = soup.select('#ID_MenkyoSkkuSel')
    various_licenses = list()
    if len(license_names) > 0:
        for i, license_name in enumerate(license_names):
            license = license_name.text.strip() + '(' + license_required[i].text.strip() + ')'
            various_licenses.append(license)
    return ('、').join(various_licenses)
