import pandas as pd
import glob

txtfiles = []
for file in glob.glob("COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv"):
    txtfiles.append(file[56:])

main_df=pd.DataFrame()


for i in txtfiles:
    temp_file = pd.read_csv("COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/{}".format(i))
    temp_file['Last Update'] = pd.to_datetime(temp_file['Last Update'])
    temp_date = temp_file['Last Update'][0].date()

    temp_df = temp_file.groupby('Country/Region').sum()
    temp_df['record_date']=temp_date

    main_df = main_df.append(temp_df)

temp.groupby(temp.index).resample('W', on='record_date').sum()


for i in txtfiles[txtfiles.index(i):]:
    temp_file = pd.read_csv("COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/{}".format(i))
    temp_file['Last_Update'] = pd.to_datetime(temp_file['Last_Update'])
    temp_date = temp_file['Last_Update'][0].date()

    temp_df = temp_file.groupby('Country_Region').sum()
    temp_df['record_date']=temp_date

    main_df = main_df.append(temp_df)

temp_df['record_date'] = pd.to_datetime(temp_df['record_date'])

temp_df.groupby(temp_df.index).resample('W', on='record_date').sum()

main_df.groupby(main_df.index).tail(1).sort_values('Confirmed', ascending=False).head(11)

main_df2 = main_df[main_df.index.isin(['US', 'Italy', 'Spain', 'France', 'United Kingdom', 'China', 'Iran',
       'Belgium', 'Germany', 'Netherlands', 'Brazil', 'India', 'Russia', 'Turkey'])]

main_df2['Population(m)'] = 0

main_df2.loc[main_df2.index=='US','Population(m)'] = 328
main_df2.loc[main_df2.index=='Spain','Population(m)'] = 47
main_df2.loc[main_df2.index=='Italy','Population(m)'] = 60
main_df2.loc[main_df2.index=='Belgium','Population(m)'] = 11
main_df2.loc[main_df2.index=='France','Population(m)'] = 67
main_df2.loc[main_df2.index=='United Kingdom','Population(m)'] = 67
main_df2.loc[main_df2.index=='China','Population(m)'] = 1393
main_df2.loc[main_df2.index=='Iran','Population(m)'] = 82
main_df2.loc[main_df2.index=='Germany','Population(m)'] = 83
main_df2.loc[main_df2.index=='Netherlands','Population(m)'] = 17
main_df2.loc[main_df2.index=='Brazil','Population(m)'] = 210
main_df2.loc[main_df2.index=='India','Population(m)'] = 1366
main_df2.loc[main_df2.index=='Russia','Population(m)'] = 145
main_df2.loc[main_df2.index=='Turkey','Population(m)'] = 83

main_df2.loc[main_df2.index=='US', 'Population density /sq mi'] = 87
main_df2.loc[main_df2.index=='Spain', 'Population density /sq mi'] = 241
main_df2.loc[main_df2.index=='Italy', 'Population density /sq mi'] = 518
main_df2.loc[main_df2.index=='Belgium', 'Population density /sq mi'] = 974
main_df2.loc[main_df2.index=='France', 'Population density /sq mi'] = 319
main_df2.loc[main_df2.index=='United Kingdom', 'Population density /sq mi'] = 710
main_df2.loc[main_df2.index=='China', 'Population density /sq mi'] = 377
main_df2.loc[main_df2.index=='Iran', 'Population density /sq mi'] = 131
main_df2.loc[main_df2.index=='Germany', 'Population density /sq mi'] = 603
main_df2.loc[main_df2.index=='Netherlands', 'Population density /sq mi'] = 1089
main_df2.loc[main_df2.index=='Brazil', 'Population density /sq mi'] = 64
main_df2.loc[main_df2.index=='India','Population density /sq mi'] = 1073
main_df2.loc[main_df2.index=='Russia','Population density /sq mi'] = 23
main_df2.loc[main_df2.index=='Turkey','Population density /sq mi'] = 275

main_df2.to_excel("covid_aggregated_filtered_2.xls")