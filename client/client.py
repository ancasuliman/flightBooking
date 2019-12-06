from urllib.parse import urlencode
from collections import OrderedDict
import requests
import json
import sys

api_url = "http://server:5000"

endpoints = dict()
endpoints["getOptimalRoute"] = "/optimalRoute?"
endpoints["bookTicket"]      = "/reservations/"
endpoints["buyTicket"]       = "/tickets/"

welcome = True

if __name__ == "__main__":
    while True:
        if (welcome):
            print("Welcome to AirplaneService!")
            welcome = False
        print("Insert a command (getOptimalRoute, bookTicket, buyTicket)!")
        print("Type \"quit\" to exit app")

        command = sys.stdin.readline().strip()

        if command == "getOptimalRoute":
            print("Enter flight source (String):")
            source = sys.stdin.readline().strip()
            
            print("Enter flight destination (String):")
            dest = sys.stdin.readline().strip()

            print("Enter max flights (Int):")
            maxFlights = int(sys.stdin.readline().strip())

            while True:
                print("Enter flight departure day (Int 1-365):")
                departureDay = int(sys.stdin.readline().strip())
                if (1 <= departureDay and departureDay <= 365):
                    break
            
            query_string = urlencode(OrderedDict(source=source, destination=dest, maxFlights=maxFlights, departureDay=departureDay))
            URL = api_url + endpoints[command] + query_string
            r = requests.get(url = URL)

            print(r.content)

        elif command == "bookTicket":
            print("Enter number of flights of your route (Int):")
            numberOfFlights = int(sys.stdin.readline().strip())

            data = {'flightIDs': []}

            while numberOfFlights > 0:
                print("Enter flightID (String):")
                flightID = sys.stdin.readline().strip()
                data['flightIDs'].append(flightID)

                numberOfFlights -= 1
            
            URL = api_url + endpoints[command]
            r = requests.post(url = URL, json = data)
            
            print(r.content)
            
        elif command == "buyTicket":
            print("Enter ID of reservation (String):")
            reservationID = sys.stdin.readline().strip()

            print("Enter card details (String):")
            cardDetails = sys.stdin.readline().strip()

            data = {'reservationID': reservationID, 'cardDetails': cardDetails}

            URL = api_url + endpoints[command]
            r = requests.post(url = URL, json = data)

            print(r.content)
            
        elif command == "quit":
            break
        else:
            print("Incorrect command!")


