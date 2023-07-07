"""updates/gets the request headers and body(s).

This module navigates the website to be scraped and
catches the post requests to get the request headers,
body(s) needed for crawling the website.

This script requires that `playwright` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following

classes:
    change_headers_ (change_headers)
        updates/gets the request headers and body(s).
        this class inherit form the abstract class
        change_headers found in 
        scrapers_m.abstract_classes module. 
"""

from playwright.sync_api import Playwright, sync_playwright, expect
from time import sleep
from scrapers_m.abstract_classes import change_headers

class change_headers_ (change_headers):
    """updates/gets the request headers and body(s).
    
    this class inherit form the abstract class
    change_headers found in 
    scrapers_m.abstract_classes module.
        
    contains methods responsible for extracting the headers and requests body(s)
    need for the scraping process.

    Args:
        change_headers (change_headers): abstract class used for inheritance.

    Attributes:
        search_page_api_headers (dict): stories the headers used to request the search page api.
        result_api_headers (dict): stories the headers used to request the each result api.
        WEBSITE (str): the url of the website being scraped.
        search_page_api (str): part of the url for the search page post request 
            (used to catch the request and extract it' headers, data, and url).
        result_api_headers (str): part of the url for the an individual result page post request 
            (used to catch the request and extract it' headers, data, and url).
        requests_data_dict (dict): stores the bodies for the requests needed for the scraping
            process.
    
    Methods:
        get_headers() -> tuple[str, dict, dict, dict]
            extracts the needed headers, requests body(s) and urls.
    """

    search_page_api_headers = {}
    result_api_headers = {}
    
    def __init__(self, WEBSITE:str) -> None:    
        self.WEBSITE = WEBSITE
        
        self.search_page_api = "rdc_search_srp?client_id=rdc-search-rentals-search&schema=vesta"
        self.result_api = "hestia?client_id=rdc-x-rentals"
        
        self.requests_data_dict = {
        "pages": "",
        "flood":"{\"query\":\"\\nquery GetLocalData($propertyId: ID!) {\\n  home(property_id: $propertyId) {\\n    local {\\n      flood {\\n        flood_factor_score\\n        flood_factor_severity\\n        flood_trend\\n      }\\n    }\\n  }\\n}\",\"variables\":{\"propertyId\":\"00000000\"},\"callfrom\":\"LDP\",\"nrQueryType\":\"FLOOD_RISK\"}",
        "fire": "{\"query\":\"\\nquery GetLocalData($propertyId: ID!) {\\n  home(property_id: $propertyId) {\\n    local {\\n      wildfire {\\n        fire_factor_score\\n        fire_factor_severity\\n        fire_trend\\n      }\\n    }\\n  }\\n}\",\"variables\":{\"propertyId\":\"00000000\"},\"callfrom\":\"LDP\",\"nrQueryType\":\"WILDFIRE_RISK\"}",
        "schools": "{\"query\":\"\\nquery TransformShow($property_id: ID,  $listing_id: ID, $listing_type: String) {\\n  home(property_id: $property_id, listing_id: $listing_id, listing_type: $listing_type) {\\n    nearby_schools {\\n      schools {\\n        coordinate {\\n          lat\\n          lon\\n        }\\n        distance_in_miles\\n        district {\\n          id\\n          name\\n        }\\n        education_levels\\n        funding_type\\n        greatschools_id\\n        id\\n        name\\n        nces_code\\n        parent_rating\\n        rating\\n        slug: slug_id\\n        student_count\\n        review_count\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{\"property_id\":\"0000000000\",\"listing_type\":\"rental\",\"tag_version\":\"v1\",\"caller\":\"desktop\",\"debug\":false},\"callfrom\":\"LDP_RENTALS\",\"nrQueryType\":\"MAIN_LDP_RENTALS\",\"user_id\":null,\"cacheKey\":\"LDP-SEARCH\"}"
        }
        
        
    def __clean_dict(self,dict:dict) -> None:
        del dict["host"]
        del dict["accept-encoding"]
        del dict["content-length"]
        del dict["origin"]
        del dict["connection"]
        del dict["cookie"]
        
    def __route_intercept(self,route):
        
        if self.search_page_api in route.request.url:
            self.search_page_api_headers = route.request.all_headers()
            self.search_page_api_headers["url"] = route.request.url
            self.__clean_dict(self.search_page_api_headers)
            pages_request_body = route.request.post_data
            self.requests_data_dict["pages"] = pages_request_body
            
        if self.result_api in route.request.url:
            self.result_api_headers = route.request.all_headers()
            self.result_api_headers["url"] = route.request.url
            self.__clean_dict(self.result_api_headers)
            
        if "google" in route.request.url:
            return route.abort()

        return route.continue_()

    def get_headers(self) -> tuple[str, dict, dict, dict]:
        """extracts the needed headers, requests body(s) and urls.
        
        navigates through the given website and catches the needed requests 
        made by the browser and extract there headers, body and url and
        assign it to it's class attributes then it returns these attributes.
        
        Returns:
            page_content (str): the first search page source code.
            self.search_page_api_headers (dict): the search page post request headers.
            self.result_api_headers (dict): a result page request headers.
            self.requests_data_dict (dict): contains the body for each request needed
                in the scraping process.
        """    
        with sync_playwright() as p:
            while len(self.result_api_headers) == 0:
                try:
                    browser = p.firefox.launch()
                    context = browser.new_context(viewport={"width": 1920, "height": 1080})
                    page = context.new_page()
                    
                    page.route("**/*", self.__route_intercept)
                    page.goto(self.WEBSITE , timeout=0)
                
                    page.wait_for_selector("text=Property Type").click()
                    sleep(3)
                    page.click("text=Single Family Home")
                    sleep(3)
                    try:
                        page.click("text=Done")
                    except:
                        pass
                    
                    page.wait_for_selector('button[aria-label*="Reset Single"]')
                    sleep(2)
                    # filtered page ------------------------------------------------------------------------------
                    page.locator("body").press("End")
                    page_content = page.content()
                    next_page = page.wait_for_selector('[aria-label="pagination"] a:nth-last-of-type(1)')
                    next_page.scroll_into_view_if_needed()
                    next_page.click()
                    page.wait_for_selector('div[aria-label="pagination"]>a:nth-of-type(3)[aria-current="true"]')
                    # second page ------------------------------------------------------------------------------
                    result_css = 'section[class*="PropertiesList_propertiesContaine"]>div[id*="placeholder_property_"]:nth-of-type(1) a[class="card-anchor"]'
                    result = page.wait_for_selector(result_css)
                    result_url = "https://www.realtor.com"+result.get_attribute("href")
                    page.goto(result_url , timeout=0)

                    sleep(2)  
                    # result page ------------------------------------------------------------------------------
                    page.locator("body").press("End")
                    sleep(1)
                    page.locator("body").press("Home")
                    try:
                        school = page.wait_for_selector('div[class*="school"]')
                        school.scroll_into_view_if_needed()
                        school.click()
                    except:   
                        environmental_risk = page.wait_for_selector('div[data-testid="environmentalRiskAccordion"]')
                        environmental_risk.scroll_into_view_if_needed()
                        environmental_risk.click()
                        
                    while self.result_api_headers == None:
                        sleep(2)
                    browser.close()
                    break
                
                except:
                    browser.close()
                    sleep(60)
        return page_content, self.search_page_api_headers, self.result_api_headers, self.requests_data_dict
