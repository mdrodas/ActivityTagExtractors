class Address:

    def __init__(self, street):
        self.rid = ""
        self.new(street, "", "", "", "", "", "", "")

    def new(self, street, city, country, state, nr, postcode, lat, lon):
        self.street = street  # String
        self.city = city  # String
        self.country = country  # String
        self.state = state  # String
        self.nr = nr  # String
        self.postcode = postcode  # String
        self.lat = lat  # String
        self.lon = lon  # String

    def toDict(self):
        address = dict(
            street=self.street,
            city=self.city,
            country=self.country,
            state=self.state,
            nr=self.nr,
            postcode=self.postcode,
            lat=self.lat,
            lon=self.lon,
        )
        return address


if __name__ == "__main__":
    directory = '../resources/model_examples/'
    with open(directory + 'Address.osql', 'a', newline='') as outfile:
        for i in range(1):
            a = Address("street_name")
            cmd = "INSERT INTO Address CONTENT {0}".format(a.toDict())
            print(cmd)
            outfile.write(cmd + ';\n')
            outfile.flush()
