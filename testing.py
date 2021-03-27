import re
import wikipedia as wp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Wikipedia scrapper

wiki_page = 'Climate_of_Italy'
html = wp.page(wiki_page).html().replace(u'\u2212', '-')


def dataframe_cleaning(table_number: int):
    global html
    df = pd.read_html(html, encoding='utf-8')[table_number]
    df.drop(np.arange(5, len(df.index)), inplace=True)
    df.columns = df.columns.droplevel()
    df.drop('Year', axis=1, inplace=True)

    find = '\((.*?)\)'
    for i, column in enumerate(df.columns):
        if i > 0:
            df[column] = (df[column]
                          .str.findall(find)
                          .map(lambda x: (float(x[0]) - 32) * (5 / 9)))
    return df


# Setting up all the DataFrames that will be used to plot Italy's average temperature with high and low variation.

potenza_df = dataframe_cleaning(3)
milan_df = dataframe_cleaning(4)
florence_df = dataframe_cleaning(6)

# Constructing aggregated DataFrame for all temperatures in Italy:

concat_df = pd.concat((potenza_df, milan_df, florence_df))

italy_df = pd.DataFrame()
for i, index in enumerate(list(set(concat_df['Month']))):
    if i == 0:
        temp_df = concat_df[concat_df['Month'] == index]
        temp_df = temp_df.groupby('Month').agg(np.max)
    if i in range(1, 4):
        temp_df = concat_df[concat_df['Month'] == index]
        temp_df = temp_df.groupby('Month').agg(np.mean)
    if i == 4:
        temp_df = concat_df[concat_df['Month'] == index]
        temp_df = temp_df.groupby('Month').agg(np.min)
    italy_df = italy_df.append(temp_df)

italy_df = italy_df.apply(lambda x: np.round(x, 2))
italy_df

# Importing DATA
url = 'https://github.com/DavideMagno/ItalianCovidData/blob/master/Daily_Covis19_Italian_Data_Province_Incremental.csv'
covid_data = pd.read_csv(url, index_col=0)

while True:
    pass

# Grouping
covid_positive = covid_data.groupby('Date').agg({'Total Positive': np.sum})

# Creating plot
fig, ax = plt.subplots(figsize=[8, 4.5])

# Plotting
ax.plot(covid_positive)

# Labeling
plt.title('COVID-19 Italy \nNumber of new cases by from Feb 2019')
plt.xlabel('Months')
plt.ylabel('Number of new cases')

# Setting x-tick labels.
locations = np.arange(0, 393, 30)
plt.xticks(locations, np.linspace(0, len(locations), len(locations), dtype=int))

plt.show()
