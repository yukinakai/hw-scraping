def get_offer_val(offers, element_id):
    if element_id in offers:
        offer_val = offers[element_id]
    else:
        offer_val = ''
    return offer_val
