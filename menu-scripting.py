import requests
import json

# APIS
# APIs are application programming interfaces. 
# we use them to store and fetch data between clients and servers, statelessly.

# ROUTING
# routing means matching URL + HTTP methods to functions.

# so when someone says /ice-cream with method POST, 
# we call a def, create_ice_cream

def main():

    # get input for date
    year = (input("Enter year: "))[2:4]
    month = input("Enter month: ")
    day = input("Enter day: ")

    dateArg = (year+"-"+month+"-"+day)
    # dateArg = "2026-02-26"

    # lunch arg
    lunchInput = (input("Enter what mealtime you would like to see: \nBreakfast, Lunch, or Dinner: ")).lower()
    lunchArg = 4

    if lunchInput == "breakfast":
        lunchArg = 10
    elif lunchInput == "lunch":
        lunchArg = 25
    elif lunchInput == "dinner":
        lunchArg = 16
    
    # let's get the response here, and the error code.
    response = getResponse(dateArg, lunchArg)
    print(response.status_code, '\n')
    
    if (response.status_code == 200):
        response = response.json()
        
        cafFoodInfo = parseJSON(response)
        dailyItems = getDailyItems(cafFoodInfo)
        stations = (getStations(cafFoodInfo))

        # let's sort the items by station
        for i in range(len(stations)):
            print("Station", i)
            for items in stations[i].get('skus'):
                if dailyItems.get(items) != None:
                    print(dailyItems.get(items))
            print()

# fetch a response, input date string.

def getResponse(dateArg, lunchArgs):

    # api URL
    url = "https://api.elevate-dxp.com/api/mesh/c087f756-cc72-4649-a36f-3a41b700c519/graphql"

    # basic query, scraped from network investigation
    query = """
    query getLocationRecipes(
    $campusUrlKey: String!, 
    $locationUrlKey: String!, 
    $date: String!, 
    $mealPeriod: Int, 
    $viewType: Commerce_MenuViewType!
    ) {
    getLocationRecipes(
        campusUrlKey: $campusUrlKey, 
        locationUrlKey: $locationUrlKey, 
        date: $date, 
        mealPeriod: $mealPeriod, 
        viewType: $viewType
    ) {
        locationRecipesMap {
        skus
        stationSkuMap {
            id
            skus
        }
        dateSkuMap {
            date
            stations {
            id
            skus {
                simple
                configurable {
                sku
                variants
                }
            }
            }
        }
        }
        products {
        items {
            id
            name
            sku
            images {
            label
            roles
            url
            }
            attributes {
            name
            value
            }
            ...on Catalog_SimpleProductView {
            price {
                final {
                amount {
                    currency
                    value
                }
                }
            }
            }
            ...on Catalog_ComplexProductView {
            options {
                title
                values {
                id
                title
                ...on Catalog_ProductViewOptionValueProduct {
                    product {
                    name
                    sku
                    attributes {
                        name
                        value
                    }
                    price {
                        final {
                        amount {
                            value
                            currency
                        }
                        }
                    }
                    }
                }
                }
            }
            }
        }
        }
    }
    }
    """

    # parameters for fetching
    variables = {
        "campusUrlKey": "campus",
        "locationUrlKey": "schulze",
        "date": dateArg,
        "mealPeriod": lunchArgs,
        "viewType": "DAILY"
    }

    headers = {
        "x-api-key": "ElevateAPIProd",
        "aem-elevate-clientpath": "ch/univlamonroe/en",
        "magento-store-code": "ch_univlamonroe",
        "magento-store-view-code": "ch_univlamonroe_en",
        "magento-website-code": "ch_univlamonroe",
        "store": "ch_univlamonroe_en",
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://univlamonroe.mydininghub.com",
        "Referer": "https://univlamonroe.mydininghub.com/"
    }
    
    # raw api response
    response = requests.get(url, headers=headers, params={"query": query, "variables": json.dumps(variables)})
    return response

# parses the JSON and returns a list of daily items.   
def parseJSON(response): 
    data = response.get('data')
    cafFoodInfo = data.get('getLocationRecipes')

    # for viewing each type in the nested JSON
    # print(type(data))
    # print(type(getLocationRecipes))
    # print(type(products))
    # print(type(items))
    return cafFoodInfo

def getStations(cafFoodInfo):
    stationsMap = cafFoodInfo.get('locationRecipesMap')
    stations = stationsMap.get('stationSkuMap')
    return stations


# gets the items of the day.
def getDailyItems(cafFoodInfo):
    products = cafFoodInfo.get('products')
    items = products.get('items')
    dailyItemsDict = dict()
    for item in items:
        dailyItemsDict.update({item.get('sku') : item.get('name')})
    return dailyItemsDict

# define meal periods. we can call the api to get this too, but for now here's a harcoded ref

# 10 = breakfast
# 4/13 = all day
# 16 = dinner
# lunch = 25
 


# breakfast = 40 (actually 10 tho)
# lunch = 90
# dinner = 16
# brunch = 70
# all day = 4

# morning snack = 28
# afternoon snack = 1
# limited dinner = 53
# evening snack = 22
# overnight = 31
main()


# IDEAS
# get date, meal for day obs
# get allergens
# pings for when the hall closes and opens
# pings for strange hours
# pings for when they have an event
# pings for when they are serving favorited meals
# macro tracking

# parse the response into a model, 
# fr example for meals, dates, and have methods that execute queries for certain information.
"""
MAPPING

cafeteria has stations
stations have ids, meals
meals have ids, ames, SKUS

"""
 


""" 

TASKS:
1. Input
Raw data: 1k+ lines of nested JSON from the dining API (menus, stations, items, attributes, hours, events).

2. Goals
Parse and understand the nested JSON
Identify key entities: Meal, Station, Item, Attribute, Hall, Hours, Event.
Map relationships (e.g., a Meal has multiple Stations, a Station has multiple Items).
Design a data model

Create Python classes or ORM models representing the entities.
Include relationships and relevant fields (allergens, macros, availability, dates).
Build backend architecture

Functions or services that call the API and populate your models.
Maintain a clean separation: API layer → Data layer → Business logic layer.
Optional persistence: save parsed data to JSON, CSV, or a database.

Implement business logic
Filters: by allergens, macros, meal period, favorites.
Aggregations: daily menus, totals for macros.
Event-based logic: notifications when meals are available or halls are closing.
Anything derived: favorites tracking, meal suggestions, or alerts.

3. Deliverable
A backend system that can:
Accept parameters (date, meal period, hall)
Query the API or cached data
Produce structured, usable objects (Meal → Station → Item → Attributes)
Perform operations and queries on that data efficiently

"""