import pandas
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os
timestamp = str(datetime.now())[0:19] + "Hrs"


# def pm_levels():
#     # URL you want to scrape AQI.in dashboard
#     url = "https://www.aqi.in/dashboard/india/delhi/new-delhi"

#     response = requests.get(url)

#     # Check if request was successful
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Navigating through web page to target pm level elements
#         container = soup.body.main.div.div.div
#         all_divs = container.find_all('div', recursive=False)[4]
#         target = all_divs.find_all('span', class_="font-bold")

#         pm10 = target[2].text
#         pm2_5 = target[4].text

#     return pm2_5, pm10


# To add any new city then add its details in this dictionary
location =  {"new-delhi": "delhi", 
             "mumbai": "maharashtra", 
             "greater-noida" : "uttar-pradesh", 
             "kolkata" : "west-bengal", 
             "hyderabad" : "telangana", 
             "pune": "maharashtra"}

index = ["aqi", "pm2_5", "pm10", "temp", "humidity", "wind_speed", "wind_direction"]

# Required info from web will be complied in 'data' dictionary
data = {}


# Main function to search web page and store data    
def get_raw_data(state, city):
    # URL you want to scrape AQI.in dashboard
    url = f"https://www.aqi.in/weather/india/{state}/{city}"

    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Navigating through web page to target pm level elements
        container1 = soup.find_all('a', href=f"https://www.aqi.in/dashboard/india/{state}/{city}")[1].div
        all_divs1 = container1.find_all('div', recursive=False)[1]
        target1 = all_divs1.find_all('span', class_="font-bold")
            
        
        aqi = target1[0].text
        pm2_5 = target1[1].text
        pm10 = target1[2].text
            

        # Navigating through web page to target temperature and humidity
        container2 = soup.find('section', id = "hash-current").div
        all_divs2 = container2.find_all('div', recursive = False)[1].div
        divs2 = all_divs2.find('div', recursive = False)
        target2 = divs2.find_all('span', recursive = True)
            
        temp = target2[0].text
        humidity = target2[6].text[-3:-1]


        # Navigating for wind speed and direction
        container3 = soup.find('section', id = "hash-current").find_next_sibling('section')
        all_divs3 = container3.find_all('div', recursive = False)[1].div
        target3 = all_divs3.find_all('span', recursive = True)

        wind_speed = target3[1].text
        wind_direction = target3[8].text

        # print(f"{city}: {aqi}, {pm2_5}, {pm10}, {temp}, {humidity}, {wind_speed}, {wind_direction}")
        data[city] = [aqi, pm2_5, pm10, temp, humidity, wind_speed, wind_direction]
        print(data)

        
        # Checking Wether csv file already exists or not
        # --If file exists:
        if os.path.isfile(f"levels_{city}.csv") == True:
            # levels = pandas.read_csv(f"levels_{city}.csv", index_col = "Unnamed: 0")
            levels = pandas.read_csv(f"levels_{city}.csv" , index_col = "Unnamed: 0")
            levels.loc[str(timestamp), :] = [aqi, pm2_5, pm10, temp, humidity, wind_speed, wind_direction]
            # levels.to_csv(f"levels_{city}.csv")
            levels.to_csv(f"levels_{city}.csv")
            # print(f"{city}: \n {levels}")
            # pass
             

        # --If file doesn't exist
        elif os.path.isfile(f"levels_{city}.csv") == False:
            # data[city] = [1, 2, 3, 4, 5, 6, 7]
            levels = pandas.DataFrame(data[city], index = index, columns = [timestamp]).T
            # levels.to_csv(f"levels_{city}.csv")
            levels.to_csv(f"levels_{city}.csv")
            # print(f"{city}: \n {levels}")
            # pass

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)


# Creating infinite loop to call function periodically (every hour)
if __name__ == "__main__":
    # while True:
    #     if int(datetime.now().strftime("%S")) == 58:
            # Calling function to fetch data for given locations/cities
            for key, value in location.items():
                get_raw_data(value, key)
                # pass


# get_raw_data("delhi", "new-delhi")

levels_now = pandas.DataFrame(data, index = index)
# print(levels_now)





