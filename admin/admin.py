import requests
import json
import sys

api_url = "http://server:5000"

endpoints = dict()
endpoints['adaugare_zbor'] = "/flights/"
endpoints['anulare_zbor'] = "/flights/" 

welcome = True

if __name__ == "__main__":
    while True:
        if (welcome):
            print("Welcome to AirplaneService, admin app!")
            welcome = False
        print("Insert a command (adaugare_Zbor, anulare_Zbor)!")
        print("Type \"quit\" to exit app")

        command = sys.stdin.readline().strip().lower()

        if command == "adaugare_zbor":
            print("Enter flight source (String):")
            source = sys.stdin.readline().strip()
            
            print("Enter flight destination (String):")
            dest = sys.stdin.readline().strip()
            
            while True:
                print("Enter flight departure day (Int 1-365):")
                departureDay = int(sys.stdin.readline().strip())
                if (1 <= departureDay and departureDay <= 365):
                    break
            
            while True:
                print("Enter flight departure hour (Int 0-23):")
                departureHour = int(sys.stdin.readline().strip())
                if (0 <= departureHour and departureHour <= 23):
                    break
            
            print("Enter flight duration (Int):")
            duration = int(sys.stdin.readline().strip())
            
            print("Enter flight number of seats (Int):")
            numberOfSeats = int(sys.stdin.readline().strip())
                
            print("Enter flight ID (String):")
            flightID = sys.stdin.readline().strip()

            URL = api_url + endpoints[command]
            data = {
                'source': source,
                'dest': dest,
                'departureDay': departureDay,
                'departureHour': departureHour,
                'duration': duration,
                'numberOfSeats': numberOfSeats,
                'flightID': flightID
            }

            r = requests.post(url = URL, json = data)
        
        elif command == "anulare_zbor":
            print("Enter flightID (String):")
            flightID = sys.stdin.readline().strip()

            URL = api_url + endpoints[command] + flightID
            r = requests.delete(url = URL)
            print(r)
        
        elif command == "quit":
            break

        else:
            print("Incorrect command!")





