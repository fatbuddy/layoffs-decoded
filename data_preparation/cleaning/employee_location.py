#10k requests per day
import requests
import time
locationiq_token = "pk.193f7f0a30342b4a64f39837324ef939"
import pandas as pd
from random import randint
import spacy

def call_api(country):
    raw_country = country
    url = f"https://us1.locationiq.com/v1/search.php?key={locationiq_token}&q={country}&format=json"
    response = requests.get(url)
    data = response.json()
    # Extract country name from response
    if len(data) > 0:
        country = data[0]['display_name'].split(',')[-1]
        if country:
            return country
        else:
            return raw_country
    else:
        return raw_country

        
def get_country_from_address(address):
    raw_address = address
    time.sleep(3)

    try:
        # Make API call and get response
        country = call_api(address)
        return country
    except:
        try:
            address = remove_stop_words(address)
            country = call_api(address)
            return country
        except:
            return raw_address
    # print(country)
    # print()
    # print()

def remove_stop_words(raw_loc):
    en = spacy.load('en_core_web_sm')
    stopwords = en.Defaults.stop_words
    lst=[]
    for token in raw_loc.split():
        if token.lower() not in stopwords:    
            lst.append(token) 
            
    return ' '.join(lst)
    
def string_cleaning(raw_loc):
    try:
        if raw_loc == 'nan':
            raw_loc = ""
        raw_loc = raw_loc.replace("remote","").replace("hybrid","").replace("anywhere","")
        raw_loc = raw_loc.replace(".","").replace("/"," ")
        return raw_loc
    except:
        return raw_loc
    
def post_locationiq(country):
    try:
        country = country.replace("us","USA")
        country = country.replace("san francisco bay area","USA")
        return country
    except:
        return country

file_path = 'C:/Users/Crystal/OneDrive/Desktop/employee_merged_validated_csv.csv'

df = pd.read_csv(file_path)
df["country"] = df["location"]


# df.head()
# df_sample = df.sample(n=10)
# df_sample["country"] = df_sample["country"].fillna("")
# df_sample["country"] = df_sample["country"].apply(lambda x: x.lower())
# df_sample["country"] = df_sample["country"].apply(lambda x: x if x in ["remote","hybrid", "anywhere"] else string_cleaning(x))
# df_sample["country"] = df_sample["country"].apply(lambda x: x if x in ["remote","hybrid", "anywhere"] else get_country_from_address(x))
# df_sample.to_csv('C:/Users/Crystal/OneDrive/Desktop/employee_location_locationiq1.csv')


# raw_loc = "nz/"
# raw_loc = "berlin, germany"
# raw_loc = "Cologne, Germany. France is as well an option."
# raw_loc = "pittsburgh"
# raw_loc = "Anywhere"
# raw_loc = "Remote/Seattle"
# raw_loc = "U.S or India"
# raw_loc = "Canada position or US position that accepts remote from Canada"
# raw_loc = "Tempe, Arizona Available locations USA"
# raw_loc = "Remote, Geelong/Melbourne"
# raw_loc = "USA/ San Francisco"
raw_loc = "San Francisco (Bay Area)/ Remote" #4585
raw_loc = raw_loc.lower()
raw_loc = raw_loc if raw_loc in ["remote", "hybrid", "anywhere"] else string_cleaning(raw_loc)
raw_loc = raw_loc if raw_loc in ["remote", "hybrid", "anywhere"] else get_country_from_address(raw_loc)
print(raw_loc)

# df["country"] = df["country"].fillna("")
# df["country"] = df["country"].apply(lambda x: x.lower())
# df["country"] = df["country"].apply(lambda x: x if x in ["remote","hybrid", "anywhere"] else string_cleaning(x))
# df["country"] = df["country"].apply(lambda x: x if x in ["remote","hybrid", "anywhere"] else get_country_from_address(x))
# df.to_csv('C:/Users/Crystal/OneDrive/Desktop/employee_location_locationiq1.csv')
# display(df_sample)