import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import re
import numpy as np
import pandas as pd


url = 'https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic#Epidemiology' 
headers = {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'lxml')


# Finding the top countries from a wikipedia table

countries =[]                         
for country in soup.select('[title*="2020 coronavirus pandemic in "]'):
    countries.append(country.get_text())

countries_infected = countries[:30]
print(countries_infected)
print(len(countries_infected))

#Finding the infected numbers per country

cont = soup.find(id = "covid19-container")
table_ = cont.table
#print(table_)

table_rows = table_.find_all('tr')

infected = []                            # taking data from table
for tr in table_rows:
	td = tr.find_all("td")
	row = [i.text for i in td]
	#print(row)
	infected += row

infected_list = infected[:-3]               # cuting the end of list that have strings instead of numbers
#print(infected_list)

def inf(list_inf):                          # taking every 4th element from the list 
	#for i in range(len(infected))
	#	if i%4==0 append list_inf[i]
	return [list_inf[i] for i in range(len(list_inf)) if i%4==0]

infected_real = inf(infected_list)  

infected_final = [infected_real[i][:-1] for i in range(len(infected_real))]         # slicing '\n' from the end of every number    
#print(infected_final)


                               
infected_final2 = [float(str.replace(',', '')) for str in infected_final]           # replasing ',' with '' into the numbers
infected_final3 = infected_final2[:30]
print(infected_final3)
print(len(infected_final3))


deaths = []
deaths = inf(infected_list[1:])                                # slicing the first number in order to catch every 4th number of deaths
#print(deaths)
deaths_final = [deaths[i][:-1] for i in range(len(deaths))]         # slicing '\n' from the end of every number 
 

deaths_final2 = [float(str.replace(',', '')) for str in deaths_final] 
deaths_final2 = deaths_final2[:30] 

print(deaths_final2)
print(len(deaths_final2))   

list_percentage = []
def percentage(list1, list2):                  # calculating percentage from 2 lists making 3
	for i,j in zip(list1,list2):
		list_percentage.append((round((j*100/i), 2)))          # j*100/i is percentage, round() to 2 decimals
	return list_percentage

percentage(infected_final3, deaths_final2)
list_percentage2 = list_percentage[:30]
print(list_percentage2)

#Ploting

countries_infected.reverse()               # on horisontal bar chart the biggest to be on the top
list_percentage2.reverse()

df = pd.DataFrame({'percentage': list_percentage2}, index=countries_infected)

ax = df.plot.barh()

plt.title("Coronavirus percentage of deaths over total infected people in Top 30 most infected countries")
plt.xlabel("Percentage\n Apr 13 2020")
plt.ylabel("Countries and territories")
plt.tight_layout()
plt.show()
print('Done')