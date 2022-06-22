def get_various_licenses(soup):
    license_names =  soup.select('#ID_MenkyoSkkuMeisho')
    license_required = soup.select('#ID_MenkyoSkkuSel')
    various_licenses = list()
    if len(license_names) > 0:
        for i, license_name in enumerate(license_names):
            license = dict()
            license['name'] = license_name
            license['required'] = license_required[i]
            various_licenses.append(license)
    else:
        various_licenses.append({
            'name': '',
            'required': ''
        })
    return various_licenses
