import requests
import json

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
# 25 = lunch

# brunch = 70
main()


# IDEAS for expansion
# get date, meal for day obs
# get allergens
# pings for when the hall closes and opens
# pings for strange hours
# pings for when they have an event
# pings for when they are serving favorited meals
# macro tracking


