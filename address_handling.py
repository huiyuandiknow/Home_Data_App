import usaddress


class Address:
    zip_good = False
    king_county = False
    zip_code = 0
    zip_extracted = False
    address_good = False

    def __init__(self, address):
        self.address = address

    def zip_extract(self):
        addr = ["",""]
        try:
            addr = usaddress.tag(self.address)
        except:
            self.zip_extracted = True
            addr[1] = 'ambiguous'
        if addr[1] != 'ambiguous':
            for key, val in addr[0].items():
                if key == "ZipCode":
                    self.zip_code = int(val)
                    self.zip_good = True
                    self.zip_extracted = True
                    if addr[1] is not 'Ambiguous':
                        self.address_good = True
                    break

    def is_zip_good(self):
        if not self.zip_extracted:
            self.zip_extract()
        return self.zip_good

    def is_address_good(self):
        if not self.zip_extracted:
            self.zip_extract()
        return self.address_good

    def is_king_county(self):
        if not self.zip_good:
            self.zip_extract()
        if self.zip_good:
            my_zip = (
                98126, 98133, 98136, 98134, 98138, 98144, 98146, 98148, 98155, 98154, 98158, 98164, 98166, 98168, 98177,
                98178,
                98190, 98188,
                98198, 98195, 98199, 98224, 98251, 98288, 98354, 98001, 98003, 98002, 98005, 98004, 98007, 98006, 98009,
                98008,
                98011, 98010,
                98014, 98019, 98022, 98024, 98023, 98025, 98028, 98027, 98030, 98029, 98032, 98031, 98034, 98033, 98038,
                98040,
                98039, 98042,
                98045, 98047, 98051, 98050, 98053, 98052, 98055, 98057, 98056, 98059, 98058, 98068, 98065, 98070, 98072,
                98075,
                98074, 98077,
                98083, 98092, 98101, 98103, 98102, 98105, 98104, 98107, 98106, 98109, 98108, 98112, 98115, 98114, 98117,
                98116,
                98119, 98118,
                98122, 98121, 98125)
            if self.zip_code in my_zip:
                self.king_county = True
        return self.king_county

