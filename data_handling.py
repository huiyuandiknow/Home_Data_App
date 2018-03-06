from address_handling import address_zip_extract, is_king_county
from db_model import existing_address
from helper import num
from model import main_model
from zillow_api_handler import zillow_api


def results(address, living, beds, baths, lot, year):
    print(existing_address(address, living, beds, baths, lot, year))
    if beds == '':
        beds = '2'
    if beds == '5+':
        beds = '5'
    if baths == '':
        baths = '1'

    res = ''
    home_zip = address_zip_extract(address)
    comps = []
    if home_zip != '':
        if is_king_county(home_zip):
            if num(living) is not None:
                liv = living

            else:
                liv = '1800'
            if num(lot) is not None:
                lt = lot
            else:
                lt = '6000'
            if num(year) is not None:
                ye = year
            else:
                ye = '1959'
            house = '{"1":{"bedrooms":' + '"' + beds + '"' + ',"bathrooms":"' + baths + '","sqft_living":"' + liv + \
                    '","sqft_lot":"' + lt + '","zipcode":"' + home_zip + '"}}'
            # val = model_rez(house)
            val = main_model(int(home_zip), int(liv), int(beds), int(baths), int(lt), int(ye))
            res = {'val': val, "beds": beds, "baths": baths, "liv": liv, "lt": lt, "zipcode": home_zip, "year": ye}
        data = zillow_api(address)
        if not isinstance(data, str):
            for el in data['comps']:
                comps.append(el.get_dict())
        result = {'zillow': data, 'model': res, 'comps': comps}

    else:
        result = ''
    return result


