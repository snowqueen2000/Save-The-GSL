import datetime
import pandas as pd 
import math as m

"""
IMPORT DATA AND POPULATE INTO DATAFRAMES
   
format is datetime (month/20/year) and data type for monthly,
        datetime (01/01/year) and data type for annual


data to be imported    
    - snow water equivalent (snowpack) [inches]
    - lake level [units??]]
    - precipitation (salt lake metropolitan area) [inches]
    - gdp of utah (proxy for commercial water usage) [dollars]
    - population of utah (proxy for individual water usage)[people]

"""

###   IMPORT SNOW WATER EQUIVALENT DATA (inches)
snow_water = pd.read_csv('state_of_utah_snow_water.csv') # snow water equivalent

#find the mean swe per month
october_snow = snow_water.loc[:30].mean()
november_snow = snow_water.loc[31:60].mean()
december_snow = snow_water.loc[61:91].mean()
january_snow = snow_water.loc[92:122].mean()
february_snow = snow_water.loc[124:151].mean()
march_snow = snow_water.loc[152:182].mean()
april_snow = snow_water.loc[183:212].mean()
may_snow = snow_water.loc[213:243].mean()
june_snow = snow_water.loc[244:273].mean()
july_snow = snow_water.loc[274:304].mean()
august_snow = snow_water.loc[305:334].mean()
september_snow = snow_water.loc[335:365].mean()

#function to convert swe data to date time
    #one piece of data per month that is on the 20th
def populate_snow_datetime(data, month, start_year, df):
    for i in range(len(data)-10):
        temp = pd.DataFrame([[datetime.date(start_year+i,month,20), data[i]]],columns=['date','swe'])
        df = pd.concat([df,temp], ignore_index=True)
    return df

#populate into a data frame
swe_df = pd.DataFrame(columns=['date','swe'])

swe_df = populate_snow_datetime(october_snow, 10, 1981, swe_df)
swe_df = populate_snow_datetime(november_snow, 11, 1981, swe_df)
swe_df = populate_snow_datetime(december_snow, 12, 1981, swe_df)
swe_df = populate_snow_datetime(january_snow, 1, 1981, swe_df)
swe_df = populate_snow_datetime(february_snow, 2, 1981, swe_df)
swe_df = populate_snow_datetime(march_snow, 3, 1981, swe_df)
swe_df = populate_snow_datetime(april_snow, 4, 1981, swe_df)
swe_df = populate_snow_datetime(may_snow, 5, 1981, swe_df)
swe_df = populate_snow_datetime(june_snow, 6, 1981, swe_df)
swe_df = populate_snow_datetime(july_snow, 7, 1981, swe_df)
swe_df = populate_snow_datetime(august_snow, 8, 1981, swe_df)
swe_df = populate_snow_datetime(september_snow, 9, 1981, swe_df)

swe_df = swe_df.sort_values(by='date')

###   IMPORT LAKE LEVEL DATA 
lake_level = pd.read_csv('monthly', sep = '\t', comment = '#') 

#function to convert lake data to datetime
def populate_lake_datetime(data, df):
    for i in range(len(data)-1):
        temp = pd.DataFrame([[datetime.date(int(data['year_nu'][i+1]),int(data['month_nu'][i+1]),20), float(data['mean_va'][i+1])]],columns=['date','lake_level'])
        df = pd.concat([df,temp], ignore_index=True)
    return df

lk_lvl_df = pd.DataFrame(columns=['date','lake_level'])
lk_lvl_df = populate_lake_datetime(lake_level, lk_lvl_df)

###   IMPORT PRECIPITATION DATA (inches)
precipitation = pd.read_csv('precipitation_data.csv')

#function to convert pecipitation data to datetime
def populate_precip_datetime(data, df):

    for i in range(len(data)):
        for j in range(12):
            month = (str)(j+1)
            temp = pd.DataFrame([[datetime.date(int(data['Year'][i]),int(j+1),20), float(data[month][i])]],columns=['date','precipitation'])
            df = pd.concat([df,temp], ignore_index=True)

    return df

precip_df = pd.DataFrame(columns=['date','precipitation'])
precip_df = populate_precip_datetime(precipitation, precip_df)

###   IMPORT GDP DATA (some form of dollars)
gdp = pd.read_csv('UTNGSP.csv')

#function to convert gdp data to datetime
def populate_gdp_datetime(data, df):

    for i in range(len(data)):
        year = data['DATE'][i][:4]
        temp = pd.DataFrame([[datetime.date(int(year),int(1),20), float(data['UTNGSP'][i])]],columns=['date','gdp'])
        df = pd.concat([df,temp], ignore_index=True)

    return df

gdp_df = pd.DataFrame(columns=['date','gdp'])
gdp_df = populate_gdp_datetime(gdp, gdp_df)

###   IMPORT POPULATION GROWTH DATA
pop_growth = pd.read_csv('population_growth.csv')

def populate_pop_datetime(data, df):

    for i in range(len(data)):
        temp = pd.DataFrame([[datetime.date(int(pop_growth['year'][i]),int(1),20), float(data['pop'][i])]],columns=['date','population'])
        df = pd.concat([df,temp], ignore_index=True)

    return df

pop_df = pd.DataFrame(columns=['date','population'])
pop_df = populate_pop_datetime(pop_growth, pop_df)

###   SLICE ALL DFS TO 1990
swe_monthly = swe_df.loc[swe_df["date"]>datetime.date(1990,1,1)]
precip_monthly = precip_df.loc[precip_df["date"]>datetime.date(1990,1,1)]
lk_lvl_monthly = lk_lvl_df.loc[lk_lvl_df["date"]>datetime.date(1990,1,1)]
gdp_annual = gdp_df.loc[gdp_df["date"]>datetime.date(1990,1,1)]
pop_annual = pop_df.loc[pop_df["date"]>datetime.date(1990,1,1)]

#reset indexes
swe_monthly = swe_monthly.reset_index(drop=True)
precip_monthly = precip_monthly.reset_index(drop=True)
lk_lvl_monthly = lk_lvl_monthly.reset_index(drop=True)
gdp_annual = gdp_annual.reset_index(drop=True)
pop_annual = pop_annual.reset_index(drop=True)

###    ANNUAL INFORMATION FOR MONTHLY DATA

#function to sum months to get annual data from monthly data
def make_annual_sum(df, str, df_annual):
    curr_year = 1990
    curr_inches = 0
    month = 0

    for i in range(len(df)):
        month += 1
        if(int(df['date'][i].year)==curr_year):
            curr_inches += df[str][i]
        elif(month>12 or i == len(df)):
            temp = pd.DataFrame([[datetime.date(int(curr_year),int(1),20), float(curr_inches)]],columns=['date', str])
            df_annual = pd.concat([df_annual,temp], ignore_index=True)
            curr_year += 1
            curr_inches = 0

    return df_annual

swe_annual = pd.DataFrame(columns=['date','swe'])
swe_annual = make_annual_sum(swe_monthly, 'swe', swe_annual)

precip_annual = pd.DataFrame(columns=['date','precipitation'])
precip_annual = make_annual_sum(precip_monthly, 'precipitation', precip_annual)

def make_annual_lake_level(df, str, df_annual):
    month = 0

    for i in range(len(df)):
        month += 1
        if(int(df['date'][i].month)==1):
            temp = pd.DataFrame([[df['date'][i], float(df[str][i])]],columns=['date', str])
            df_annual = pd.concat([df_annual,temp], ignore_index=True)

    return df_annual

lk_lvl_annual = pd.DataFrame(columns=['date','lake_level'])
lk_lvl_annual = make_annual_lake_level(lk_lvl_monthly, 'lake_level', lk_lvl_annual)


###    CLEAN DATA

#monthly
swe_monthly 
precip_monthly 
lk_lvl_monthly 

#annual
gdp_annual 
pop_annual
precip_annual
lk_lvl_annual 
