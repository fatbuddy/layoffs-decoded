import pandas as pd
import numpy as np
import re
import pandas as pd
import s3fs
 
df = pd.read_csv("C:/Users/Crystal/OneDrive/Desktop/employee_location_locationiq2.csv", usecols=['country'])

# 
# remove blank entries and strip spaces
df = df.apply(lambda x: x.str.strip())
# df = df.replace('\s\s', np.nan)
# df = df.dropna()
# count the occurrences of each unique country
country_counts = df['country'].value_counts()
country_counts = country_counts[country_counts != 176]
country_counts.to_csv("C:/Users/Crystal/OneDrive/Desktop/country_counts.csv")
# print(country_counts[:10])


AWS_S3_BUCKET = "layoffs-decoded-master"
AWS_ACCESS_KEY_ID = "ASIAUHN3JA72IXYNQVCB"
AWS_SECRET_ACCESS_KEY = "hZOZhDz7yz9T7pH3RktXgC72a6cGh5E/PmifCWE0"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEAsaCXVzLXdlc3QtMiJIMEYCIQDoCgvICsXkIMYAI+2XvS9szgW3j3Iq6dDXilNwBzTx9wIhAKdXhWaQixAruDzVLEURIzFH0Cz50HJmGPKOcD7AM9KgKvICCOT//////////wEQABoMMjkwODM5OTIyNjc2IgwMuMzl2U1Ma1PIo1UqxgK/n4lCfYPLdLt9LSfu1PlzbFLkXeH6iNCZ0SA2bEH0sj/p7Cs3z2KlTcQmT656JQmJTcTPGCe76AUR/cz37b3o4STYtCMokMOODn9dQ4+4HgnKArVEybBx9iq2BlH//OPnSMIMNMVsTVrMVLZHL6tX27+jcle2bu7i7xK1/UC3xpKTM0LzBIAQE1KbkVM+uSi8xuKL6HEJscJp64MDIVxp5UVIGUM8G+BTTC0076PxGEDpCHotMtM0ekRlNhzPvgkfsCAJyZoXLzGoWS1yJqeIx5gpUm7NdZGM2d0ZSUBNRL1KA+8Ys2UywZaZ09nMEGuSR6afWqebHSTny7kT8wI+pyesli92oGhkdiVTB15UMSNLh10kgBjE1km6cVTQbdur1gUKGdYF/oFixMttfB9Tm5WwZcjWMKiPbQdt+IZSyzWlT1mEXDCNqK6hBjqmAQdKle14mNho1BBf+ixtYhPzMyNx7XkFbJBCJMi6NB0Z06XCSq5JbOLyjvSoa9AKApkDnQq/NUkLIvcC86g2ce/T2g3okthOmEGpNl8ioz9kWHq+bzHu8PtiytRj1CQQEL/o48AGec+ZmYwGCRNvHgxM7TXUCyWsUBo8noj04DAn037SHNobPaGl1ndFnXV8Gu2+0zQ27RP5CG14TPwV+UcAnutUO8A="

folder_path = "training_data_q3"  #you can create your own folder in S3 for each question and put all the tables csv in #that
covid_csv = "country_counts.csv" #give the name of csv that would want in S3

# writing dataframes covid training data to AWS S3
country_counts.to_csv(
    f"s3://{AWS_S3_BUCKET}/{folder_path}/{covid_csv}",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY,
        "token": AWS_SESSION_TOKEN,
    },
)