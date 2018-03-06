from address_handling import Address
from address_handling import address_zip_extract, is_king_county
from db_model import existing_address
from helper import num
from model import main_model
from zillow_api_handler import zillow_api


class Results:
    """It represents a ready to use result as object.

    """
    home_zip = ''
    val = 'wrong data entered'
    comps = []
    zillow = ''
    has_zillow = False
    has_model_data = False

    def __init__(self, address, living, beds, baths, lot, year):
        self.address = address
        self.living = living
        self.beds = beds
        self.baths = baths
        self.lot = lot
        self.year = year

    def check(self):
        if self.beds == '':
            self.beds = 2
        if self.beds == '5+':
            self.beds = '5'
        if self.baths == '':
            self.baths = '1'
        if num(self.living) is None:
            self.living = '1800'
        if num(self.lot) is None:
            self.lot = '6000'
        if num(self.year) is None:
            self.year = '1959'

    def get_result(self):
        self.check()
        data = ''
        home_address = Address(self.address)
        if home_address.is_zip_good():
            self.home_zip = home_address.zip_code
            if home_address.is_king_county():
                self.val = main_model(self.home_zip, int(self.living), int(self.beds), int(self.baths), int(self.lot),
                                      int(self.year))
                self.has_model_data = True
            if home_address.is_address_good():
                data = zillow_api(self.address)
            if not isinstance(data, str):
                self.zillow = data['principal'].get_dict()
                self.val = self.zillow['zestimate']['amount']
                self.has_zillow = True
                if not isinstance(data['comps'], str):
                    for el in data['comps']:
                        self.comps.append(el.get_dict())

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


