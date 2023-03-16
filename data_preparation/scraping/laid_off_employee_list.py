#!/usr/bin/env python

import requests
import json
import pandas as pd
import os


def execute_script(saveToFile=True):
    url = "https://airtable.com/v0.3/view/viw0n8xMThNj0LhZb/readSharedViewData?stringifiedObjectParams=%7B%22shouldUseNestedResponseFormat%22%3Atrue%7D&requestId=reqhwaFf1jjxutaD2&accessPolicy=%7B%22allowedActions%22%3A%5B%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viw0n8xMThNj0LhZb%22%2C%22action%22%3A%22readSharedViewData%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viw0n8xMThNj0LhZb%22%2C%22action%22%3A%22getMetadataForPrinting%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viw0n8xMThNj0LhZb%22%2C%22action%22%3A%22readSignedAttachmentUrls%22%7D%2C%7B%22modelClassName%22%3A%22row%22%2C%22modelIdSelector%22%3A%22rows%20*%5BdisplayedInView%3Dviw0n8xMThNj0LhZb%5D%22%2C%22action%22%3A%22createBoxDocumentSession%22%7D%2C%7B%22modelClassName%22%3A%22row%22%2C%22modelIdSelector%22%3A%22rows%20*%5BdisplayedInView%3Dviw0n8xMThNj0LhZb%5D%22%2C%22action%22%3A%22createDocumentPreviewSession%22%7D%5D%2C%22shareId%22%3A%22shrMt3xmtTO0p4MGT%22%2C%22applicationId%22%3A%22app1PaujS9zxVGUZ4%22%2C%22generationNumber%22%3A0%2C%22expires%22%3A%222023-03-16T00%3A00%3A00.000Z%22%2C%22signature%22%3A%22beff54aa5124f1c2e4f7a6e7fe9a8426db3a178010a1c4ba544c95faf014b505%22%7D"
    headers = {
        'x-airtable-application-id': 'app1PaujS9zxVGUZ4',
        'x-airtable-inter-service-client': 'webClient',
        'x-airtable-page-load-id': 'pglq2rV3R1pLI5zyz',
        'x-early-prefetch': 'true',
        'x-requested-with': 'XMLHttpRequest',
        'x-time-zone': 'America/Vancouver',
        'x-user-locale': 'en',
        'Content-Type': 'application/json'
    }

    out_dir = f"{os.path.realpath(os.path.dirname(__file__))}"

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    if (saveToFile):
        file = open(f"{out_dir}/laid-off-employee-response.json",'w', encoding="utf-8")
        file.write(response.text)
        file.close()

    # read the saved file if necessary
    # file = open('laid-off-employee-list.json','r', encoding="utf-8")
    # data = json.loads(file.read())

    # order of the columns name: List Name, Date, # People, Link, Locations, Date Added
    columns = [column['name'] for column in data['data']['table']['columns']]

    # hardcode index 4 to extract the information for the locations
    locations = data['data']['table']['columns'][4]['typeOptions']['choices']


    rows = []
    for row in data['data']['table']['rows']:
        entry = []
        # List Name
        entry.append(row['cellValuesByColumnId']['fldZQ3ZXm5eOWKG3H'])
        # Date
        entry.append(row['cellValuesByColumnId']['fldOkKqwOGoOU8Zht'])
        # Num of People
        entry.append(row['cellValuesByColumnId']['fldtzjucInR1oOIVw'])
        # Link
        entry.append(row['cellValuesByColumnId']['fldsqsoYUbcxeXkiV'])
        # Locations
        # print(row['cellValuesByColumnId']['fld2D71rjOAW8NZuF'])
        if 'fld2D71rjOAW8NZuF' in row['cellValuesByColumnId']:
            entry_location = []
            for location in row['cellValuesByColumnId']['fld2D71rjOAW8NZuF']:
                print('location: '+ location)
                entry_location.append(locations[location]['name'])
            entry.append(entry_location)
        else:
            entry.append([])

        # Date Added
        entry.append(row['cellValuesByColumnId']['fld08pXiuOELNU7lR'])

        rows.append(entry)

    df = pd.DataFrame(rows, columns=columns)
    if (saveToFile):
        df.to_csv(f"{out_dir}/laid-off-employee-list.csv", index=False)
    return df.to_records().tolist()


if __name__ == "__main__":
    execute_script()
