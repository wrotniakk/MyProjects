#!/usr/bin/env python
# coding: utf-8

# # Population of various countries- analysis
# ## Data provided by The World Bank

# Tools used in this raport will be mainly provided by the pandas and matplotlib libraries

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as random
get_ipython().run_line_magic('matplotlib', 'inline')


# ## 1. Data preparation

# First, let's take a look at the data we will be analyzing:

# In[4]:


countries = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_4902028.csv',
                       skiprows=4)
countries.set_index("Country Name", inplace = True)
countries


# Next lets filter out 'Country Groupes' out of the data frame (such as South Asia, Arab Wolrd, etc):

# In[5]:


country_list = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Vietnam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']


# In[6]:


countries = countries[countries.index.isin(country_list)]


# ## 2. Barplots
# ### a) Top 5 most populated

# Let's find the 5 most populated countries (most recent data goes back to 2021):

# In[7]:


countries["2021"].nlargest()


# So now let us visualize how populations of these countries were changing over years. For that, we prepare a smaller dataframe, containing only these five countries (we will also remove the last column "Unnamed" full of NaN values).

# In[8]:


df = countries[countries.index.isin(countries["2021"].nlargest().index)]
df = df.drop(labels = df.columns[-1], axis = 1)


# In[9]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[29]:


with plt.style.context('Solarize_Light2'):
    fig = plt.figure(figsize = (10,5))
    ax = fig.add_subplot()


    plt.xlim(0,2000000000)
    ax.xaxis.set_ticks(range(0,1900000000,200000000), labels = ['0','200M','400M','600M','800M','1 MLD','1.2 MLD','1.4 MLD','1.6 MLD','1.8 MLD'])

    ax.set_title('Top 5 Most Populated Countries')
    ax.set_xlabel(xlabel ='Population',loc = 'left')

    bars = ax.barh(df.index, df['1960'], color='teal')
    text = ax.text(1500000000,4,'', fontsize = 20,
                   bbox = dict(facecolor = '#F3EADA',edgecolor="black"),
                  fontstyle = 'italic')
    labs = [ax.text(0,i,'',bbox = dict(facecolor = '#F3EADA',edgecolor="black"),
                    fontsize=12) for i in range(5)]

    def update(year):

        for i in range(5):
            bars[i].set(width = df.iloc[i][f"{year}"])
            labs[i].set_text(df.iloc[i]['Country Code'])
            labs[i].set_x(bars[i].get_width()+50000000)

        text.set_text(f"{year}")

        return bars,labs[0],labs[1],labs[2],labs[3],labs[4]
                
    



    animate = FuncAnimation(fig, update, range(1960,2022), repeat = False, blit = True)

    plt.show()


# (And the black&white version):

# In[30]:


with plt.style.context('default'):
    fig = plt.figure(figsize = (6,3))
    ax = fig.add_subplot()


    plt.xlim(0,2000000000)
    ax.xaxis.set_ticks(range(0,1900000000,200000000),
                       labels = ['0','200M','400M','600M','800M','1 MLD','1.2 MLD','1.4 MLD','1.6 MLD','1.8 MLD'],
                       fontsize=7)

    ax.set_title('Top 5 Most Populated Countries', fontsize=16)
    ax.set_xlabel(xlabel ='Population',loc = 'left', fontsize=10)

    bars = ax.barh(df.index, df['1960'], color='black')
    text = ax.text(1500000000,4,'', fontsize = 12,
                   bbox = dict(facecolor = 'white',edgecolor="black"),
                  fontstyle = 'italic')
    labs = [ax.text(0,i,'',bbox = dict(facecolor = 'white',edgecolor="black"),
                    fontsize=6) for i in range(5)]

    def update(year):

        for i in range(5):
            bars[i].set(width = df.iloc[i][f"{year}"])
            labs[i].set_text(df.iloc[i]['Country Code'])
            labs[i].set_x(bars[i].get_width()+50000000)

        text.set_text(f"{year}")

        return bars,labs[0],labs[1],labs[2],labs[3],labs[4]
                
    



    animate = FuncAnimation(fig, update, range(1960,2022), repeat = False, blit = True)

    plt.show()


# ### b) Random country from random year as a 'centroid'

# For the next part we will pick one country and year at random. Next, after narrowing down our dataframe to only the chosen year, let us add a new column, containing information on how much difference there is between population of every country and our chosen country.
# In other words, we'll be examining the absolute value of difference between populations

# In[10]:


num_of_countries = len(countries.index)  # so we know how much countries
num_of_countries                         # there is in the dataset


# So now, our chosen country and year are

# In[41]:


"""
Here is the cell I executed the first time. Then, all of the data
concerning this part is based on this (random at the time) outcome.
I keep it commented out, so that the following data and plots stay
adequate

country_num, year_num = random.randint(0,180), random.randint(1960,2021)
chosen = countries.index[country_num]
chosen, year_num
"""


# In[12]:


chosen = "Marshall Islands"
year_num = 1990


# We then proceed now to adding the new column to our dataframe

# In[13]:


new_df = countries[f"{year_num}"].to_frame()
new_df


# In[14]:


new_df["Abs Difference"] = [abs(new_df.loc[chosen][0]-new_df.iloc[i][0])
                                 for i in range(num_of_countries)]
new_df


# Now we'll make a dataframe containing our chosen country and 4 others, whose population in the given year was the smallest, in realtion to the chosen country.
# Then, we proceed to make yet another plot of population change over years.

# In[15]:


df2 = countries[countries.index.isin(new_df["Abs Difference"].nsmallest().index)]
df2 = df2.drop(labels = df2.columns[-1], axis = 1)
df2


# In[16]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[32]:


with plt.style.context('Solarize_Light2'):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot()

    plt.xlim(0,110000)
    ax.xaxis.set_ticks(range(0,110000,20000),
                       labels = ['0','20T','40T','60T','80T','100T'])

    ax.set_title('Dynamic population of 5 chosen countries', fontsize=20)
    ax.set_xlabel(xlabel ='Population',loc = 'left')

    bars = ax.barh(df2.index, df2['1960'], color='#B740AD')

    text = ax.text(85000,2,'', fontsize = 20,
                   bbox = dict(facecolor = '#F3EADA',edgecolor="black"),
                  fontstyle = 'italic')

    labs = [ax.text(0,i,'',bbox = dict(facecolor = '#F3EADA',edgecolor="black"),
                    fontsize=12) for i in range(5)]

    def update(year):

        for i in range(5):
            bars[i].set_width(df2.iloc[i][f"{year}"])
            labs[i].set_text(df2.iloc[i]['Country Code'])
            labs[i].set_x(bars[i].get_width()+1500)

        text.set_text(f"{year}")

        return bars, labs[0],labs[1],labs[2],labs[3],labs[4]

    animate = FuncAnimation(fig, update, range(1960,2022), interval = 100, repeat = False, blit = True)

    plt.show()


# (And black&white version):

# In[24]:


with plt.style.context('default'):
    fig = plt.figure(figsize=(6,3))
    ax = fig.add_subplot()

    plt.xlim(0,110000)
    ax.xaxis.set_ticks(range(0,110000,20000),
                       labels = ['0','20T','40T','60T','80T','100T'],
                      fontsize=7)

    ax.set_title('Dynamic population of 5 chosen countries', fontsize=12)
    ax.set_xlabel(xlabel ='Population',loc = 'left')

    bars = ax.barh(df2.index, df2['1960'], color='black')

    text = ax.text(85000,2,'', fontsize = 10,
                   bbox = dict(facecolor = 'white',edgecolor="black"),
                  fontstyle = 'italic')

    labs = [ax.text(0,i,'', bbox = dict(facecolor = 'white',edgecolor="black"),
                    fontsize=6) for i in range(5)]

    def update(year):

        for i in range(5):
            bars[i].set_width(df2.iloc[i][f"{year}"])
            labs[i].set_text(df2.iloc[i]['Country Code'])
            labs[i].set_x(bars[i].get_width()+3000)

        text.set_text(f"{year}")

        return bars, labs[0],labs[1],labs[2],labs[3],labs[4]

    animate = FuncAnimation(fig, update, range(1960,2022), interval = 200, repeat = False, blit = True)

    plt.show()


# ### c) Poland from random year as a 'centroid'

# Okay, so now we generate a similar barplot, but this time with Poland as the 'centroid'.

# In[96]:


# rand_year = random.randint(1960,2021)


# In[17]:


rand_year = 2011


# In[18]:


poland_df = countries[f"{rand_year}"].to_frame()
poland_df


# In[36]:


poland_df["Abs Difference"] = [abs(poland_df.loc['Poland'][0]-poland_df.iloc[i][0])
                                 for i in range(num_of_countries)]
poland_df


# In[38]:


df3 = countries[countries.index.isin(poland_df["Abs Difference"].nsmallest().index)]
df3 = df3.drop(labels = df3.columns[-1], axis = 1)
df3


# In[39]:


with plt.style.context('Solarize_Light2'):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot()

    plt.xlim(0,60000000)
    ax.xaxis.set_ticks(range(0,60000000,5000000),
                       labels = ['0','5M','10M','15M','20M','25M','30M','35M','40M','45M','50M','55M'])

    ax.set_title('Dynamic population of 5 chosen countries (Poland as centroid)',
                 loc='left',
                 pad = 10)
    ax.set_xlabel(xlabel ='Population',loc = 'left')

    bars = ax.barh(df3.index, df3['1960'], color='#FF6F91')

    text = ax.text(50000000,3,'', fontsize = 20,
                   bbox = dict(facecolor = '#F3EADA',edgecolor="black"),
                  fontstyle = 'italic')

    labs = [ax.text(0,i,'',bbox = dict(facecolor = '#F3EADA',edgecolor="black"),
                    fontsize=12) for i in range(5)]

    def update(year):

        for i in range(5):
            bars[i].set_width(df3.iloc[i][f"{year}"])
            labs[i].set_text(df3.iloc[i]['Country Code'])
            labs[i].set_x(bars[i].get_width()+1000000)

        text.set_text(f"{year}")

        return bars, labs[0],labs[1],labs[2],labs[3],labs[4]

    animate = FuncAnimation(fig, update, range(1960,2022), interval = 200, repeat = False, blit = True)

    plt.show()


# (And the black&white version):

# In[31]:


with plt.style.context('default'):
    fig = plt.figure(figsize=(6,3))
    ax = fig.add_subplot()

    plt.xlim(0,60000000)
    ax.xaxis.set_ticks(range(0,60000000,5000000),
                       labels = ['0','5M','10M','15M','20M','25M','30M','35M','40M','45M','50M','55M'],
                      fontsize=7)

    ax.set_title('Population of 5 chosen countries (Poland as centroid)',
                 loc='left',
                 pad = 10,
                fontsize=12)
    ax.set_xlabel(xlabel ='Population',loc = 'left', fontsize=10)

    bars = ax.barh(df3.index, df3['1960'], color='black')

    text = ax.text(50000000,3,'', fontsize = 10,
                   bbox = dict(facecolor = 'white',edgecolor="black"),
                  fontstyle = 'italic')

    labs = [ax.text(0,i,'',bbox = dict(facecolor = 'white',edgecolor="black"),
                    fontsize=7) for i in range(5)]

    def update(year):

        for i in range(5):
            bars[i].set_width(df3.iloc[i][f"{year}"])
            labs[i].set_text(df3.iloc[i]['Country Code'])
            labs[i].set_x(bars[i].get_width()+1500000)

        text.set_text(f"{year}")

        return bars, labs[0],labs[1],labs[2],labs[3],labs[4]

    animate = FuncAnimation(fig, update, range(1960,2022), interval = 200, repeat = False, blit = True)

    plt.show()


# It's actually pretty interesting how Poland was so much ahead, in terms of population, compared to the other four, just to finish last in the year 2021. Truly remarkable what happened, especially in African countries- Sudan and Algieria.

# ## 3. Line plots
# ### a) Top 5 populated countries

# Let's remind ourselves the dataframe we'll be using for the next plot

# In[20]:


df


# In[38]:


with plt.style.context('ggplot'):
    
    # Looks
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot()
    plt.xlim(1960,2025)
    ax.xaxis.set_ticks(range(1960,2030,10))
    plt.ylim(0,1800000000)
    ax.yaxis.set_ticks(range(0,1800000001,200000000),
                      labels=['0','200M','400M','600M','800M','1 MLD','1.2 MLD','1.4 MLD','1.6 MLD','1.8 MLD'])
    ax.set_title("Top 5 Most Populated Countries", fontsize=20)

    # Preparing data
    china_line, = ax.plot([],[],color='red')
    china_line.set_label("China")
    china_data = [[],[]]
    
    indo_line, = ax.plot([],[],color='#3ABF2B', label="Indonesia")
    indo_line.set_label("Indonesia")
    indo_data = [[],[]]
    
    india_line, = ax.plot([],[],color='olive', label="India")
    india_line.set_label("India")
    india_data = [[],[]]
    
    pak_line, = ax.plot([],[],color='brown', label="Pakistan")
    pak_line.set_label("Pakistan")
    pak_data = [[],[]]
    
    usa_line, = ax.plot([],[],color='teal', label="USA")
    usa_line.set_label("USA")
    usa_data = [[],[]]
    
    ax.legend(loc="upper left")
    
    """
    I dont add the 'Country Code' labels to the lines as I'm not
    sure how that's supposed to look like to avoid those labels
    overlapping with each other- especially in the context of
    Indonesia, Pakistan and USA, whose populations run somewhat
    close to each other.
    That's why I added the legend instead.
    (same applies to the next lineplots)
    """
    
    text = ax.text(1990,1600000000,'', fontsize = 20,
                   bbox = dict(facecolor = (0.9,0.9,0.9),edgecolor="black"),
                  fontstyle = 'italic')

    
    # Function
    def update(year):
        
        china_data[0].append(year)
        china_data[1].append(df.loc["China"][f"{year}"])
        indo_data[0].append(year)
        indo_data[1].append(df.loc["Indonesia"][f"{year}"])
        india_data[0].append(year)
        india_data[1].append(df.loc["India"][f"{year}"])
        pak_data[0].append(year)
        pak_data[1].append(df.loc["Pakistan"][f"{year}"])
        usa_data[0].append(year)
        usa_data[1].append(df.loc["United States"][f"{year}"])
        
        china_line.set_data(china_data[0],china_data[1])
        indo_line.set_data(indo_data[0],indo_data[1])
        india_line.set_data(india_data[0],india_data[1])
        pak_line.set_data(pak_data[0],pak_data[1])
        usa_line.set_data(usa_data[0],usa_data[1])
        
        text.set_text(f"{year}")
        
        return china_line,indo_line,india_line,pak_line,usa_line
    
    animation = FuncAnimation(fig,update,range(1960,2022),interval=100,repeat=False, blit=True)
    plt.show()
        


# ### b) Population of countries close to the "centroid"

# Let's remember ourselves the dataframe for our lineplot (we're not random-selecting the country and year again as we want to simply create a line version for the previous barplot)

# In[34]:


df2


# In[25]:


with plt.style.context('ggplot'):
    
    # Looks
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot()
    plt.xlim(1960,2025)
    ax.xaxis.set_ticks(range(1960,2030,10))
    plt.ylim(0,110000)
    ax.yaxis.set_ticks(range(0,110000,20000),
                       labels = ['0','20T','40T','60T','80T','100T'])

    ax.set_title("Dynamic population of 5 chosen countries", fontsize=20)

    andora_line, = ax.plot([],[],color='red',label="Andorra")
    andora_data = [[],[]]
    
    amsamoa_line, = ax.plot([],[],color='#3ABF2B', label="American Samoa")
    amsamoa_data = [[],[]]
    
    farislands_line, = ax.plot([],[],color='olive', label="Faroe Islands")
    farislands_data = [[],[]]
    
    marshislands_line, = ax.plot([],[],color='brown', label="Marshal Islands")
    marshislands_data = [[],[]]
    
    nmarislands_line, = ax.plot([],[],color='teal', label="Northern Mariana Islands")
    nmarislands_data = [[],[]]
    
    ax.legend(loc="upper left")
    
    
    text = ax.text(1990,90000,'', fontsize = 20,
                   bbox = dict(facecolor = (0.9,0.9,0.9),edgecolor="black"),
                  fontstyle = 'italic')

    # Function
    def update(year):
        
        andora_data[0].append(year)
        andora_data[1].append(df2.loc["Andorra"][f"{year}"])
        amsamoa_data[0].append(year)
        amsamoa_data[1].append(df2.loc["American Samoa"][f"{year}"])
        farislands_data[0].append(year)
        farislands_data[1].append(df2.loc["Faroe Islands"][f"{year}"])
        marshislands_data[0].append(year)
        marshislands_data[1].append(df2.loc["Marshall Islands"][f"{year}"])
        nmarislands_data[0].append(year)
        nmarislands_data[1].append(df2.loc["Northern Mariana Islands"][f"{year}"])
        
        andora_line.set_data(andora_data[0],andora_data[1])
        amsamoa_line.set_data(amsamoa_data[0],amsamoa_data[1])
        farislands_line.set_data(farislands_data[0],farislands_data[1])
        marshislands_line.set_data(marshislands_data[0],marshislands_data[1])
        nmarislands_line.set_data(nmarislands_data[0],nmarislands_data[1])
        
        text.set_text(f"{year}")
        
        return andora_line,amsamoa_line,farislands_line,marshislands_line,nmarislands_line, text
    
    
    animation = FuncAnimation(fig,update,range(1960,2022),interval=200,repeat=False,blit=True)
    plt.show()
    


# ### c) Population of countries close to Poland

# Let's remind ourselves of the dataframe we're going to use. We use Poland as the 'centroid' and once again, we leave 2011 as our centroid year (we do NOT random-generate it) 

# In[49]:


df3


# In[355]:


with plt.style.context('ggplot'):
    
    # Looks
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot()
    plt.xlim(1960,2025)
    ax.xaxis.set_ticks(range(1960,2030,10))
    plt.ylim(0,60000000)
    ax.yaxis.set_ticks(range(0,60000000,5000000),
                       labels = ['0','5M','10M','15M','20M','25M','30M','35M','40M','45M','50M','55M'],
                      fontsize=10)

    ax.set_title('Population of 5 chosen countries (Poland as centroid)',
                 loc='left',
                 pad = 10,
                fontsize=20)
    
    arg_line, = ax.plot([],[],color='#00C4FF',label="Argentina")
    arg_data = [[],[]]
    
    canada_line, = ax.plot([],[],color='#3ABF2B', label="Canada")
    canada_data = [[],[]]
    
    algeria_line, = ax.plot([],[],color='olive', label="Algeria")
    algeria_data = [[],[]]
    
    poland_line, = ax.plot([],[],color='red', label="Poland")
    poland_data = [[],[]]
    
    sudan_line, = ax.plot([],[],color='brown', label="Sudan")
    sudan_data = [[],[]]
    
    ax.legend(loc="upper left")
    
    
    text = ax.text(1982,50000000,'', fontsize = 20,
                   bbox = dict(facecolor = (0.9,0.9,0.9),edgecolor="black"),
                  fontstyle = 'italic')

    # Function
    def update(year):
        
        arg_data[0].append(year)
        arg_data[1].append(df3.loc["Argentina"][f"{year}"])
        canada_data[0].append(year)
        canada_data[1].append(df3.loc["Canada"][f"{year}"])
        algeria_data[0].append(year)
        algeria_data[1].append(df3.loc["Algeria"][f"{year}"])
        poland_data[0].append(year)
        poland_data[1].append(df3.loc["Poland"][f"{year}"])
        sudan_data[0].append(year)
        sudan_data[1].append(df3.loc["Sudan"][f"{year}"])
        
        arg_line.set_data(arg_data[0],arg_data[1])
        canada_line.set_data(canada_data[0],canada_data[1])
        algeria_line.set_data(algeria_data[0],algeria_data[1])
        poland_line.set_data(poland_data[0],poland_data[1])
        sudan_line.set_data(sudan_data[0],sudan_data[1])
        
        text.set_text(f"{year}")
        
        return arg_line,canada_line,algeria_line,poland_line,sudan_line, text
    
    
    animation = FuncAnimation(fig,update,range(1960,2022),interval=200,repeat=False,blit=True)
    plt.show()


# ## 4. Bubble plots

# Now our goal is to create, for previously used data, a coresponding bubble plots, so scatter plots with a 3rd dimension, indicted by the point volume (a bubble). This bubble will provide us with information on population density in the given year

# For the population density, we will need actual area of the countries, so that we could then take a population and divide it by the area of the coresponding country. For that, we import another dataset from The World Bank.

# In[21]:


area = pd.read_csv('API_AG.LND.TOTL.K2_DS2_en_csv_v2_5161402/API_AG.LND.TOTL.K2_DS2_en_csv_v2_5161402.csv',
                   skiprows=4)


# In[22]:


area.set_index('Country Name', inplace=True)


# In[23]:


area = area[area.index.isin(country_list)]


# In[24]:


area.info()


# We have some missing values. Lets take care of that:

# In[25]:


area.dropna(axis=1, how='all', inplace=True)


# In[26]:


area.fillna(0, inplace=True)


# In[27]:


area.info()


# We removed the columns that 'contained' only a missing values. As for the rest missing values, they are now replaced with a '0', which should make sense- we treat such a country as a non-existent.

# ### a) Top 5 populated countries

# In[65]:


df


# For every country, lets prepare a separate dataframe, with population, area and density for every year 

# In[28]:


new_dfs = []
for i in range(5):
    new_dfs.append(pd.concat([df.iloc[i]['1961':'2020'],area.loc[df.index[i]]["1961":"2020"]],axis=1))
    new_dfs[i].columns = ["Population", "Area"]
    new_dfs[i]["Density"] = (new_dfs[i]["Population"])/(new_dfs[i]["Area"])
    new_dfs[i] = new_dfs[i].convert_dtypes()


# In[29]:


china_df = new_dfs[0]
indo_df = new_dfs[1]
india_df = new_dfs[2]
pak_df = new_dfs[3]
usa_df = new_dfs[4]


# In[30]:


china_df


# We will generate bubbles for every 10 years passing from 1961 (up to 2020, where our data ends), since the bubble plot containing as much as 59 bubbles (one for EVERY year), for each of five countries (making it 295 bubbles in total), would be disgusting and illegible.

# In[193]:


with plt.style.context("ggplot"):
    
    """
    Once again, I will not include Country Tags, since the bubble plot 
    even now is barely readable. The Tags would inevitably generate on
    top of each other, resulting in a visual catastrophe...
    The same goes for the next bubble plots.
    """

    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot()
    plt.ylim(0,1800000000)
    ax.yaxis.set_ticks(range(0,1800000001,200000000),
                      labels=['0','200M','400M','600M','800M','1 MLD','1.2 MLD','1.4 MLD','1.6 MLD','1.8 MLD'])
    ax.set_title("Top 5 Most Populated Countries", fontsize=24)
    plt.xlim(1958,2025)
    ax.xaxis.set_ticks([i for i in range(1961,2021,10)]+[2020])
    text = ax.text(1979,1500000000,"",
            bbox = dict(facecolor = 'white',edgecolor="black"),
           fontsize=24, fontstyle="italic")
    
    # For the legend
    ax.scatter(x=[0],y=[0],color='red',label='China')
    ax.scatter(x=[0],y=[0],color='#3ABF2B',label='Indonesia')
    ax.scatter(x=[0],y=[0],color='olive',label='India')
    ax.scatter(x=[0],y=[0],color='brown',label='Pakistan')
    ax.scatter(x=[0],y=[0],color='teal',label='USA')
                    
    ax.legend(loc="upper left", fontsize=15)

    def update(year):
        
        
        if year == 2020:
            
            a = [i for i in range(0,year-1960,10)] + [len(china_df)-1]
            
            # China
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=china_df["Population"].values[a],
                       s=china_df["Density"].values[a]*20,
                       alpha = 0.5, color='red', label="China")
            # Indonesia
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=indo_df["Population"].values[a],
                       s=indo_df["Density"].values[a]*20,
                       alpha = 0.5, color='#3ABF2B',label="Indonesia")
            # India
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=india_df["Population"].values[a],
                       s=india_df["Density"].values[a]*20,
                       alpha = 0.5, color='olive', label="India")
            # Pakistan
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=pak_df["Population"].values[a],
                       s=pak_df["Density"].values[a]*20,
                       alpha = 0.5, color='brown', label="Pakistan")
            # USA
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=usa_df["Population"].values[a],
                       s=usa_df["Density"].values[a]*20,
                       alpha = 0.5, color='teal', label="USA")
        else:
            
            a = [i for i in range(0,year-1960,10)]
            
            # China
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=china_df["Population"].values[a],
                       s=china_df["Density"].values[a]*20,
                       alpha = 0.5, color='red', label="China")
            # Indonesia
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=indo_df["Population"].values[a],
                       s=indo_df["Density"].values[a]*20,
                       alpha = 0.5, color='#3ABF2B',label="Indonesia")
            # India
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=india_df["Population"].values[a],
                       s=india_df["Density"].values[a]*20,
                       alpha = 0.5, color='olive', label="India")
            # Pakistan
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=pak_df["Population"].values[a],
                       s=pak_df["Density"].values[a]*20,
                       alpha = 0.5, color='brown', label="Pakistan")
            # USA
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=usa_df["Population"].values[a],
                       s=usa_df["Density"].values[a]*20,
                       alpha = 0.5, color='teal', label="USA")
        
        text.set_text(f"{year}")
    
    
    animate = FuncAnimation(fig, update,
                            [i for i in range(1961,2021,10)]+[2020],
                            interval=1000, repeat=False, blit=True)
        
    plt.show()


# ### b) Chosen country as a centroid

# In[194]:


df2


# In[31]:


new_dfs2 = []
for i in range(5):
    new_dfs2.append(pd.concat([df2.iloc[i]['1961':'2020'],area.loc[df2.index[i]]["1961":"2020"]],axis=1))
    new_dfs2[i].columns = ["Population", "Area"]
    new_dfs2[i]["Density"] = (new_dfs2[i]["Population"])/(new_dfs2[i]["Area"])
    new_dfs2[i] = new_dfs2[i].convert_dtypes()


# In[32]:


andora_df = new_dfs2[0]
amsamoa_df = new_dfs2[1]
farislands_df = new_dfs2[2]
marshislands_df = new_dfs2[3]
nmarislands_df = new_dfs2[4]


# In[208]:


marshislands_df


# In[236]:


with plt.style.context("ggplot"):

    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot()
    plt.ylim(0,110000)
    ax.yaxis.set_ticks(range(0,110000,20000),
                       labels = ['0','20T','40T','60T','80T','100T'])

    ax.set_title("Dynamic population of 5 chosen countries", fontsize=20)
    plt.xlim(1958,2025)
    ax.xaxis.set_ticks([i for i in range(1961,2021,10)]+[2020])
    text = ax.text(1984,90000,"",
            bbox = dict(facecolor = 'white',edgecolor="black"),
           fontsize=24, fontstyle="italic")
    
    # For the legend
    ax.scatter(x=[0],y=[0],color='red',label='Andorra')
    ax.scatter(x=[0],y=[0],color='#3ABF2B',label='American Samoa')
    ax.scatter(x=[0],y=[0],color='olive',label='Faroe Islands')
    ax.scatter(x=[0],y=[0],color='brown',label='Marshall Islands')
    ax.scatter(x=[0],y=[0],color='teal',label='North. Mar. Islands')
                    
    ax.legend(loc="upper left", fontsize=15)

    def update(year):
        
        
        if year == 2020:
            
            a = [i for i in range(0,year-1960,10)] + [len(andora_df)-1]
            
            # Andorra
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=andora_df["Population"].values[a],
                       s=andora_df["Density"].values[a]*20,
                       alpha = 0.5, color='red')
            # American Samoa
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=amsamoa_df["Population"].values[a],
                       s=amsamoa_df["Density"].values[a]*20,
                       alpha = 0.5, color='#3ABF2B')
            # Faroe Islands
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=farislands_df["Population"].values[a],
                       s=farislands_df["Density"].values[a]*20,
                       alpha = 0.5, color='olive')
            # Marshall Islands
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=marshislands_df["Population"].values[a],
                       s=marshislands_df["Density"].values[a]*20,
                       alpha = 0.5, color='brown')
            # Northern Mariana Islands
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=nmarislands_df["Population"].values[a],
                       s=nmarislands_df["Density"].values[a]*20,
                       alpha = 0.5, color='teal')
        else:
            
            a = [i for i in range(0,year-1960,10)]
            
            # Andorra
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=andora_df["Population"].values[a],
                       s=andora_df["Density"].values[a]*20,
                       alpha = 0.5, color='red')
            # American Samoa
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=amsamoa_df["Population"].values[a],
                       s=amsamoa_df["Density"].values[a]*20,
                       alpha = 0.5, color='#3ABF2B')
            # Faroe Islands
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=farislands_df["Population"].values[a],
                       s=farislands_df["Density"].values[a]*20,
                       alpha = 0.5, color='olive')
            # Marshall Islands
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=marshislands_df["Population"].values[a],
                       s=marshislands_df["Density"].values[a]*20,
                       alpha = 0.5, color='brown')
            # Northern Mariana Islands
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=nmarislands_df["Population"].values[a],
                       s=nmarislands_df["Density"].values[a]*20,
                       alpha = 0.5, color='teal')
            
        text.set_text(f"{year}")
    
    
    animate = FuncAnimation(fig, update,
                            [i for i in range(1961,2021,10)]+[2020],
                            interval=1000, repeat=False, blit=True)
        
    plt.show()


# ### c) Poland as a 'centroid'

# In[40]:


df3


# In[41]:


new_dfs3 = []
for i in range(5):
    new_dfs3.append(pd.concat([df3.iloc[i]['1961':'2020'],area.loc[df3.index[i]]["1961":"2020"]],axis=1))
    new_dfs3[i].columns = ["Population", "Area"]
    new_dfs3[i]["Density"] = (new_dfs3[i]["Population"])/(new_dfs3[i]["Area"])
    new_dfs3[i] = new_dfs3[i].convert_dtypes()


# In[42]:


arg_df = new_dfs3[0]
canada_df = new_dfs3[1]
algeria_df = new_dfs3[2]
poland_df = new_dfs3[3]
sudan_df = new_dfs3[4]


# In[43]:


arg_df


# In[337]:


with plt.style.context("fivethirtyeight"):

    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot()
    plt.ylim(0,60000000)
    ax.yaxis.set_ticks(range(0,60000000,5000000),
                       labels = ['0','5M','10M','15M','20M','25M','30M','35M','40M','45M','50M','55M'],
                      fontsize=15)

    ax.set_title('Population of 5 chosen countries (Poland as centroid)',
                 loc='left',
                 pad = 10,
                fontsize=20)
    plt.xlim(1958,2025)
    ax.xaxis.set_ticks([i for i in range(1961,2021,10)]+[2020],
                       labels=[i for i in range(1961,2021,10)]+[2020],
                       fontsize=15)
    text = ax.text(1980,50000000,"",
            bbox = dict(facecolor = 'white',edgecolor="black"),
           fontsize=24, fontstyle="italic")
    
    # For the legend
    ax.scatter(x=[0],y=[0],color='#00C4FF',label='Argentina')
    ax.scatter(x=[0],y=[0],color='#3ABF2B',label='Canada')
    ax.scatter(x=[0],y=[0],color='olive',label='Algeria')
    ax.scatter(x=[0],y=[0],color='red',label='Poland')
    ax.scatter(x=[0],y=[0],color='brown',label='Sudan')
                    
    ax.legend(loc="upper left", fontsize=15)

    def update(year):
        
        
        if year == 2020:
            
            a = [i for i in range(0,year-1960,10)] + [len(arg_df)-1]
            
            # Argentina
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=arg_df["Population"].values[a],
                       s=arg_df["Density"].values[a]*20,
                       alpha = 0.5, color='#00C4FF')
            # Canada
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=canada_df["Population"].values[a],
                       s=canada_df["Density"].values[a]*20,
                       alpha = 0.5, color='#3ABF2B')
            # Algeria
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=algeria_df["Population"].values[a],
                       s=algeria_df["Density"].values[a]*20,
                       alpha = 0.5, color='olive')
            # Poland
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=poland_df["Population"].values[a],
                       s=poland_df["Density"].values[a]*20,
                       alpha = 0.5, color='red')
            # Sudan
            ax.scatter(x=[i for i in range(1961,year+1,10)]+[2020],
                       y=sudan_df["Population"].values[a],
                       s=sudan_df["Density"].values[a]*20,
                       alpha = 0.5, color='brown')
        else:
            
            a = [i for i in range(0,year-1960,10)]
            
            # Argentina
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=arg_df["Population"].values[a],
                       s=arg_df["Density"].values[a]*20,
                       alpha = 0.5, color='#00C4FF')
            # Canada
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=canada_df["Population"].values[a],
                       s=canada_df["Density"].values[a]*20,
                       alpha = 0.5, color='#3ABF2B')
            # Algeria
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=algeria_df["Population"].values[a],
                       s=algeria_df["Density"].values[a]*20,
                       alpha = 0.5, color='olive')
            # Poland
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=poland_df["Population"].values[a],
                       s=poland_df["Density"].values[a]*20,
                       alpha = 0.5, color='red')
            # Sudan
            ax.scatter(x=[i for i in range(1961,year+1,10)],
                       y=sudan_df["Population"].values[a],
                       s=sudan_df["Density"].values[a]*20,
                       alpha = 0.5, color='brown')
            
        text.set_text(f"{year}")
    
    
    animate = FuncAnimation(fig, update,
                            [i for i in range(1961,2021,10)]+[2020],
                            interval=1000, repeat=False, blit=True)
        
    plt.show()


# ## 5. Pie charts

# The assignment is to prepare some other type of visualization for our three dataframes. Let that be pie charts (althought it's doubtful that it's a good choice in the case of our data)

# What we'll be visualizing is actually the proportion between populations of given countries, dynamically changing over years.

# ### a) Top 5 countries

# In[239]:


df


# In[44]:


with plt.style.context('fivethirtyeight'):
    
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot()
    
    wedges, labls, texts = ax.pie(df['1960'],labels=df.index,autopct='%1.1f%%',
                                   colors=['red','#3ABF2B','olive','brown','teal'],
                                   textprops=dict(fontweight="bold", fontsize=15),
                                   radius=1,
                                    labeldistance=1.1,
                                    pctdistance=0.8)
    ax.text(-1.7,0.7,"1960",fontsize=20,
            fontweight='bold',
            bbox=dict(facecolor="white",edgecolor="black"))
    ax.set_title("Top 5 populated countries (Population ratio)",
            fontsize=20)
    for i in range(5):
        texts[i].set_color("white")
    
    def update(year):
        ax.clear()
        
        wedges, labls, texts = ax.pie(df[f'{year}'],labels=df.index,autopct='%1.1f%%',
                                   colors=['red','#3ABF2B','olive','brown','teal'],
                                   textprops=dict(fontweight="bold",fontsize=15),
                                   radius=1,
                                   labeldistance=1.1,
                                    pctdistance=0.8)
        for i in range(5):
            texts[i].set_color("white")
        
        ax.text(-1.7,0.7,f"{year}",fontsize=20,
                fontweight='bold',
                bbox=dict(facecolor="white",edgecolor="black"))
        ax.set_title("Top 5 populated countries (Population ratio)",
                fontsize=20)
            
            
    animate = FuncAnimation(fig, update, range(1961,2021),repeat=False,
                           blit=True)
    plt.show()
        


# ### b) Chosen country as a 'centroid'

# In[322]:


df2


# In[343]:


with plt.style.context('fivethirtyeight'):
    
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot()
    
    wedges, labls, texts = ax.pie(df2['1960'],labels=df2.index,autopct='%1.1f%%',
                                   colors=['red','#3ABF2B','olive','brown','teal'],
                                   textprops=dict(fontweight="bold", fontsize=15),
                                   radius=1,
                                    labeldistance=1.1,
                                    pctdistance=0.7)
    ax.text(1.5,0,"1960",fontsize=20,
            fontweight='bold',
            bbox=dict(facecolor="white",edgecolor="black"))
    
    ax.set_title("5 chosen countries with a centroid (Population ratio)",
                fontsize=20)
    for i in range(5):
        texts[i].set_color("white")
    
    def update(year):
        ax.clear()
        
        wedges, labls, texts = ax.pie(df2[f'{year}'],labels=df2.index,autopct='%1.1f%%',
                                   colors=['red','#3ABF2B','olive','brown','teal'],
                                   textprops=dict(fontweight="bold",fontsize=15),
                                   radius=1,
                                   labeldistance=1.1,
                                    pctdistance=0.7)
        for i in range(5):
            texts[i].set_color("white")
        
        ax.text(1.5,0,f"{year}",fontsize=20,
                fontweight='bold',
                bbox=dict(facecolor="white",edgecolor="black"))
        ax.set_title("5 chosen countries with a centroid (Population ratio)",
                    fontsize=20)
                
            
    animate = FuncAnimation(fig, update, range(1961,2021),repeat=False,
                           blit=True)
    plt.show()
        


# ### c) Poland as a centroid

# In[344]:


df3


# In[ ]:


with plt.style.context('fivethirtyeight'):
    
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot()
    
    wedges, labls, texts = ax.pie(df3['1960'],labels=df3.index,autopct='%1.1f%%',
                                   colors=['#00C4FF','#FF976C','olive','#BC0000','#4A271E'],
                                   textprops=dict(fontweight="bold", fontsize=15),
                                   radius=1,
                                    labeldistance=1.1,
                                    pctdistance=0.7)
    ax.text(1.5,0,"1960",fontsize=20,
            fontweight='bold',
            bbox=dict(facecolor="white",edgecolor="black"))
    
    ax.set_title("5 chosen countries with a Poland as a centroid \n (Population ratio)",
                fontsize=20)
    for i in range(5):
        texts[i].set_color("white")
    
    
    def update(year):
        ax.clear()
        
        wedges, labls, texts = ax.pie(df3[f'{year}'],labels=df3.index,autopct='%1.1f%%',
                                   colors=['#00C4FF','#FF976C','olive','#BC0000','#4A271E'],
                                   textprops=dict(fontweight="bold",fontsize=15),
                                   radius=1,
                                   labeldistance=1.1,
                                    pctdistance=0.7)
        for i in range(5):
            texts[i].set_color("white")
        
        ax.text(1.5,0,f"{year}",fontsize=20,
                fontweight='bold',
                bbox=dict(facecolor="white",edgecolor="black"))
        ax.set_title("5 chosen countries with a Poland as a centroid \n (Population ratio)",
                    fontsize=20)
                
            
    animate = FuncAnimation(fig, update, range(1961,2021),repeat=False,
                           blit=True)
    plt.show()
        


# ## 6. Plot showing some 'strange' behavior

# There was a horrible period in modern history of Cambodia. After years of Vietnamese war and proclaiming and American-friendly government, in 1975 Cambodia underwent a coup- the power was taken by communist extremist Pot Pot and his Khmer Rouge army. 
# 
# The new regime modelled itself on Maoist China during the Great Leap Forward, immediately evacuated the cities, and sent the entire population on forced marches to rural work projects. They attempted to rebuild the country's agriculture on the model of the 11th century, discarded Western medicine, and destroyed temples, libraries, and anything considered Western.
# 
# Estimates as to how many people were killed by the Khmer Rouge regime range from approximately one to three million. The most commonly cited figure is two million (about a quarter of the population).This era gave rise to the term Killing Fields, and the prison Tuol Sleng became notorious for its history of mass killing. Hundreds of thousands fled across the border into neighbouring Thailand. The regime disproportionately targeted ethnic minority groups. The Cham Muslims suffered serious purges with as much as half of their population exterminated. Pol Pot was determined to keep his power and disenfranchise any enemies or potential threats, and thus increased his violent and aggressive actions against his people.
# 
# The regime period ended in 1978 with an invasion of Vietnamese forces. Pot Pot fled deep into the jungle, where he allegedlly died in 1998, surrounded by his followers.

# In[45]:


df_camb = countries.drop(labels = countries.columns[-1], axis = 1)


# In[46]:


df_camb.loc["Cambodia"]


# In[47]:


df_camb['absolute_1974'] = abs(df_camb['1974']-df_camb.loc["Cambodia"]['1974'])


# In[48]:


df_camb['absolute_2021'] = abs(df_camb['2021']-df_camb.loc["Cambodia"]['2021'])


# In[49]:


df_camb


# In[50]:


df4 =  df_camb.sort_values(by = ['absolute_2021','absolute_1974']).head(5)


# In[51]:


df4


# First, let's take a quick look at Cambodia's population dynamic. There, we can easly see the horrific doings of the Khmer Rouge's regime.

# In[16]:


with plt.style.context('dark_background'): 
    fig = plt.figure(figsize=(7,6))
    ax = fig.add_subplot()
    plt.ylim(0,19000000)
    ax.yaxis.set_ticks(range(0,19000000,3000000),
                       labels=['0','3M','6M','9M','12M','15M','18M'])

    cambodia_line, = ax.plot(range(1960,2022),df4.loc["Cambodia"]['1960':'2021'],
                            color="red", linewidth = 3, label="Cambodia")
    regime_line, = ax.plot([1975 for i in range(1000000,18000000)],
                           range(1000000,18000000),
                          color="white",
                          linestyle="--",
                          label="Pot Pot's coup")
    ax.legend(loc="upper left")
    
    
    ax.set_title("Cambodian population 1960-2021", fontsize=20)

    plt.show()


# We will now compare the population decline to some other countries. Let's focus only on the period up to year 2000- what's happened then is not that important for this analysis.
# Note that something strange happened also in Somalia, in the early 90s. That's actually a break of a devastating civil war, which still goes on as of the year 2023.

# In[52]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[53]:


with plt.style.context('dark_background'):
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot()
    plt.ylim(0,16000000)
    ax.yaxis.set_ticks(range(0,16000000,3000000),
                       labels=['0','3M','6M','9M','12M','15M'],
                      fontsize=14)
    
    ax.set_title("Dynamic change of Cambodian population \n (four countries for refference)",
                fontsize=20)
    year_text = ax.text(1.2,14000000,"Year:", fontsize=20, fontweight="bold")
    year_counter = ax.text(2,14000000,"1960", fontsize=20, fontweight="bold",
                          bbox = dict(facecolor="black",edgecolor="w"))
    
    
    bars = ax.bar(df4.index, df4['1960'],
                  color =['#A00000','#CD4F4F','#CD4F4F','#CD4F4F','#CD4F4F'])
    
    line, = ax.plot([],
                   linestyle="--",
                   linewidth = 4,
                   color = "w")
    text = ax.text(0.5,df4.loc['Cambodia']['1975']+330000,
                  "", fontsize=20, fontweight="bold")
    
    def update(year):
        
        if year in range(1976,1986):
            line.set_xdata(range(5))
            line.set_ydata([df4.loc['Cambodia']['1975']+80000 for i in range(5)])
            text.set_text("Pot Pot's coup")
            return line,
        if year >= 1986: # the actual year is 1976, 1977, 1978...
            if year == 1988:
                line.set_xdata([])
                line.set_ydata([])
                text.set_text("")
            for i in range(5):
                bars[i].set_height(df4.iloc[i][f'{year-10}'])
            
            year_counter.set_text(f"{year-10}")
            return bars
            

        
        for i in range(5):
            bars[i].set_height(df4.iloc[i][f'{year}'])
            
        year_counter.set_text(f"{year}")
        return bars
        
    
    animate = FuncAnimation(fig, update, range(1960,2011),
                           repeat=False, interval=500, blit=True)
    
    plt.show()
    


# ## 7. aGantt plot

# Gantt plot will be of use to prepare a kind of scheduled 'activities' taking place over time. In this case, we will make a schedule for the 2022/23 academical year at the University of Warsaw

# In[54]:


acad_year = pd.date_range('2023-09-1','2024-10-10')


# In[187]:


with plt.style.context('seaborn-v0_8-whitegrid'):
    
    fig = plt.figure(figsize=(29.7,21.0))
    ax = fig.add_subplot()
    plt.ylim(0,6)
    ax.yaxis.set_ticks([1,2,3,4,5],
                       labels=['Language\nexams','Classes,\nExams','Holidays','Formality\nperiods','Semester'],
                      fontsize=30,
                      fontweight="demibold")
    fig.autofmt_xdate()
    ax.set_xlim(acad_year[0],acad_year[-1])
    ax.xaxis.set_ticks(acad_year[::30].date,
                       labels=acad_year[::30].date,
                      fontsize=15,
                      fontweight="demibold")
    ax.set_title("Academic year 2024/24- schedule",
                 fontsize=40, fontweight="bold")
    
    # Exams
    ax.broken_barh([(pd.to_datetime('2024-01-29'),pd.to_datetime('2024-02-11')-pd.to_datetime('2024-01-29')),
                    (pd.to_datetime('2024-02-19'),pd.to_datetime('2024-02-25')-pd.to_datetime('2024-02-19')),
                   (pd.to_datetime('2024-06-17'),pd.to_datetime('2024-07-07')-pd.to_datetime('2024-06-17')),
                   (pd.to_datetime('2024-09-02'),pd.to_datetime('2024-09-15')-pd.to_datetime('2024-09-02'))],
                   (1.7,0.5),alpha=0.7,color="red")
    ax.text(pd.to_datetime('2024-02-1'),1.3,"egzaminacyjna\nsesja zimowa",
           ha="center", color="red",rotation=26,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-02-22'),1.2,"egzaminacyjna\nsesja poprawkowa\nsemestru zimowego",
           ha="center", color="red",rotation=26,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-06-29'),1.3,"egzaminacyjna\nsesja letnia",
           ha="center", color="red",rotation=26,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-09-07'),1.2,"egzaminacyjna\nsesja poprawkowa\nsemestru letniego",
           ha="center", color="red",rotation=26,
           fontsize=13,fontweight="semibold")

    # Classes
    ax.broken_barh([(pd.to_datetime('2023-10-2'),pd.to_datetime('2023-10-29')-pd.to_datetime('2023-10-2')),
                   (pd.to_datetime('2023-10-30'),pd.to_datetime('2023-12-03')-pd.to_datetime('2023-10-30')),
                   (pd.to_datetime("2023-12-04"),pd.to_datetime('2023-12-21')-pd.to_datetime('2023-12-04')),
                   (pd.to_datetime('2024-01-08'),pd.to_datetime('2024-01-28')-pd.to_datetime('2024-01-08')),
                   (pd.to_datetime('2024-02-26'),pd.to_datetime('2024-03-17')-pd.to_datetime('2024-02-26')),
                   (pd.to_datetime('2024-03-18'),pd.to_datetime('2024-04-28')-pd.to_datetime('2024-03-18')),
                   (pd.to_datetime('2024-04-29'),pd.to_datetime('2024-06-16')-pd.to_datetime('2024-04-29'))],
                   (1.7,0.5),alpha=0.7, color="#0094FF")
    ax.text(pd.to_datetime('2023-10-15'),2.3,"zajęcia\ndydaktyczne\n(blok I)",
            ha="center",color="#0094FF",
           fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2023-11-14'),2.3,"zajęcia\ndydaktyczne\n(blok II)",
            ha='center',color='#0094FF',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2023-12-14'),2.3,"zajęcia\ndydaktyczne\n(blok III)",
            ha='center',color='#0094FF',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-01-18'),2.3,"zajęcia\ndydaktyczne\n(blok III cd)",
            ha='center',color='#0094FF',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-03-06'),2.3,"zajęcia\ndydaktyczne\n(blok I)",
            ha='center',color='#0094FF',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-04-09'),2.3,"zajęcia\ndydaktyczne\n(blok II)",
            ha='center',color='#0094FF',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-22'),2.3,"zajęcia\ndydaktyczne\n(blok III)",
            ha='center',color='#0094FF',
            fontsize=14,fontweight="semibold")
    
    # Semester
    ax.broken_barh([(pd.to_datetime('2023-10-01'),pd.to_datetime('2024-02-18')-pd.to_datetime('2023-10-01')),
                   (pd.to_datetime('2024-02-19'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-02-19'))],
                  (4.7,0.5),alpha=0.9,color='#BAA1D5')
    ax.text(pd.to_datetime('2023-12-14'),5.3,"SEMESTR ZIMOWY",
           fontweight="bold",ha="center",color="#BAA1D5",
           fontsize=20)
    ax.text(pd.to_datetime('2024-06-08'),5.3,"SEMESTR LETNI",
           fontweight="bold",ha="center",color="#BAA1D5",
           fontsize=20)
    # Holidays
    ax.broken_barh([(pd.to_datetime('2023-12-22'),pd.to_datetime('2024-01-07')-pd.to_datetime('2023-12-22')),
                   (pd.to_datetime('2024-02-12'),pd.to_datetime('2024-02-18')-pd.to_datetime('2024-02-12')),
                   (pd.to_datetime('2024-03-28'),pd.to_datetime('2024-04-02')-pd.to_datetime('2024-03-28')),
                   (pd.to_datetime('2024-05-10'),pd.to_datetime('2024-05-11')-pd.to_datetime('2024-05-10')),
                   (pd.to_datetime('2024-05-31'),pd.to_datetime('2024-06-02')-pd.to_datetime('2024-05-31')),
                   (pd.to_datetime('2024-07-08'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-07-08'))],
                  (2.7,0.5),alpha=0.7,color="#E8A900")
    ax.plot([pd.to_datetime('2024-05-02'), pd.to_datetime('2024-05-02')],
           [2.7,3.2], linewidth=4, color='#E8A900')
    ax.text(pd.to_datetime('2023-12-30'),3.3,"Wakacje zimowe",
           ha="center",color="#E8A900",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-02-15'),3.3,"Przerwa\nmiędzysemestralna",
           ha="center",color="#E8A900",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-03-30'),3.3,"Wakacje wiosenne",
           ha="center",color="#E8A900",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-02'),3.3,"Dzień\nflagi\n2.05",
           ha="center",color="#E8A900",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-16'),3.3,"Juwenalia",
           ha="center",color="#E8A900",rotation=28,
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-06-01'),3.3,"Boże Ciało",
           ha="center",color="#E8A900",rotation=28,
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-08-12'),3.3,"Wakacje letnie",
           ha="center",color="#E8A900",
            fontsize=14,fontweight="semibold")
    
    # Language exams
    ax.broken_barh([(pd.to_datetime('2024-01-29'),pd.to_datetime('2024-01-30')-pd.to_datetime('2024-01-29')),
                   (pd.to_datetime('2024-06-17'),pd.to_datetime('2024-06-18')-pd.to_datetime('2024-06-17')),
                   (pd.to_datetime('2024-09-02'),pd.to_datetime('2024-09-03')-pd.to_datetime('2024-09-02'))],
                  (0.7,0.5),color='#FF00AB', alpha=0.8)
    ax.plot([pd.to_datetime('2024-02-24'),pd.to_datetime('2024-02-24')],
           [0.7,1.2],color="#FF00AB",linewidth=4)
    ax.text(pd.to_datetime('2024-01-20'),0.22,"pisemne egzaminy\ncertyfikacyjne z\njęzyków obcych",
           ha="center",color="#FF00AB",rotation=20,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-02-24'),0.2,"pisemne egzaminy\ncertyfikacyjne z\njęzyka angielskiego\nna poziomie B2",
           ha="center",color="#FF00AB",rotation=20,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-06-17'),0.25,"pisemne egzaminy\ncertyfikacyjne z\njęzyków obcych",
           ha="center",color="#FF00AB",rotation=20,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-09-02'),0.25,"pisemne egzaminy\ncertyfikacyjne z\njęzyków obcych",
           ha="center",color="#FF00AB",rotation=20,
           fontsize=13,fontweight="semibold")
    
    # Formalities
    ax.broken_barh([(pd.to_datetime('2023-10-01'),pd.to_datetime('2024-02-18')-pd.to_datetime('2023-10-01')),
                   (pd.to_datetime('2024-03-04'),pd.to_datetime('2024-03-31')-pd.to_datetime('2024-03-04')),
                   (pd.to_datetime('2024-06-01'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-06-01'))],
                  (3.7,0.5), alpha=0.9, color='#009A92')
    ax.broken_barh([(pd.to_datetime('2024-09-16'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-09-16'))],
                  (3.9,0.5),alpha=0.7,color='#009A92')
    
    ax.plot([pd.to_datetime('2023-10-20'),pd.to_datetime('2023-10-20')],
           [0.1,5.6],color="#009A92",
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2023-10-20'),5.7,
           "ostateczny termin składania wniosku o usunięcie\npodpięcia przedmiotu pod program studiów",
           fontsize=13,fontweight="semibold",color="#009A92")
    
    ax.plot([pd.to_datetime('2024-01-19'),pd.to_datetime('2024-01-19')],
           [0.1,5.6],color="#009A92",
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2024-01-19'),5.65,
           "ostateczny termin rezygnacji\nz zaliczenia przedmiotu\nw semestrze zimowym",
           fontsize=13,fontweight="semibold",color="#009A92")
    
    ax.plot([pd.to_datetime('2024-03-15'),pd.to_datetime('2024-03-15')],
           [0.1,5.6],color="#009A92",
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2024-03-15'),5.65,
           "ostateczny termin składania wniosku\no usunięcie podpięcia przedmiotu\npod program studiów",
           fontsize=13,fontweight="semibold",color="#009A92")
    
    ax.plot([pd.to_datetime('2024-06-01'),pd.to_datetime('2024-06-01')],
           [0.1,5.6],color='#009A92',
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2024-06-01'),5.65,
           "ostateczny termin rezygnacji\nz zaliczenia przedmiotu\nw semestrze letnim ",
           fontsize=13,fontweight="semibold",color="#009A92")
    
    
    ax.text(pd.to_datetime('2023-12-14'),4.3,
            "okres dokonywania podpięć przedmiotów realizowanych\nw semestrze letnim roku akademickiego 2023/2024",
           ha="center",color="#009A92",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-03-03'),4.3,
            "okres, w którym należy podjąć wszystkie\nindywidualne decyzje dotyczące\nzaliczenia semestru zimowego 2023/2024",
           ha="left",color="#009A92",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-04-01'),3.8,
            "(dotyczy kierunków studiów,\ndla których planowany\ntermin ich zakończenia przypada\nna koniec semestru zimowego)",
           ha="left",color="#009A92",
            fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-25'),4.25,
            "okres dokonywania podpięć przedmiotów realizowanych\nw semestrze zimowym i całym roku akademickim 2024/2025",
           ha="left",color="#009A92",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-09-19'),4.45,
           "okres, w którym należy podjąć wszystkie\nindywidualne decyzje dotyczące\nzaliczenia roku akademickiego 2023/2024",
           ha="center",color="#009A92",
            fontsize=14,fontweight="semibold")
    plt.savefig("gatt_schedule_color.pdf",format="pdf")
    


# And as for the black&white version:

# In[185]:


with plt.style.context('seaborn-v0_8-whitegrid'):
    
    fig = plt.figure(figsize=(29.7,21.0))
    ax = fig.add_subplot()
    plt.ylim(0,6)
    ax.yaxis.set_ticks([1,2,3,4,5],
                       labels=['Language\nexams','Classes,\nExams','Holidays','Formality\nperiods','Semester'],
                      fontsize=30,
                      fontweight="demibold")
    fig.autofmt_xdate()
    ax.set_xlim(acad_year[0],acad_year[-1])
    ax.xaxis.set_ticks(acad_year[::30].date,
                       labels=acad_year[::30].date,
                      fontsize=15,
                      fontweight="demibold")
    ax.set_title("Academic year 2024/24- schedule",
                 fontsize=40, fontweight="bold")
    
    # Exams
    ax.broken_barh([(pd.to_datetime('2024-01-29'),pd.to_datetime('2024-02-11')-pd.to_datetime('2024-01-29')),
                    (pd.to_datetime('2024-02-19'),pd.to_datetime('2024-02-25')-pd.to_datetime('2024-02-19')),
                   (pd.to_datetime('2024-06-17'),pd.to_datetime('2024-07-07')-pd.to_datetime('2024-06-17')),
                   (pd.to_datetime('2024-09-02'),pd.to_datetime('2024-09-15')-pd.to_datetime('2024-09-02'))],
                   (1.7,0.5),alpha=0.7,color="black")
    ax.text(pd.to_datetime('2024-02-1'),1.3,"egzaminacyjna\nsesja zimowa",
           ha="center", color="black",rotation=26,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-02-22'),1.2,"egzaminacyjna\nsesja poprawkowa\nsemestru zimowego",
           ha="center", color="black",rotation=26,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-06-29'),1.3,"egzaminacyjna\nsesja letnia",
           ha="center", color="black",rotation=26,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-09-07'),1.2,"egzaminacyjna\nsesja poprawkowa\nsemestru letniego",
           ha="center", color="black",rotation=26,
           fontsize=13,fontweight="semibold")

    # Classes
    ax.broken_barh([(pd.to_datetime('2023-10-2'),pd.to_datetime('2023-10-29')-pd.to_datetime('2023-10-2')),
                   (pd.to_datetime('2023-10-30'),pd.to_datetime('2023-12-03')-pd.to_datetime('2023-10-30')),
                   (pd.to_datetime("2023-12-04"),pd.to_datetime('2023-12-21')-pd.to_datetime('2023-12-04')),
                   (pd.to_datetime('2024-01-08'),pd.to_datetime('2024-01-28')-pd.to_datetime('2024-01-08')),
                   (pd.to_datetime('2024-02-26'),pd.to_datetime('2024-03-17')-pd.to_datetime('2024-02-26')),
                   (pd.to_datetime('2024-03-18'),pd.to_datetime('2024-04-28')-pd.to_datetime('2024-03-18')),
                   (pd.to_datetime('2024-04-29'),pd.to_datetime('2024-06-16')-pd.to_datetime('2024-04-29'))],
                   (1.7,0.5),alpha=0.7, color="black")
    ax.text(pd.to_datetime('2023-10-15'),2.3,"zajęcia\ndydaktyczne\n(blok I)",
            ha="center",color="black",
           fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2023-11-14'),2.3,"zajęcia\ndydaktyczne\n(blok II)",
            ha='center',color='black',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2023-12-14'),2.3,"zajęcia\ndydaktyczne\n(blok III)",
            ha='center',color='black',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-01-18'),2.3,"zajęcia\ndydaktyczne\n(blok III cd)",
            ha='center',color='black',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-03-06'),2.3,"zajęcia\ndydaktyczne\n(blok I)",
            ha='center',color='black',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-04-09'),2.3,"zajęcia\ndydaktyczne\n(blok II)",
            ha='center',color='black',
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-22'),2.3,"zajęcia\ndydaktyczne\n(blok III)",
            ha='center',color='black',
            fontsize=14,fontweight="semibold")
    
    # Semester
    ax.broken_barh([(pd.to_datetime('2023-10-01'),pd.to_datetime('2024-02-18')-pd.to_datetime('2023-10-01')),
                   (pd.to_datetime('2024-02-19'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-02-19'))],
                  (4.7,0.5),alpha=0.9,color='black')
    ax.text(pd.to_datetime('2023-12-14'),5.3,"SEMESTR ZIMOWY",
           fontweight="bold",ha="center",color="black",
           fontsize=20)
    ax.text(pd.to_datetime('2024-06-08'),5.3,"SEMESTR LETNI",
           fontweight="bold",ha="center",color="black",
           fontsize=20)
    # Holidays
    ax.broken_barh([(pd.to_datetime('2023-12-22'),pd.to_datetime('2024-01-07')-pd.to_datetime('2023-12-22')),
                   (pd.to_datetime('2024-02-12'),pd.to_datetime('2024-02-18')-pd.to_datetime('2024-02-12')),
                   (pd.to_datetime('2024-03-28'),pd.to_datetime('2024-04-02')-pd.to_datetime('2024-03-28')),
                   (pd.to_datetime('2024-05-10'),pd.to_datetime('2024-05-11')-pd.to_datetime('2024-05-10')),
                   (pd.to_datetime('2024-05-31'),pd.to_datetime('2024-06-02')-pd.to_datetime('2024-05-31')),
                   (pd.to_datetime('2024-07-08'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-07-08'))],
                  (2.7,0.5),alpha=0.7,color="black")
    ax.plot([pd.to_datetime('2024-05-02'), pd.to_datetime('2024-05-02')],
           [2.7,3.2], linewidth=4, color='black')
    ax.text(pd.to_datetime('2023-12-30'),3.3,"Wakacje zimowe",
           ha="center",color="black",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-02-15'),3.3,"Przerwa\nmiędzysemestralna",
           ha="center",color="black",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-03-30'),3.3,"Wakacje wiosenne",
           ha="center",color="black",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-02'),3.3,"Dzień\nflagi\n2.05",
           ha="center",color="black",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-16'),3.3,"Juwenalia",
           ha="center",color="black",rotation=28,
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-06-01'),3.3,"Boże Ciało",
           ha="center",color="black",rotation=28,
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-08-12'),3.3,"Wakacje letnie",
           ha="center",color="black",
            fontsize=14,fontweight="semibold")
    
    # Language exams
    ax.broken_barh([(pd.to_datetime('2024-01-29'),pd.to_datetime('2024-01-30')-pd.to_datetime('2024-01-29')),
                   (pd.to_datetime('2024-06-17'),pd.to_datetime('2024-06-18')-pd.to_datetime('2024-06-17')),
                   (pd.to_datetime('2024-09-02'),pd.to_datetime('2024-09-03')-pd.to_datetime('2024-09-02'))],
                  (0.7,0.5),color='black', alpha=0.8)
    ax.plot([pd.to_datetime('2024-02-24'),pd.to_datetime('2024-02-24')],
           [0.7,1.2],color="black",linewidth=4)
    ax.text(pd.to_datetime('2024-01-20'),0.22,"pisemne egzaminy\ncertyfikacyjne z\njęzyków obcych",
           ha="center",color="black",rotation=20,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-02-24'),0.2,"pisemne egzaminy\ncertyfikacyjne z\njęzyka angielskiego\nna poziomie B2",
           ha="center",color="black",rotation=20,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-06-17'),0.25,"pisemne egzaminy\ncertyfikacyjne z\njęzyków obcych",
           ha="center",color="black",rotation=20,
           fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-09-02'),0.25,"pisemne egzaminy\ncertyfikacyjne z\njęzyków obcych",
           ha="center",color="black",rotation=20,
           fontsize=13,fontweight="semibold")
    
    # Formalities
    ax.broken_barh([(pd.to_datetime('2023-10-01'),pd.to_datetime('2024-02-18')-pd.to_datetime('2023-10-01')),
                   (pd.to_datetime('2024-03-04'),pd.to_datetime('2024-03-31')-pd.to_datetime('2024-03-04')),
                   (pd.to_datetime('2024-06-01'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-06-01'))],
                  (3.7,0.5), alpha=0.9, color='black')
    ax.broken_barh([(pd.to_datetime('2024-09-16'),pd.to_datetime('2024-09-30')-pd.to_datetime('2024-09-16'))],
                  (3.9,0.5),alpha=0.7,color='black')
    
    ax.plot([pd.to_datetime('2023-10-20'),pd.to_datetime('2023-10-20')],
           [0.1,5.6],color="black",
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2023-10-20'),5.7,
           "ostateczny termin składania wniosku o usunięcie\npodpięcia przedmiotu pod program studiów",
           fontsize=13,fontweight="semibold")
    
    ax.plot([pd.to_datetime('2024-01-19'),pd.to_datetime('2024-01-19')],
           [0.1,5.6],color="black",
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2024-01-19'),5.65,
           "ostateczny termin rezygnacji\nz zaliczenia przedmiotu\nw semestrze zimowym",
           fontsize=13,fontweight="semibold")
    
    ax.plot([pd.to_datetime('2024-03-15'),pd.to_datetime('2024-03-15')],
           [0.1,5.6],color="black",
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2024-03-15'),5.65,
           "ostateczny termin składania wniosku\no usunięcie podpięcia przedmiotu\npod program studiów",
           fontsize=13,fontweight="semibold")
    
    ax.plot([pd.to_datetime('2024-06-01'),pd.to_datetime('2024-06-01')],
           [0.1,5.6],color="black",
           linewidth=3,linestyle="--")
    ax.text(pd.to_datetime('2024-06-01'),5.65,
           "ostateczny termin rezygnacji\nz zaliczenia przedmiotu\nw semestrze letnim ",
           fontsize=13,fontweight="semibold")
    
    ax.text(pd.to_datetime('2023-12-14'),4.3,
            "okres dokonywania podpięć przedmiotów realizowanych\nw semestrze letnim roku akademickiego 2023/2024",
           ha="center",color="black",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-03-03'),4.3,
            "okres, w którym należy podjąć wszystkie\nindywidualne decyzje dotyczące\nzaliczenia semestru zimowego 2023/2024",
           ha="left",color="black",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-04-01'),3.8,
            "(dotyczy kierunków studiów,\ndla których planowany\ntermin ich zakończenia przypada\nna koniec semestru zimowego)",
           ha="left",color="black",
            fontsize=13,fontweight="semibold")
    ax.text(pd.to_datetime('2024-05-25'),4.25,
            "okres dokonywania podpięć przedmiotów realizowanych\nw semestrze zimowym i całym roku akademickim 2024/2025",
           ha="left",color="black",
            fontsize=14,fontweight="semibold")
    ax.text(pd.to_datetime('2024-09-19'),4.45,
           "okres, w którym należy podjąć wszystkie\nindywidualne decyzje dotyczące\nzaliczenia roku akademickiego 2023/2024",
           ha="center",color="black",
            fontsize=14,fontweight="semibold")
    plt.savefig("gatt_schedule_b&w.pdf",format="pdf")
    


# In[ ]:




