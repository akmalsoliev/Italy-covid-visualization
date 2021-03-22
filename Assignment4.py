import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


covid_data = pd.read_csv('Daily_Covis19_Italian_Data_Province_Incremental.csv')

covid_positive = covid_data.groupby('Date').agg({'Total Positive': np.sum})

fig, ax = plt.subplots(figsize=[8, 4.5])

ax.plot(covid_positive)

# Labeling
plt.title('COVID-19 Italy \nNumber of new cases by from Feb 2019')
plt.xlabel('Months')
plt.ylabel('Number of people')

# Setting x-tick labels.
locations = np.arange(0, 393, 30)#393
plt.xticks(locations, np.linspace(0, len(locations), len(locations), dtype=int))

plt.show()