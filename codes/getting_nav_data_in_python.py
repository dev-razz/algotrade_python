#installing the required Packages 
pip install datetime
pip install mftool 

import pandas as pd
from mftool import Mftool
from datetime import datetime, timedelta # importing datetime and timedelta form datetime

mf = Mftool()

# Getting the scheme codes of mutual funds
scheme_codes = mf.get_scheme_codes()
scheme_codes

# getting only the scheme codes from the dictionary.
scheme_code_list = [x for x in scheme_codes.keys()]
scheme_code_list

def HistoricalNav(scheme_code_list, start_date, end_date):
  # Assert keyword is a debugging tool.
  # Below assert keyword check whehther the scheme_code_list is a list and it is present, if not it raises an assertion failure message.
  assert (isinstance(scheme_code_list, list) is True), "Arguement scheme_code_list should be a list" 
  assert (isinstance(start_date, str) is True), "start_date must be a str in %d-%m-%Y format" # checks whether start date is present and is in correct format.
  assert (isinstance(end_date, str) is True), "end_date must be a str in %d-%m-%Y format" # checks whether end date is present and is in correct format

  main_df = pd.DataFrame() #empty dataframe

  for schemes in scheme_code_list:
    data = mf.get_scheme_historical_nav_for_dates(schemes, start_date, end_date) # requesting NAV data from the api.

    df = pd.DataFrame(data['data']) 
    df['scheme_code'] = pd.Series([data['scheme_code'] for x in range(len(df.index))]) #adding Pandas Series(scheme_code) as a column in Pandas Dataframe.
    df['scheme_name'] = pd.Series([data['scheme_name'] for x in range(len(df.index))]) #adding Pandas Series(scheme_name) as a column in Pandas Dataframe.

    df = df.sort_values(by = 'date') # sorting the values of every Scheme code based on Date

    main_df = main_df.append(df) # appending the data in the main_df dataframe.

  main_df = main_df[['scheme_code', 'scheme_name', 'date', 'nav']] #creating names of dataframe columns 
  main_df.reset_index(drop = True, inplace = True) 

  return main_df # Returning the required Dataframe.

# Function to return NAV data 
def NAV_Data(start,end): 
  try:
    values_df = HistoricalNav(scheme_code_list = scheme_code_list[0:5], start_date= start, end_date= end) #to get the data
    return values_df
  except KeyError:
    #if the data is not available on that date, going on previous date to get latest data 
    start=datetime.strptime(start, '%d-%m-%Y') - timedelta(1) # gets to previous day where the data is available.
    return NAV_Data(start.strftime("%d-%m-%Y"),end) #returns the required data. 

# Calling the function and saving the output in a variable.
# To get the latest NAV set the start_date and end_date as the last traded date in 'dd/mm/yyyy' format.
# Note:- To get data of a particular date, enter same start_date and end_date. 

start_date= "07-05-2021" # enter the date in "dd-mm-yyyy" format
end_date = "15-05-2021" # enter the date in "dd-mm-yyyy" format
values_df = NAV_Data(start_date,end_date) #calling function NAV_Data
values_df

# to get the information about a particular scheme code.
values_df[values_df['scheme_code'] == 119552]

values_df # full dataframe

