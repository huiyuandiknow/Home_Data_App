#Fake data for testing
# If received any existing address in our fake list --> result = the price in our fake data
#  else a concatenated of inputted data will return
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
    res = ""
    for el in fake_list:
        if el['address'] == address:
            res = el['price']
        else:
            res = address+" " + h_type+" " + beds + " " + baths

    return res
