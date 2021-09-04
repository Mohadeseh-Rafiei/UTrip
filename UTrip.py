import csv


class Tools:
    def __init__(self) -> None:
        pass


class Room:
    _room_types = {
        "standard": "s",
        "deluxe": "d",
        "luxury": "l",
        "premium": "p"
    }

    def __init__(self, hotel_id: str, room_type: str, room_id: int, price: int) -> None:
        self.room_id = self._room_types[room_type] + str(room_id)
        self.price = price
        self.hotel_id = hotel_id
        self.room_type = room_type
        self.reserved_day = dict()

    def set_reserved_day(self) -> None:
        for i in range(1, 31):
            self.reserved_day[i] = False

    def reserved_this_room(self, check_in: int, check_out: int) -> None:
        for day in range(check_in, check_out + 1):
            self.reserved_day[day] = True

    def free_reserved_room(self, check_in: int, check_out: int) -> None:
        for day in range(check_in, check_out + 1):
            self.reserved_day[day] = False


class RoomsManager:
    def __init__(self) -> None:
        self.all_rooms = {
            "standard": dict(),
            "deluxe": dict(),
            "luxury": dict(),
            "premium": dict()
        }

    def add_n_rooms(self, hotel_id: str, room_type: str, n: int, price: int) -> None:
        for i in range(1, n + 1):
            the_room = Room(hotel_id, room_type, i, price)
            the_room.set_reserved_day()
            self.all_rooms[room_type][the_room.room_id] = the_room

    def num_of_room_types(self) -> int:
        return len(self.all_rooms)

    def empty_rooms_type_in_time(self, room_type: str, check_in: int, check_out: int, quantity: int) -> list:
        empty_room_for_reserved = list()
        for room in self.all_rooms[room_type].items():
            flag = True
            for day in range(check_in, check_out + 1):
                if room[1].reserved_day[day]:
                    flag = False
                    break
            if flag:
                empty_room_for_reserved.append(room)
                if quantity == len(empty_room_for_reserved):
                    return empty_room_for_reserved
        return empty_room_for_reserved

    @staticmethod
    def reserve_this_rooms(room: list, check_in: int, check_out: int) -> list:
        final_rooms = list()
        for the_room in room:
            the_room[1].reserved_this_room(check_in, check_out)
            final_rooms.append(the_room)
        return final_rooms


class Hotel:
    def __init__(self, unique_id: str, property_name: str, hotel_star_rating: int, hotel_overview: str,
                 property_amenities: str, city: str, latitude: float, longitude: float, image_url: str,
                 num_of_standard_rooms: int, num_of_deluxe_rooms: int, num_of_luxury_rooms: int,
                 num_of_premium_rooms: int, standard_room_price: int, deluxe_room_price: int, luxury_room_price: int,
                 premium_room_price: int
                 ) -> None:
        self.rooms_manager = RoomsManager()
        self.unique_id = unique_id
        self.property_name = property_name
        self.hotel_star_rating = hotel_star_rating
        self.hotel_overview = hotel_overview
        self.property_amenities = property_amenities
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.image_url = image_url
        self.standard_room_price = standard_room_price
        self.deluxe_room_price = deluxe_room_price
        self.luxury_room_price = luxury_room_price
        self.premium_room_price = premium_room_price
        self.rooms_manager.add_n_rooms(self.unique_id, "standard", num_of_standard_rooms, standard_room_price)
        self.rooms_manager.add_n_rooms(self.unique_id, "deluxe", num_of_deluxe_rooms, deluxe_room_price)
        self.rooms_manager.add_n_rooms(self.unique_id, "luxury", num_of_luxury_rooms, luxury_room_price)
        self.rooms_manager.add_n_rooms(self.unique_id, "premium", num_of_premium_rooms, premium_room_price)
        self.total_num_of_room = (num_of_standard_rooms + num_of_deluxe_rooms +
                                  num_of_luxury_rooms + num_of_premium_rooms)
        self.active_type_of_rooms = self.rooms_manager.num_of_room_types()
        self.sum_of_price = standard_room_price + deluxe_room_price + luxury_room_price + premium_room_price

    def average_of_prices(self) -> float:
        if self.total_num_of_room == 0:
            return 0
        return round(self.sum_of_price / self.active_type_of_rooms, 2)


class HotelsManager:
    all_hotel = dict()

    def __init__(self) -> None:
        pass

    def add_hotel(self, hotel: Hotel) -> None:
        self.all_hotel[hotel.unique_id] = hotel

    def get_hotels(self) -> list:
        hotels_sorted_key = sorted(self.all_hotel.keys())
        return hotels_sorted_key

    def is_there_available_room(self, hotel_id: str, room_type: str, quantity: int, check_in: int,
                                check_out: int) -> list:
        rooms = self.all_hotel[hotel_id].rooms_manager.empty_rooms_type_in_time(room_type, check_in,
                                                                                check_out, quantity)
        if len(rooms) < quantity:
            raise Exception("empty")
        return rooms

    def get_room(self, hotel_id: str, room_id: str, room_type: str) -> Room:
        return self.all_hotel[hotel_id].rooms_manager.all_rooms[room_type][room_id]


class Filter:
    hotels_id = HotelsManager.all_hotel
    filters_type = dict()

    def __init__(self) -> None:
        pass

    @staticmethod
    def add_city_filter(city: str) -> None:
        Filter.filters_type["city"] = city

    @staticmethod
    def add_star_filter(min_star: int, max_star: int) -> None:
        Filter.filters_type["star"] = {
            "min_star": min_star,
            "max_star": max_star
        }

    @staticmethod
    def add_average_price_filter(min_price: int, max_price: int) -> None:
        Filter.filters_type["average_price"] = {
            "min_price": min_price,
            "max_price": max_price
        }

    @staticmethod
    def add_available_room_filter(room_type: str, quantity: int, check_in: int, check_out: int) -> None:
        Filter.filters_type["available_room"] = {
            "type": room_type,
            "quantity": quantity,
            "check_in": check_in,
            "check_out": check_out
        }

    @staticmethod
    def delete_filters() -> None:
        Filter.filters_type.clear()


class CityFilter(Filter):
    def __init__(self):
        super(Filter, self).__init__()

    @staticmethod
    def apply_filter(city: str, hotels_id: list) -> list:
        filtered = list()
        for hotel_id in hotels_id:
            if city == HotelsManager.all_hotel[hotel_id].city:
                filtered.append(hotel_id)
        return filtered


class StarFilter(Filter):
    def __init__(self):
        super(Filter, self).__init__()

    @staticmethod
    def apply_filter(min_star: int, max_star: int, hotels_id: list) -> list:
        filtered = list()
        for hotel_id in hotels_id:
            if min_star <= HotelsManager.all_hotel[hotel_id].hotel_star_rating <= max_star:
                filtered.append(hotel_id)
        return filtered


class AveragePriceFilter(Filter):
    def __init__(self):
        super(Filter, self).__init__()

    @staticmethod
    def apply_filter(min_price: int, max_price: int, hotels_id: list) -> list:
        filtered = list()
        for hotel_id in hotels_id:
            if min_price <= HotelsManager.all_hotel[hotel_id].average_of_price() <= max_price:
                filtered.append(hotel_id)
        return filtered


class AvailableRoomFilter(Filter):
    def __init__(self):
        super(Filter, self).__init__()

    @staticmethod
    def apply_filter(room_type: str, quantity: int, check_in: int, check_out: int, hotels_id: list) -> list:
        filtered = list()
        for hotel_id in hotels_id:
            empties = HotelsManager.all_hotel[hotel_id].rooms_manager.empty_rooms_type_in_time(room_type, check_in,
                                                                                               check_out, quantity)
            if quantity == len(empties):
                filtered.append(hotel_id)
        return filtered


class Reserve:
    _reserve_id = 1

    def __init__(self, hotel_id: str, rooms: list, room_type: str, cost: int, check_in: int,
                 check_out: int, quantity: int) -> None:
        self.hotel_id = hotel_id
        self.id = self._reserve_id
        self.rooms = rooms
        self.room_type = room_type
        self.cost = cost
        self.check_in = check_in
        self.check_out = check_out
        self.quantity = quantity
        self._reserve_id += 1


class User:
    def __init__(self, email: str, username: str, password: str) -> None:
        self.email = email
        self.username = username
        self._password = password
        self.wallet = 0
        self.wallet_history = list()
        self.reserved = dict()

    def get_password(self) -> str:
        return self._password

    def add_reserve(self, hotel_id: str, rooms: list, room_type: str, cost: int, check_in: int, check_out: int,
                    quantity: int) -> None:
        reserved = Reserve(hotel_id, rooms, room_type, cost, check_in, check_out, quantity)
        self.reserved[reserved.id] = reserved


class UserManger:
    current_user = None

    def __init__(self) -> None:
        self._all_users = dict()

    def set_current_user(self, email: str) -> None:
        self.current_user = self._all_users[email]

    def add_user(self, user: User) -> None:
        self._all_users[user.email] = user
        self.set_current_user(user.email)

    def there_is_a_user_with_this_email(self, email: str) -> bool:
        return email in self._all_users

    def there_is_a_user_with_this_username(self, username: str) -> bool:
        for user_email in self._all_users:
            if self._all_users[user_email].username == username:
                return True
        return False

    def check_matching_password_with_email(self, email: str, password: str) -> None:
        return self._all_users[email].get_password() == password

    def add_wallet(self, amount: int) -> None:
        self.current_user.wallet_history.append(self.current_user.wallet)
        self.current_user.wallet += amount

    def get_wallet(self, count: int) -> list:
        if count < len(self.current_user.wallet_history):
            return self.current_user.wallet_history[-count:]
        return self.current_user.wallet_history

    def user_have_credit(self, amount: int, quantity: int) -> bool:
        if self.current_user.wallet < amount * quantity:
            return False
        self.current_user.wallet -= amount * quantity
        return True

    def remove_reserved_room_from_user_reserved(self, reserved_id: int) -> None:
        if reserved_id not in self.current_user.reserved:
            raise Exception("not_found")
        self.current_user.reserved.pop(reserved_id)


class UtRip:
    def __init__(self) -> None:
        self._hotels_manager = HotelsManager()
        self._user_manager = UserManger()

    def add_hotel(self, hotel: Hotel) -> None:
        self._hotels_manager.add_hotel(hotel)

    def signup(self, email: str, username: str, password: str) -> None:
        if self._user_manager.there_is_a_user_with_this_username(username):
            raise Exception("bad_request")
        if self._user_manager.there_is_a_user_with_this_email(email):
            raise Exception("bad_request")
        the_user = User(email, username, password)
        self._user_manager.add_user(the_user)

    def login(self, email: str, password: str) -> None:
        if not self._user_manager.there_is_a_user_with_this_email(email):
            raise Exception("bad_request")
        if not self._user_manager.check_matching_password_with_email(email, password):
            raise Exception("bad_request")
        if self._user_manager.current_user is not None:
            raise Exception("bad_request")
        self._user_manager.set_current_user(email)

    def logout(self) -> None:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        self._user_manager.current_user = None

    def post_wallet(self, amount: int) -> None:
        if amount < 0:
            raise Exception("bad_request")
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        self._user_manager.add_wallet(amount)

    def get_wallet(self, count: int) -> list:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        return self._user_manager.get_wallet(count)

    def get_hotels(self) -> list:
        hotels_id = self._hotels_manager.get_hotels()
        if len(hotels_id) == 0:
            raise Exception("empty")
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        return hotels_id

    def get_hotel(self, hotel_id: str) -> Hotel:
        if hotel_id not in self._hotels_manager.all_hotel:
            raise Exception("not_found")
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        return self._hotels_manager.all_hotel[hotel_id]

    def add_city_filter(self, city: str) -> None:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        Filter.add_city_filter(city)

    def add_average_price_filter(self, min_price: int, max_price: int) -> None:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        Filter.add_average_price_filter(min_price, max_price)

    def add_star_filter(self, min_star: int, max_star: int) -> None:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        Filter.add_star_filter(min_star, max_star)

    def add_available_room_filter(self, room_type: str, quantity: int, check_in: int, check_out: int) -> None:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        Filter.add_available_room_filter(room_type, quantity, check_in, check_out)

    @staticmethod
    def apply_filter_to_hotels(hotels_id: list) -> list:
        final = hotels_id
        for filter_type in Filter.filters_type.keys():
            if filter_type == "city":
                final = CityFilter.apply_filter(Filter.filters_type[filter_type], final)
            elif filter_type == "star":
                final = StarFilter.apply_filter(Filter.filters_type[filter_type]["min_star"],
                                                Filter.filters_type[filter_type]["max_star"], final)
            elif filter_type == "average_price":
                final = AveragePriceFilter.apply_filter(Filter.filters_type[filter_type]["min_price"],
                                                        Filter.filters_type[filter_type]["max_price"], final)
            elif filter_type == "available_room":
                final = AvailableRoomFilter.apply_filter(Filter.filters_type[filter_type]["type"],
                                                         Filter.filters_type[filter_type]["quantity"],
                                                         Filter.filters_type[filter_type]["check_in"],
                                                         Filter.filters_type[filter_type]["check_out"], final)
        final.sort()
        return final

    def delete_filters(self) -> None:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        Filter.delete_filters()

    def post_reserves(self, hotel_id: str, room_type: str, quantity: int, check_in: int, check_out: int) -> list:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        rooms = self._hotels_manager.is_there_available_room(hotel_id, room_type, quantity, check_in, check_out)
        if not self._user_manager.user_have_credit(rooms[0][1].price, quantity):
            raise Exception("not_enough_credit")
        cost = quantity * rooms[0][1].price
        rooms = self._hotels_manager.all_hotel[hotel_id].rooms_manager.reserve_this_rooms(rooms, check_in, check_out)
        self._user_manager.current_user.add_reserve(hotel_id, rooms, room_type, cost, check_in, check_out, quantity)
        return rooms

    def get_reserves(self) -> dict:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        reserved = self._user_manager.current_user.reserved
        if not reserved:
            raise Exception("empty")
        return reserved

    def cancel_reserved_room(self, reserved_id: int) -> None:
        if self._user_manager.current_user is None:
            raise Exception("permission_denied")
        check_in = self._user_manager.current_user.reserved[reserved_id].check_in
        check_out = self._user_manager.current_user.reserved[reserved_id].check_out
        for room in self._user_manager.current_user.reserved[reserved_id].rooms:
            self._hotels_manager.get_room(room[1].hotel_id, room[0], room[1].room_type).free_reserved_room(check_in,
                                                                                                           check_out)
        self._user_manager.remove_reserved_room_from_user_reserved(reserved_id)


class UserInterface:
    _messages = {
        "bad_request": "Bad Request",
        "permission_denied": "Permission Denied",
        "empty": "Empty",
        "not_found": "Not Found",
        "not_enough_credit": "Not Enough Credit"
    }
    data_sign = "?"

    def __init__(self) -> None:
        self._ut_rip = UtRip()
        self._dispatch = {
            "POST":
                {
                    "signup": self._signup,
                    "login": self._login,
                    "logout": self._logout,
                    "wallet": self._post_wallet,
                    "filters": self._filters,
                    "reserves": self._post_reserves
                },
            "GET":
                {
                    "wallet": self._get_wallet,
                    "hotels": self._get_hotels,
                    "reserves": self._get_reserves
                },
            "DELETE":
                {
                    "filters": self._delete_filters,
                    "reserves": self._cancel_reserved_room
                }
        }

    def _cancel_reserved_room(self, data: list) -> None:
        reserved_id = int(data[data.index("id") + 1])
        try:
            self._ut_rip.cancel_reserved_room(reserved_id)
            print("OK")
        except Exception as err:
            print(self._messages[str(err.args[0])])

    @staticmethod
    def _print_reserved(reserved: dict) -> None:
        for reserve in reserved:
            print("id:", reserved[reserve].id, end=" ")
            print("hotel:", reserved[reserve].hotel_id, end=" ")
            print("room:", reserved[reserve].room_type, end=" ")
            print("quantity:", reserved[reserve].quantity, end=" ")
            print("cost:", reserved[reserve].cost, end=" ")
            print("check_in", reserved[reserve].check_in, end=" ")
            print("check_out", reserved[reserve].check_out, end=" ")

    def _get_reserves(self, data: list) -> None:
        try:
            reserved = self._ut_rip.get_reserves()
            self._print_reserved(reserved)
        except Exception as err:
            print(self._messages[str(err.args[0])])

    @staticmethod
    def _print_reserved_room(room: list) -> None:
        for the_room in room:
            print(the_room[1].room_id, end=" ")
        print()

    def _post_reserves(self, data: list) -> None:
        hotel_id = data[data.index("hotel") + 1]
        room_type = data[data.index("type") + 1]
        quantity = int(data[data.index("quantity") + 1])
        check_in = int(data[data.index("check_in") + 1])
        check_out = int(data[data.index("check_out") + 1])
        try:
            room = self._ut_rip.post_reserves(hotel_id, room_type, quantity, check_in, check_out)
            self._print_reserved_room(room)
        except Exception as err:
            print(self._messages[str(err.args[0])])

    def _delete_filters(self, data: list) -> None:
        self._ut_rip.delete_filters()

    def _filters(self, data: list) -> None:
        filter_type = data[0]
        try:
            if filter_type == "city":
                self._ut_rip.add_city_filter(data[1])
            elif filter_type == "min_price" or filter_type == "max_price":
                min_price = int(data[data.index("min_price") + 1])
                max_price = int(data[data.index("max_price") + 1])
                self._ut_rip.add_average_price_filter(min_price, max_price)
            elif filter_type == "min_star" or filter_type == "max_star":
                min_star = int(data[data.index("min_star") + 1])
                max_star = int(data[data.index("max_star") + 1])
                self._ut_rip.add_star_filter(min_star, max_star)
            elif filter_type == "type" or filter_type == "quantity" or filter_type == "check_in" or filter_type == "check_out":
                room_type = data[data.index("type") + 1]
                quantity = int(data[data.index("quantity") + 1])
                check_in = int(data[data.index("check_in") + 1])
                check_out = int(data[data.index("check_out") + 1])
                self._ut_rip.add_available_room_filter(room_type, quantity, check_in, check_out)
            print("OK")
        except Exception as err:
            print(self._messages[str(err.args[0])])

    @staticmethod
    def _print_hotel_detail(hotel: Hotel) -> None:
        print(hotel.unique_id)
        print(hotel.property_name)
        print("star:", hotel.hotel_star_rating)
        print("overview:", hotel.hotel_overview)
        print("amenities:", hotel.property_amenities)
        print("city:", hotel.city)
        print("latitude:", hotel.latitude)
        print("longitude:", hotel.longitude)
        print("#rooms:", len(hotel.rooms_manager.all_rooms["standard"]), len(hotel.rooms_manager.all_rooms["deluxe"]),
              len(hotel.rooms_manager.all_rooms["luxury"]), len(hotel.rooms_manager.all_rooms["premium"]))
        print("prices:", hotel.standard_room_price, hotel.deluxe_room_price, hotel.luxury_room_price,
              hotel.premium_room_price)

    @staticmethod
    def _print_hotels(hotels_id: list) -> None:
        for hotel_id in hotels_id:
            the_hotel = HotelsManager.all_hotel[hotel_id]
            print(the_hotel.unique_id, the_hotel.property_name, the_hotel.city, the_hotel.total_num_of_room,
                  the_hotel.average_of_prices())

    def _get_hotels(self, data: list) -> None:
        try:
            if len(data) == 0:
                hotels_id = self._ut_rip.get_hotels()
                hotels_id = self._ut_rip.apply_filter_to_hotels(hotels_id)
                self._print_hotels(hotels_id)
            else:
                hotel_id = data[data.index("id") + 1]
                hotel = self._ut_rip.get_hotel(hotel_id)
                self._print_hotel_detail(hotel)
        except Exception as err:
            print(self._messages[str(err.args[0])])

    @staticmethod
    def _show_wallet_history(wallet_history: list) -> None:
        wallet_history.reverse()
        for wallet in wallet_history:
            print(wallet)

    def _get_wallet(self, data: list) -> None:
        count = int(data[data.index("count") + 1])
        try:
            wallet_history = self._ut_rip.get_wallet(count)
            self._show_wallet_history(wallet_history)
        except Exception as err:
            print(self._messages[str(err.args[0])])

    def _post_wallet(self, data: list) -> None:
        amount = int(data[data.index("amount") + 1])
        try:
            self._ut_rip.post_wallet(amount)
            print("OK")
        except Exception as err:
            print(self._messages[str(err.args[0])])

    def _logout(self, user_data: list) -> None:
        try:
            self._ut_rip.logout()
            print("OK")
        except Exception as err:
            print(self._messages[str(err.args[0])])

    def _login(self, user_data: list) -> None:
        email = user_data[user_data.index("email") + 1]
        password = user_data[user_data.index("password") + 1]
        try:
            self._ut_rip.login(email, password)
            print("OK")
        except Exception as err:
            print(self._messages[str(err.args[0])])

    def _signup(self, user_data: list) -> None:
        email = user_data[user_data.index("email") + 1]
        username = user_data[user_data.index("username") + 1]
        password = user_data[user_data.index("password") + 1]
        try:
            self._ut_rip.signup(email, username, password)
            print("OK")
        except Exception as err:
            print(self._messages[str(err.args[0])])

    def _get_command(self) -> None:
        while True:
            try:
                orders = input().split()
                if self.data_sign in orders:
                    orders.remove(self.data_sign)
                if orders[0] not in self._dispatch.keys():
                    raise Exception("bad_request")
                if orders[1] not in self._dispatch[orders[0]].keys():
                    raise Exception("bad_request")
                self._dispatch[orders[0]][orders[1]](orders[2:])
            except Exception as err:
                print(self._messages[str(err.args[0])])

    @staticmethod
    def _get_one_hotel_data(row: list) -> Hotel:
        unique_id = row[0]
        property_name = row[1]
        hotel_star_rating = int(row[2])
        hotel_overview = row[3]
        property_amenities = row[4]
        city = row[5]
        latitude = float(row[6])
        longitude = float(row[7])
        image_url = row[8]
        num_of_standard_rooms = int(row[9])
        num_of_deluxe_rooms = int(row[10])
        num_of_luxury_rooms = int(row[11])
        num_of_premium_rooms = int(row[12])
        standard_room_price = int(row[13])
        deluxe_room_price = int(row[14])
        luxury_room_price = int(row[15])
        premium_room_price = int(row[16])
        the_hotel = Hotel(
            unique_id, property_name, hotel_star_rating, hotel_overview, property_amenities, city, latitude,
            longitude, image_url, num_of_standard_rooms, num_of_deluxe_rooms, num_of_luxury_rooms,
            num_of_premium_rooms, standard_room_price, deluxe_room_price, luxury_room_price, premium_room_price
        )
        return the_hotel

    def _read_hotels_data(self, filename: str) -> None:
        with open(filename) as hotels_file:
            csv_reader = csv.reader(hotels_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    the_hotel = self._get_one_hotel_data(row)
                    self._ut_rip.add_hotel(the_hotel)
                line_count += 1

    def run(self) -> None:
        self._read_hotels_data("Assest/Hotels.csv")
        self._get_command()


if __name__ == '__main__':
    user_interface = UserInterface()
    user_interface.run()
