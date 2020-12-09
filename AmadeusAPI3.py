from amadeus import Client, ResponseError
import json


"""
Получение списка рейсов и стоимости билетов по выбраному направлению.
origin = пункт отправления
destination = пункт назначения
departure_date = дата рейса
count_adults = количество пассажиров

API Endpoint
https://test.api.amadeus.com/v2/shopping/flight-offers
API Portal / Home Page
https://developers.amadeus.com/self-service/category/air/api-doc/flight-offers-search

"""


class FlightBook:

    def __init__(self, client_id, client_secret):
        self.amadeus = Client(
        client_id=client_id,
        client_secret=client_secret
        )

    def get_flight(self,origin,destination,departure_date,count_adults):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.count_adults = count_adults
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=self.origin,
                destinationLocationCode=self.destination,
                departureDate=self.departure_date,
                adults=self.count_adults)
            if response.status_code == 200:
                return response.result
        except ResponseError as error:
            print(error)
            return None

    def get_hotel(self,town):
        try:
            # Get list of Hotels by city code
            hotels_by_city = self.amadeus.shopping.hotel_offers.get(cityCode=town)
        except ResponseError as error:
            raise error
        if hotels_by_city.status_code == 200:
            return hotels_by_city.data


##################################################################################



client_id='E83hHlSYX4J9iK5ODOBEsXIWVGd92NFs'
client_secret='65FilKd9pTA5o04g'
origin = 'DME'
destination = 'OVB'
departure_date = '2021-03-01'
count_adults = 1

flight1 = FlightBook(client_id, client_secret)
res = flight1.get_flight(origin,destination,departure_date,count_adults)
hotel = flight1.get_hotel(destination)

if res is not None:
    for i in range(len(res['data'])):
        print(f"Рейс {i}:  {res['data'][i]['itineraries'][0]['segments'][0]['carrierCode']} "
              f"{res['data'][i]['itineraries'][0]['segments'][0]['number']}, "
              f"Количество сегментов-{len(res['data'][i]['itineraries'][0]['segments'])}, "
              f"Цена: {res['data'][i]['price']['grandTotal']}  {res['data'][i]['price']['currency']}")
else:
    print('Обломайся.')
#
# write to file
#
filename = 'amadeus1.json'
with open(filename, "w") as f:
    json.dump(res, f)

print(hotel)

############################################################################################
