import zillow
from address_handling import address_zip_extract
from helper import dec, enc


def zillow_api(address):
    zip_code = address_zip_extract(address)
    key = dec('M1-OLo18g1trev4fo_pu1if', 15)
    print(enc('Ba7QJZL6tJvzO4yG'))
    print(dec(enc('Ba7QJZL6tJvzO4yG')))

    if zip_code == '':
        zip_code = '98058'
        address = '1309 Harrington Ave SE, Renton'
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
