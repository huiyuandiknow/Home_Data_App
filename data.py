#Fake data for testing
def Results(address, h_type, beds, baths):
    fake_list = [
        {
            'id': 1,
            'price': '$299,000',
            'zillowPrice': '$288,000',
            'date': '02-01-218',
            'address': "address1"
           
        },
         {
            'id': 2,
            'price': '$189,099',
            'zillowPrice': '$288,000',
            'date': '02-01-218',
            'address': "address2"
           
        }
    ]
    price = ""
    for el in fake_list:
        if el['address'] == address:
            price = el['price']

    res = (price+" "+address+" "+h_type+" "+beds+" "+ baths)

    return res
