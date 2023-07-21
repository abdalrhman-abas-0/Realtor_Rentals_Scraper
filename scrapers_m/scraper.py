""" this module contains the scraper/parser methods

classes:
    class scrapers_(scrapers):
        contain the scrapers methods which extract the data form the json response.
"""
from scrapers_m.abstract_classes import scrapers
import json

class scrapers_(scrapers):
    """contain the scrapers methods which extract the data form the json response.

    inherits for the scrapers_m.abstract_classes.scrapers class.
    
    Methods:
        primary(self,response:json, results_list:list) -> None:
            extract the appropriate data from the response of the primary stage.
        secondary (response:json , request:str) -> dict:
            extract the appropriate data from the response of the secondary stage.
    """
    
    def primary(self,response:json, results_list:list) -> None: # one listing at a time
        """extract the appropriate data from the response of the primary stage.

        extract the data of all the results found in the response of the search result
        and append them to the passed list.
        
        Args:
            response (json): the response object of the primary request.
            results_list (list): the list where the scraped results are appended

        """
        try: 
            listings = response["props"]["pageProps"]["properties"]
        except:
            listings = response["data"]["home_search"]["properties"]

        for listing in listings:

            property_id = listing["property_id"]
            
            advertisers =listing["advertisers"]
            
            last_update = listing["list_date"]
            
            year_built = listing["description"]["year_built"]
            
            pet_policy = listing["pet_policy"]
            
            parameter = listing["description"]["sqft"]
            
            bath_rooms = listing["description"]["baths_consolidated"]
            
            bed_rooms = listing["description"]["beds"]
            
            if listing["list_price"] != None:
                price = listing["list_price"]
            elif listing["list_price_max"] != None:
                price = listing["list_price_max"]
            else:
                price = listing["list_price_min"]
                
                                
            address =listing["location"]["address"]
            del address["coordinate"], address["country"]
            
            status = listing["status"]
            listing_page = "https://www.realtor.com/realestateandhomes-detail/" + listing["permalink"]

            result ={
                "property id":property_id ,
                "listing page":listing_page,
                "status":status,
                "price":price,
                "address":address,
                "bed rooms":bed_rooms,
                "bath rooms":bath_rooms,
                "parameter":parameter,
                "pets policy": pet_policy,
                "year built": year_built,
                "last update":last_update,
                "advertisers":advertisers
            }
            for key, value in result.items():
                if value == '':
                    result[key] = "Not Listed" 
                        
            results_list.append(result)
        
        
    def secondary (self, response:json , request:str) -> dict:
        """extract the appropriate data from the response.

        extract the data from the response according to the request
        passed and return them as a dict.
        
        Args:
            response (json): the response object of the json response.
            request (str): the request name send to the server.
            
        Returns:
            dict: a dictionary fo the scraped data.

        """

        if request == "schools":
            try:
                json_response = response["data"]["home"]["nearby_schools"]["schools"]
            except:
                json_response = "not available"
                
        elif request == "fire":
            try:
                json_response = response["data"]["home"]["local"]["wildfire"]["fire_factor_score"]
            except:
                json_response = "not available"
        
        else: 
            try:
                json_response = response['data']['home']['local']['flood']['flood_factor_score']
            except:
                json_response = "not available"
          
                
        return json_response
