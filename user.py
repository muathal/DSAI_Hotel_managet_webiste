# user.py
class User:
    #super class
    def __init__(self, name):
        self.name = name



class Guest(User):
    def __init__(self, name, phone):
        super().__init__(name)
        self.__phone = phone
        self.booking = None



class Employee(User):
    #manage the hotel
    def __init__(self, name, emp_id):
        super().__init__(name)
        self.__emp_id = emp_id

    def add_room(self, hotel, number, room_type, price):
        hotel.add_room(number, room_type, price)

    def remove_room(self, hotel, room_number):
        hotel.remove_room(room_number)