from lookerapi import LookerApi
import json
import yaml

host = 'localhost'

#-- Data to not be inlcuded 
#-- Should be put in json file for easy access and modification
#-- Is case sensitive
type_filter = [
"data_day_of_month", "date_day_of_week", "date_day_of_week_index", "date_hour", "date_hour_of_day",
"date_month", "date_month_name", "date_month_num", "date_quarter", "date_raw", "date_time", "date_week",
"date_week_of_year", "date_year", "date_day_of_month", "date_day_of_year"
]

label_filter = [
"Visited Raw", "Visited Month", "Visited Year", "Visited Week", "Visited Quarter", "Quarter",
"Month", "Period Start Quarter", "Day of week short", "Day of week", "Period End Raw", "Period End Week",
"Cal Time", "Month short", "Period Start Raw", "F Cal Date", "Day of year", "Period Start Year", "Period End Time",
"Quarter number", "Cal Raw", "Period End Quarter", "Cal Quarter", "Period Start Month", "Year number", "Period End Year",
"Cal Week", "Day of week in month", "Day of week number", "Week of year", "Period End Month", "Day of Month", "Week of month",
"Month number", "Period Days", "Period Start Week", "Period Start Time"
]


class LoadData(object):

    def __init__(self, model_name):

        self.dimensions = " "
        self.measures = " "

        self.explore_label = " "
        self.explore_name = " "

        self.looker = ""
        self.model_body = ""

        self.model_name = model_name

        self.setup()

##-- Sets up the looker api
    def setup(self):

        f = open('config.yml')
        params = yaml.safe_load(f)
        f.close()

        my_host = params['hosts'][host]['host']
        my_secret = params['hosts'][host]['secret']
        my_token = params['hosts'][host]['token']

        self.looker = LookerApi(host=my_host,
        token=my_token,
        secret = my_secret)

        ##-- Gests a list of explores
        def get_explores(self):
        self.model_body = self.looker.get_model(self.model_name)
        return self.model_body['explores'] 

##-- Gets fields of a single explore and returns the label
    def set_explore(self, explore):

        self.explore_name = explore
        self.dimensions = self.looker.get_fields(self.model_name, self.explore_name, "dimensions")
        self.measures = self.looker.get_fields(self.model_name, self.explore_name, "measures") 

        for index in range(len(self.model_body['explores'])):
        data = self.model_body["explores"][index]
        if data["name"] == self.explore_name:
        self.explore_label = data["label"]
        return data["label"]

#Loads data into body to be sent to googleSheets

    def load_data(self):

        body = {
        'values' : [
                [
                    'Explore', 'Label', 'Description', 'Group Label', 'Type', 'SQL', 'Field'
                ]
            ]
        }

        ##-- Adds the dimension fields
        for index in range(len(self.dimensions)):

            if self.dimensions[index]["hidden"] == False:

            if (self.dimensions[index]["label_short"] not in label_filter and 
            self.dimensions[index]["type"] not in type_filter):

            append = [
            self.explore_label, 
            self.dimensions[index]["label_short"], 
            self.dimensions[index]["description"],
            self.dimensions[index]["field_group_label"],
            self.dimensions[index]["type"],
            self.dimensions[index]["sql"],
            "dimension"
            ]

        body['values'].extend([append])

        ##-- Adds the measure fields
        for index in range(len(self.measures)):

            if self.measures[index]["hidden"] == False:

            if self.measures[index]["type"] not in type_filter:

            append = [
            self.explore_label, 
            self.measures[index]["label_short"], 
            self.measures[index]["description"],
            self.measures[index]["field_group_label"],
            self.measures[index]["type"],
            self.measures[index]["sql"],
            "measure"
            ]

            body['values'].extend([append]) 


        return body


