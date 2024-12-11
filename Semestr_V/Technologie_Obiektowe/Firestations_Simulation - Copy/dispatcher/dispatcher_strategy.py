from .i_dispatcher_strategy import IDispatcher
import math

def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Promień Ziemi w km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# class HazardDispatchStrategy(IDispatcher):
#     def dispatch(self, event, stations):
#         # Sortowanie stacji według odległości od zdarzenia
#         sorted_stations = sorted(stations, key=lambda s: haversine_distance(event.location, s.location))

#         # Dodajemy debugowanie, żeby zobaczyć posortowaną listę stacji
#         print(f"Sorted stations by distance from event at {event.location}:")
#         for station in sorted_stations:
#             print(f"{station.name} at {station.location}, distance: {haversine_distance(event.location, station.location)} km")
        
#         vehicles_assigned = []

#         # Przypisywanie pojazdów z najbliższych stacji
#         for station in sorted_stations:
#             if station.has_free_vehicle():
#                 vehicle = station.dispatch_vehicle(event)
#                 vehicle.assign_task(event)
#                 vehicles_assigned.append(vehicle)
#                 if len(vehicles_assigned) >= 2:  # Maksymalnie 2 pojazdy do miejscowego zagrożenia
#                     break

#         # Sprawdzanie, czy udało się przydzielić wystarczającą liczbę pojazdów
#         if len(vehicles_assigned) < 2:
#             print(f"Brak wystarczających pojazdów do obsługi miejscowego zagrożenia w {event.location}")

#         return vehicles_assigned
    

# class FireDispatchStrategy(IDispatcher):
#     def dispatch(self, event, stations):
#         # Sortowanie stacji według odległości od zdarzenia
#         sorted_stations = sorted(stations, key=lambda s: haversine_distance(event.location, s.location))
        
#         # Dodajemy debugowanie, żeby zobaczyć posortowaną listę stacji
#         print(f"Sorted stations by distance from event at {event.location}:")
#         for station in sorted_stations:
#             print(f"{station.name} at {station.location}, distance: {haversine_distance(event.location, station.location)} km")
        
#         vehicles_assigned = []

#         # Przypisywanie pojazdów z najbliższych stacji
#         for station in sorted_stations:
#             if station.has_free_vehicle():
#                 vehicle = station.dispatch_vehicle(event)
#                 vehicle.assign_task(event)
#                 vehicles_assigned.append(vehicle)
#                 if len(vehicles_assigned) >= 3:  # Maksymalnie 3 pojazdy do pożaru
#                     break

#         # Sprawdzanie, czy udało się przydzielić wystarczającą liczbę pojazdów
#         if len(vehicles_assigned) < 3:
#             print(f"Brak wystarczających pojazdów do obsługi pożaru w {event.location}")

#         return vehicles_assigned

class HazardDispatchStrategy(IDispatcher):
    def dispatch(self, event, stations):
        # Sortowanie stacji według odległości od zdarzenia
        sorted_stations = sorted(stations, key=lambda s: haversine_distance(event.location, s.location))

        print(f"Sorted stations by distance from event at {event.location}:")
        for station in sorted_stations:
            print(f"{station.name} at {station.location}, distance: {haversine_distance(event.location, station.location)} km")
        
        vehicles_assigned = []
        required_vehicles = 2  # Maksymalna liczba pojazdów dla miejscowego zagrożenia

        for station in sorted_stations:
            free_vehicles = station.get_free_vehicles()
            if free_vehicles:
                # Dodaj pojazdy z tej stacji, ale nie więcej niż potrzeba
                for vehicle in free_vehicles:
                    if len(vehicles_assigned) < required_vehicles:
                        vehicle.assign_task(event)
                        vehicles_assigned.append(vehicle)

                # Jeśli mamy wystarczającą liczbę pojazdów, przerywamy
                if len(vehicles_assigned) >= required_vehicles:
                    break

        if len(vehicles_assigned) < required_vehicles:
            print(f"Brak wystarczających pojazdów do obsługi miejscowego zagrożenia w {event.location}")

        return vehicles_assigned


class FireDispatchStrategy(IDispatcher):
    def dispatch(self, event, stations):
        # Sortowanie stacji według odległości od zdarzenia
        sorted_stations = sorted(stations, key=lambda s: haversine_distance(event.location, s.location))

        print(f"Sorted stations by distance from event at {event.location}:")
        for station in sorted_stations:
            print(f"{station.name} at {station.location}, distance: {haversine_distance(event.location, station.location)} km")
        
        vehicles_assigned = []
        required_vehicles = 3  # Maksymalna liczba pojazdów dla pożaru

        for station in sorted_stations:
            free_vehicles = station.get_free_vehicles()
            if free_vehicles:
                # Dodaj pojazdy z tej stacji, ale nie więcej niż potrzeba
                for vehicle in free_vehicles:
                    if len(vehicles_assigned) < required_vehicles:
                        vehicle.assign_task(event)
                        vehicles_assigned.append(vehicle)

                # Jeśli mamy wystarczającą liczbę pojazdów, przerywamy
                if len(vehicles_assigned) >= required_vehicles:
                    break

        if len(vehicles_assigned) < required_vehicles:
            print(f"Brak wystarczających pojazdów do obsługi pożaru w {event.location}")

        return vehicles_assigned

