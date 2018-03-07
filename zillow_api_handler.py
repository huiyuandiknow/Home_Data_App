import zillow
from address_handling import Address
from helper import dec


def zillow_api(address):
    home_address = Address(address)
    if home_address.is_zip_good():
        zip_code = home_address.zip_code
    else:
        zip_code = '98058'
        address = '1309 Harrington Ave SE, Renton'
    key = dec('M1-OLo18g1trev4fo_pu1if', 15)
    api = zillow.ValuationApi()
    data = api.GetDeepSearchResults(key, address, zip_code)
    if not isinstance(data, str):
        full_data = api.GetDeepComps(key, data.zpid)
        if not isinstance(full_data, str):
            full_data['principal'].extended_data = data.extended_data
        else:
            full_data = {
                'principal': data,
                'comps': [data]
            }
        return full_data
    else:
        return "Wrong address"
