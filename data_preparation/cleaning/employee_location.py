#10k requests per day
import requests
import time
locationiq_token = "pk.193f7f0a30342b4a64f39837324ef939"
import pandas as pd
from random import randint
import spacy
AWS_S3_BUCKET = "layoffs-decoded-master"
AWS_ACCESS_KEY_ID = "AKIAUHN3JA72IHF7WP6J"
AWS_SECRET_ACCESS_KEY = "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"


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
    time.sleep(2)

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


folder_path = "training_data_q3"
csv = "employee_merged_validated_csv.csv"


# loading training data from AWS S3
df = pd.read_csv(
    f"s3://{AWS_S3_BUCKET}/{folder_path}/{csv}",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    }, 
)

df["country"] = df["location"]

df["country"] = df["country"].fillna("")
df["country"] = df["country"].apply(lambda x: x.lower())
df["country"] = df["country"].apply(lambda x: x if x in ["remote","hybrid", "anywhere"] else string_cleaning(x))
unique_values = df["country"].drop_duplicates()
country_dict = {}
count = 0
for value in unique_values:
    count += 1
    print(count,"/",len(unique_values))
    country_dict[value] = get_country_from_address(value)
    
df["country"] = df["country"].apply(lambda x: country_dict[x] if x in country_dict else x)


#write to s3
folder_path = "training_data_q3"  #you can create your own folder in S3 for each question and put all the tables csv in #that
csv = "employee_location_locationiq2.csv" #give the name of csv that would want in S3

# writing dataframes covid training data to AWS S3
df.to_csv(
    f"s3://{AWS_S3_BUCKET}/{folder_path}/{csv}",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY,
    },
)