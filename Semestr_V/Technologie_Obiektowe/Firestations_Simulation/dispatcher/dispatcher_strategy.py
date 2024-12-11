from .i_dispatcher_strategy import IDispatcher
import math

def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class HazardDispatchStrategy(IDispatcher):
    def dispatch(self, event, stations):
        sorted_stations = sorted(stations, key=lambda s: haversine_distance(event.location, s.location))

        print(f"Sorted stations by distance from event at {event.location}:")
        for station in sorted_stations:
            print(f"{station.name} at {station.location}, distance: {haversine_distance(event.location, station.location)} km")
        
        vehicles_assigned = []
        required_vehicles = 2

        for station in sorted_stations:
            free_vehicles = station.get_free_vehicles()
            if free_vehicles:
                for vehicle in free_vehicles:
                    if len(vehicles_assigned) < required_vehicles:
                        vehicle.assign_task(event)
                        vehicles_assigned.append(vehicle)

                if len(vehicles_assigned) >= required_vehicles:
                    break

        if len(vehicles_assigned) < required_vehicles:
            print(f"Brak wystarczających pojazdów do obsługi miejscowego zagrożenia w {event.location}")

        return vehicles_assigned


class FireDispatchStrategy(IDispatcher):
    def dispatch(self, event, stations):
        sorted_stations = sorted(stations, key=lambda s: haversine_distance(event.location, s.location))

        print(f"Sorted stations by distance from event at {event.location}:")
        for station in sorted_stations:
            print(f"{station.name} at {station.location}, distance: {haversine_distance(event.location, station.location)} km")
        
        vehicles_assigned = []
        required_vehicles = 3

        for station in sorted_stations:
            free_vehicles = station.get_free_vehicles()
            if free_vehicles:
                for vehicle in free_vehicles:
                    if len(vehicles_assigned) < required_vehicles:
                        vehicle.assign_task(event)
                        vehicles_assigned.append(vehicle)

                if len(vehicles_assigned) >= required_vehicles:
                    break

        if len(vehicles_assigned) < required_vehicles:
            print(f"Brak wystarczających pojazdów do obsługi pożaru w {event.location}")

        return vehicles_assigned

