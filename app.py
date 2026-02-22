import streamlit as st
from hotel import Hotel
from user import Employee, Guest
#from history import save_history
import json

st.set_page_config(page_title="Hotel System", page_icon="🏨", layout="wide")


# Session State
if "hotel" not in st.session_state:
    st.session_state.hotel = Hotel("Hotel")

if "guest" not in st.session_state:
    st.session_state.guest = None

if "employee" not in st.session_state:
    st.session_state.employee = None

if "role" not in st.session_state:
    st.session_state.role = None

hotel = st.session_state.hotel
guest = st.session_state.guest
employee = st.session_state.employee

#  Helpers

#save the hisory in file
def save_history(guest, nights, cost):
    try:
        with open("history.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "name": guest.name,
        "phone": guest.phone,
        "nights": nights,
        "cost": cost
    })

    with open("history.json", "w") as f:
        json.dump(data, f, indent=4)



def show_rooms(rooms):
    try:
        if not rooms:
            st.info("No rooms found.")
            return

        for r in rooms:
            st.markdown(
                f"""
                **Room {r.number}**
                - Type: `{r.room_type}`
                - Price: `{r.price}`
                - Status: `{r.status}`
                - Guests: `{len(r.guests)}/1`
                """
            )
            st.divider()
    except Exception as e:
        st.error(f"Error displaying rooms: {e}")


def search_rooms_ui():
    st.subheader("Search Rooms")
    q = st.text_input("Search by room number or type")
    if st.button("Search"):
        try:
            key = (q or "").strip().lower()
            results = [
                r for r in hotel.rooms
                if key in str(r.number).lower()
                or key in str(r.room_type).lower()
            ]
            show_rooms(results)
        except Exception as e:
            st.error(f"Search failed: {e}")
def sort_rooms_ui():
    st.subheader("Sort Rooms by Price")

    only_available = st.checkbox(
        "Show only rooms that are not full", value=False
    )

    try:
        rooms_list = hotel.rooms
        if only_available:
            rooms_list = [r for r in rooms_list if r.status != "Full"]

        sorted_rooms = sorted(rooms_list, key=lambda r: r.price) #lambda function
        show_rooms(sorted_rooms)

    except Exception as e:
        st.error(f"Sort failed: {e}")

st.title("🏨 Hotel Management System")


if st.session_state.role is None:
    st.header("Select User Type")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👨‍💼 Employee"):
            st.session_state.role = "employee"
            st.rerun()

    with col2:
        if st.button("🧳 Guest"):
            st.session_state.role = "guest"
            st.rerun()

    st.stop()

# EMPLOYEE FLOW
if st.session_state.role == "employee":
    st.sidebar.title("Employee Menu")

    if employee is None:
        st.header("Employee Login")

        emp_name = st.text_input("Employee Name")
        emp_id = st.text_input("Employee ID")

        if st.button("Login as Employee"):
            if emp_name.strip() and emp_id.strip():
                try:
                    st.session_state.employee = Employee(
                        emp_name.strip(), emp_id.strip()
                    )
                    st.success("Employee logged in")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")
            else:
                st.warning("Please enter name and ID")

    else:
        st.success(f"Logged in as {employee.name}")

        menu = st.sidebar.radio(
            "Menu",
            ["Add Room", "Manage Rooms", "View Rooms", "Logout"],
        )

        #  Add Room
        if menu == "Add Room":
            st.header("Add Room")

            number = st.number_input("Room Number", min_value=1, step=1)
            room_type = st.selectbox("Room Type", ["VIP", "Normal"])
            price = st.number_input("Price", min_value=0.0, step=50.0)

            if st.button("Add Room"):
                try:
                    if (len(hotel.rooms) != 0):
                        for room in hotel.rooms:
                            if number == room.number:
                                exist = True
                                break
                            else:
                                exist = False

                    else:
                        exist = False
                    if not exist:
                        employee.add_room(hotel, int(number), room_type, float(price))
                        st.success("Room added")
                        st.rerun()
                    else:
                        st.error("room does exist")
                except Exception as e:
                    st.error(f"Failed to add room: {e}")

        #  Manage Rooms
        elif menu == "Manage Rooms":
            st.header("Manage Rooms")

            if not hotel.rooms:
                st.info("No rooms available")
            else:
                for r in hotel.rooms:
                    c1, c2 = st.columns([4, 1])
                    c1.write(
                        f"Room {r.number} | {r.room_type} | {r.price} | "
                        f"{r.status} | Guests: {len(r.guests)}/1"
                    )
                    if c2.button("Delete", key=f"del_{r.number}"):
                        try:
                            employee.remove_room(hotel, r.number)
                            st.success("Room deleted")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Delete failed: {e}")

        # View Rooms
        elif menu == "View Rooms":
            st.header("All Rooms")
            show_rooms(hotel.rooms)

        #  Logout
        elif menu == "Logout":
            st.session_state.employee = None
            st.session_state.role = None
            st.rerun()

# GUEST FLOW
elif st.session_state.role == "guest":
    st.sidebar.title("Guest Menu")

    # Login
    if guest is None:
        st.header("Guest Login")

        g_name = st.text_input("Guest Name")
        g_phone = st.text_input("Phone Number")

        if st.button("Login as Guest"):
            if g_name.strip() and g_phone.strip():
                try:
                    phone = g_phone.strip()

                    existing_guest, existing_room = hotel.find_guest_by_phone(phone)

                    if existing_guest:
                        existing_guest.booking = existing_room
                        st.session_state.guest = existing_guest
                    else:
                        st.session_state.guest = Guest(g_name.strip(), phone)

                    st.success("Guest logged in")
                    st.rerun()

                except Exception as e:
                    st.error(f"Login failed: {e}")
            else:
                st.warning("Please enter name and phone")

    # After Login
    else:
        st.success(f"Welcome {guest.name}")

        menu = st.sidebar.radio(
            "Menu",
            [
                "View Rooms",
                "Search Rooms",
                "Sort Rooms",
                "Book Room",
                "Cancel Booking",
                "Checkout",
                "Logout",
            ],
        )

        # View Rooms
        if menu == "View Rooms":
            st.header("Available Rooms")
            show_rooms(hotel.rooms)

        # Search Rooms
        elif menu == "Search Rooms":
            search_rooms_ui()
        elif menu == "Sort Rooms":
            sort_rooms_ui()
        # Book Room
        elif menu == "Book Room":
            st.header("Book Room")

            available_rooms = [r for r in hotel.rooms if r.status != "Full"]

            if not available_rooms:
                st.warning("No rooms available")
            else:
                room_numbers = [r.number for r in available_rooms]
                selected = st.selectbox("Select Room", room_numbers)

                if st.button("Book"):
                    try:
                        ok = hotel.book_room(guest, selected)
                        if ok:
                            st.success("Booking successful")
                            st.rerun()
                        else:
                            st.error("Booking failed")
                    except Exception as e:
                        st.error(f"Booking error: {e}")

        # Cancel
        elif menu == "Cancel Booking":
            if guest.booking is None:
                st.info("No active booking")
            else:
                st.write(f"Current room: {guest.booking.number}")
                if st.button("Cancel Booking"):
                    try:
                        hotel.cancel_booking(guest)
                        st.success("Booking cancelled")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Cancel failed: {e}")

        # Checkout
        elif menu == "Checkout":
            if guest.booking is None:
                st.info("No active booking")
            else:
                room = guest.booking
                nights = st.number_input("Number of Nights", min_value=1, step=1)
                total = float(nights) * float(room.price)

                st.subheader("Invoice")
                st.write(f"Total: {total}")

                if st.button("Confirm Check-out"):
                    try:
                        save_history(guest, nights, total)
                        hotel.cancel_booking(guest)
                        st.success(f"Check-out complete. Total Cost: {total}")
                        st.session_state.guest = None
                        st.rerun()
                    except Exception as e:
                        st.error(f"Checkout failed: {e}")

        # Logout
        elif menu == "Logout":
            st.session_state.guest = None
            st.session_state.role = None

            st.rerun()

