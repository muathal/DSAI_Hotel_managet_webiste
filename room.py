class Room:
    def __init__(self, number , room_type, price):# Initialize room information
        
        self.number = number
        self.room_type = room_type
        self.price = price

        self.status = "Available"

        self.guests = []

    def add_guest(self, guest):# Add a guest to the room


        if len(self.guests) < 3:
            self.guests.append(guest)

            if len(self.guests) == 3:     # If room reaches 3 guests → mark as Full
                self.status = "Full"
                return True

        # Return False if room is already full
        return False

    def remove_guest(self, guest):  # Remove a guest from the room


        # Check if the guest exists in the room
        if guest in self.guests:
            self.guests.remove(guest)
            self.status = "Available"
            return True

        # Return False if guest was not found
        return False