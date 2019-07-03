from load_data import LoadData
from googleapi import GoogleApi
import time
start = time.time()

##-- If using different spread sheets modify this file
##-- To overcome too many api requests the program waits about 2 seconds after each call
##-- Results in slow performance of about 15 minutes
##-- Possible optimization to only write to sheets that have new info to be added
##-- Currently re writes to all sheets and re sizes all sheets regardless if new info 
##-- was added or not
##-- When making api calls, receive an error from google saying google did not verify appp
##-- Is currrently running on something called quickstart or safemode from google to make their api calls


## -- Dictionary for all models and explores
model_list = ["apps","data_science", "dfp", "e_editions", "dfp", 
"gigya", "newspapers", "omniture", "web_analytics_dashboards"]

## -- Google has yet to verify the application
summary = '={'

    summary_data = {
        'values': [
            [ ]
        ]
    }

#ID of Spreadsheets
spreadsheetId = 'YOURSPREADSHEETID'

googleapi = GoogleApi(spreadsheetId)

for model in model_list:

    print("Writing from {0} model\n".format(model))
    load = LoadData(model)
    explores = load.get_explores()

    for index in range(len(explores)): 

        if explores[index]["hidden"] == False:

            explore = explores[index]["name"]

            explore_label = load.set_explore(explore)

            data = load.load_data() 

            if googleapi.contains_sheet(explore_label) == None : googleapi.create_sheet(explore_label)

            googleapi.write(data, explore_label, "RAW") 

            summary += "filter(\'{0}\'!A1:F, len(\'{0}\'!A1:A));".format(explore_label)

#--Writes a function to a summary sheet to query all data 
#-- To be uploaded to googlesBigQuery
summary = list(summary)
summary[len(summary) - 1] = '}'
summary = "".join(summary)

summary_data['values'][0].append(summary)

googleapi.write(summary_data, "Summary", "USER_ENTERED")


print("Finished Writing\n")
print("Beginning Resizing...")
time.sleep(3)

googleapi.auto_resize()

print("Done Resizing")
print("Program Done")
end = time.time()
print("\nProgram ran in: " + str((end - start) / 60))











