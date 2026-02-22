from room import Room

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def add_room(self, number, room_type, price):
        self.rooms.append(Room(number, room_type, price)) #list of roons: assign it as object -composition relation-

    def remove_room(self, room_number):
        self.rooms = [r for r in self.rooms if r.number != room_number] #give me new list with all rooms that its number != room_number

    def list_rooms(self):
        for r in self.rooms:
            print(f"{r.number} | {r.room_type} | {r.price} | {r.status}")

    def book_room(self, guest, room_number):
        room = next((r for r in self.rooms if r.number == room_number), None) #retrieve the next item from an iterator next(iterator, default)
        if not room:
            print("Room not found")
            return False

        if room.add_guest(guest):
            guest.booking = room
            print("Booking successful")
            return True

        print("Room full")
        return False

    def cancel_booking(self, guest):
        if guest.booking:
            guest.booking.remove_guest(guest)
            guest.booking = None
            print("Booking cancelled")

    def find_guest_by_phone(self, phone):
        for room in self.rooms:
            for g in room.guests:
                if getattr(g, "phone", None) == phone:
                    return g, room
        return None, None
