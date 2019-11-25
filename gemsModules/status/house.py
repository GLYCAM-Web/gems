"""
Testing schema inheritance with pydantic:
House is generic. All houses have:
    windowCount: int
    floorCount:  int

Apartment is a specific type of house:
    aptNumber: int
"""


class House():
    street: str
    houseNumber: int
    def __init__(self, street, houseNumber):
        self.street = street
        self.houseNumber = houseNumber

    def getAddress(self):
        ##print("self.houseNumber: " + str(self.houseNumber))
        return str(self.houseNumber) + " " + self.street

class Apartment(House):
    aptNumber: int
    def __init__(self, street, houseNumber, aptNumber):
        super().__init__(street, houseNumber)
        self.aptNumber = aptNumber

    def getAddress(self):
        return str(self.houseNumber) + " " + self.street + ", apt# " + str(self.aptNumber)

# class Apartment(House):
#     aptNumber: int

#     def __init__()

if __name__ == "__main__":

    myHouse = House("Easy St.", 314)
    yourHouse = Apartment("Main Street", 10, 2)

    print("my address: " + myHouse.getAddress())
    print("your address: " + yourHouse.getAddress())
