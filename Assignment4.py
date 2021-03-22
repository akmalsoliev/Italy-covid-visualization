import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


covid_data = pd.read_csv('Daily_Covis19_Italian_Data_Province_Incremental.csv')

covid_data.plot()

covid_positive = covid_data.groupby('Date').agg(np.sum)

plt.plot(covid_positive)
plt.show()