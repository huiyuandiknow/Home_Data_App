from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import zillow
import usaddress
from model import main_model

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user2db2:123456@67.215.253.70:3306/user2db2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@67.215.253.70:3306/user1db1'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1db1:123456@localhost:8889/user1db1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
file = None

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(160), unique=True)
    beds = db.Column(db.Integer)
    baths = db.Column(db.Integer)
    h_type = db.Column(db.String(20))
    price = db.Column(db.Integer)

    def __init__(self, address, beds, baths, h_type):
        self.address = address
        self.beds = beds
        self.baths = baths
        self.baths = h_type


def results(address, living, beds, baths, lot, year):

    # existing_address = Property.query.filter_by(address=address).first()
    #
    # if existing_address:
    #     res = existing_address.price
    # else:
    #     res = address + " " + living + " " + beds + " " + baths+" " + lot
    if beds == '':
        beds = '2'
    if beds == '5+':
        beds = '5'
    if baths == '':
        baths = '1'

    res =''
    home_zip = address_zip_extract(address)
    comps = []
    if home_zip != '':
        if is_king_county(home_zip):
            if num(living) is not None:
                liv = living

            else: liv = '1800'
            if num(lot) is not None:
                lt = lot
            else:
                lt = '6000'
            if num(year) is not None:
                ye = year
            else:
                ye = '1959'
            house = '{"1":{"bedrooms":' + '"'+beds+'"' + ',"bathrooms":"' + baths + '","sqft_living":"'+liv + \
                    '","sqft_lot":"' + lt +'","zipcode":"' + home_zip+'"}}'
            #val = model_rez(house)
            val = main_model(int(home_zip), int(liv), int(beds), int(baths), int(lt),int(ye))
            res = {'val':val, "beds":beds, "baths":baths, "liv":liv, "lt":lt, "zipcode":home_zip, "year":ye}
        data = zillow_api(address)
        if not isinstance(data, str):
            for el in data['comps']:
                comps.append(el.get_dict())
        result = {'zillow': data, 'model': res, 'comps': comps}

    else:
        result = ''
    return result

def is_king_county(zip_code):
    zip =(98126,98133,98136,98134,98138,98144,98146,98148,98155,98154,98158,98164,98166,98168,98177,98178,98190,98188,
         98198,98195,98199,98224,98251,98288,98354,98001,98003,98002,98005,98004,98007,98006,98009,98008,98011,98010,
         98014,98019,98022,98024,98023,98025,98028,98027,98030,98029,98032,98031,98034,98033,98038,98040,98039,98042,
         98045,98047,98051,98050,98053,98052,98055,98057,98056,98059,98058,98068,98065,98070,98072,98075,98074,98077,
         98083,98092,98101,98103,98102,98105,98104,98107,98106,98109,98108,98112,98115,98114,98117,98116,98119,98118,
         98122,98121,98125)
    return int(zip_code) in zip

def address_zip_extract(address):
    addr = usaddress.tag(address)
    zip_code = ''
    if addr[1] != 'ambiguous':
        for key, val in addr[0].items():
            if key == "ZipCode":
                zip_code = val
                break
    return zip_code

def zillow_api(address):

    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = 'zillow_key.conf'
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as f:
        key = f.readline().replace("\n", "")
    zip_code = address_zip_extract(address)
    if zip_code == '':
        zip_code = '98058'
        address = '1309 Harrington Ave SE, Renton'
    api = zillow.ValuationApi()
    data = api.GetDeepSearchResults(key, address, zip_code)
    if not isinstance(data, str):
        full_data = api.GetDeepComps(key, data.zpid)
        full_data['principal'].extended_data = data.extended_data
        return full_data
    else:
        return "Wrong address"

def num(s):
    try:
        return int(s)
    except ValueError:
        return None