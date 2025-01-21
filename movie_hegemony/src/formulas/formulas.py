import argparse
import pandas as pd
import os


def group_to_count(df):
    print("\tGrouping by title ID")
    print("")
    df = df.groupby(by = "titleId").aggregate("count").reset_index()

    return df[["titleId","title"]]

def title_to_country(df):

    print("Linking titles to countries...")
    print("\n")

    # Prepare new, actually useful dataframe (a dictionary for now)
    new_df = {"tconst":[],
              "title":[],
              "country":[]}
    
    grouped_df = group_to_count(df)
    multi = 0
    skipped = 0
    count = 0
    lenght = grouped_df.shape[0]

    # Here I presuppose that the titleIds remained sorted the same way as in the original df
    i = 0
    for titleID, n in grouped_df.values:

        country = []
        # print("\tGrabbig a title...")
        title = df.iloc[i]["title"]
        # print(f"\t\tCluster of {n} titles")

        # print("\tLooking for countries...")
        for j in range(n-1):

            candidate = df.iloc[i+j+1]["region"]
            # print(f"\t\tCurrent: {candidate}")
            
            if candidate != r"\N":
                # print("\t\tAccepted!")
                country.append(candidate)
        # print("\tCountries added for the title")
        # In next iteration jump straight to the next 'cluster'
        i += n
        count += 1

        # Note the ambiguous and empty countries
        if len(country) > 1:
            multi += 1
            country = country[0] # take the first one
        else: # when the country was not provided
            skipped += 1
            continue # we dont want in it the data

        # print("\tAppending the dictionary...")
        new_df["tconst"].append(titleID)
        new_df["title"].append(title)
        new_df["country"].append(country)


        print(f"\t{count} titles handled. Progess:          {round(count*100/lenght, 4)}%",end="\r")

    print(f"There are {multi} ambiguous title-country links. In such cases, the first country that showed up was treated as the owner country")
    print(f"The number {skipped} of the titles were excluded due to the lack of a country provided.")
    print("\n")
    
    return pd.DataFrame(new_df)

    print(f"There are {multi} ambiguous title-country links. In such cases, the first country that showed up was treated as the owner country")
    print(f"The number {skipped} of the titles were excluded due to the lack of a country provided.")
    print("\n")
    
    return pd.DataFrame(new_df)

def load_data(folder_path,calculate):

    print("Loading data...")
    print("\n")

    # Initialize a list to store DataFrames
    dataframes = []
    
    # Loop through the files in the provided folder path
    for filename in os.listdir(folder_path):

        if filename.endswith('.tsv'):

            # We will only use title.basics, title.crew and title.ratings and title.akas
            if filename in ["title.episode.tsv","title.principals.tsv", "name.basics.tsv"]:
                print("File skipped")
                continue

            file_path = os.path.join(folder_path, filename)
            # Create a DataFrame from the TSV file

            # Unfortunately, I don't see a explicit 'country' field

            if filename == "title.akas.tsv":
                if calculate == "n":
                    df = pd.read_csv(os.path.join(folder_path, "title_countries.csv"))
                else:   
                    df = pd.read_csv(file_path, sep='\t', usecols=["titleId","title","region","isOriginalTitle"])
                    df = title_to_country(df)
            else:
                df = pd.read_csv(file_path, sep='\t')

            dataframes.append(df)
            print(f'Loaded: {filename} with {df.shape[0]} rows and {df.shape[1]} columns.')
    
    return dataframes

def load_add_data(folder_path):

    print("Loading data...")
    print("\n")

    # Initialize a list to store DataFrames
    add_data = {}
    
    # Loop through the files in the provided folder path
    for filename in os.listdir(folder_path):

        if filename.endswith(".csv"):
            if filename == "title_countries.csv": continue
            file_path = os.path.join(folder_path, filename)
            # Create a DataFrame from the CSV file
            if filename in ["countries_GDP.csv","countries_population.csv"]:
                df = pd.read_csv(file_path, skiprows=4)
            else:
                df = pd.read_csv(file_path)
            add_data[filename] = df
            print(f'Loaded: {filename} with {df.shape[0]} rows and {df.shape[1]} columns.')
    
    return add_data

def clean_data(dataframes):

    print("Cleaning data...")
    print("\n")

    cleaned_dataframes = []
    
    for df in dataframes:
        # Drop rows with any null values
        cleaned_df = df.dropna()
        
        # Store the cleaned DataFrame back into the dictionary
        cleaned_dataframes.append(cleaned_df)
    
    return cleaned_dataframes

def merge_data(dataframes):

    print("Merging dataframes...\n")
    print("\n")

    df = pd.merge(dataframes[0], dataframes[1], on='tconst', how='inner')

    for i in range(len(dataframes)-2):
        df = pd.merge(df, dataframes[i+2], on='tconst', how='inner')

    return df


def country_mapping(df,abr):
    
    result = df[df["Alpha-2 code"]==abr]

    result1 = result["Alpha-3 code"]
    result2 = result["English short name lower case"]

    if len(result1) == 0 or len(result2) == 0: return r"\N"+"|"+r"\N"
    else: return f"{result1.values[0]}|{result2.values[0]}"


def post_clean(df,add_data):

    print("Getting rid of several columns... empty rows...")
    print("\n")

    # Drop columns that won't be used anyway
    df = df.drop(["titleType","originalTitle","endYear","writers"],axis=1)

    print("Adding new columns...")
    # Add the "country_name" column based on the abbreviations from the "country" column

    df["country_name"] = df["country"].apply(lambda x: country_mapping(add_data["countries_df.csv"],x))
    df[["country_code","country_name"]] = df["country_name"].str.split('|', expand=True)

    print("Getting rid of several empty rows...")

    # Calculate the difference
    difference = list(set(df["country_code"]) - set(add_data["countries_GDP.csv"]["Country Code"]))

    # Drop rows where 'country_code' is in the difference list
    df = df[~df["country_code"].isin(difference)]

    # Now drop rows with at least one "\N"
    to_drop = df[df.isin([r"\N"]).any(axis=1)].index.tolist()

    df = df.drop(index=to_drop)

    # Change dtypes

    df = df.convert_dtypes()
    df["startYear"] = pd.to_numeric(df["startYear"]) # python fails to consider "1960" a possible int

    return df

def filter_data(df, start_year=None, end_year=None):

    """
    Filter the DataFrame according to provided year range.

    Parameters:
    df: pd.DataFrame - DataFrame containing a column 'startYear'
    start_year: int - Optional start year for filtering
    end_year: int - Optional end year for filtering

    Returns:
    pd.DataFrame - Filtered DataFrame

    Examples:
    >>> data = {'startYear': [2000, 2005, 2010, 2015, 2020]}
    >>> df = pd.DataFrame(data)
    >>> filtered_df = filter_data(df, start_year=2005, end_year=2015)
    >>> filtered_df['startYear'].tolist()
    [2005, 2010, 2015]

    >>> filtered_df = filter_data(df, start_year=1995, end_year=None)
    >>> filtered_df['startYear'].tolist()
    [2000, 2005, 2010, 2015, 2020]
    
    >>> filtered_df = filter_data(df, start_year=2015, end_year=2025)
    >>> filtered_df['startYear'].tolist()
    [2015, 2020]

    >>> filtered_df = filter_data(df, start_year=2025, end_year=2030)
    >>> filtered_df['startYear'].tolist()
    []
    
    >>> filtered_df = filter_data(df, start_year=2005, end_year=2003)
    >>> filtered_df['startYear'].tolist()
    []
    """
        
    print("Filtering data according to provided year range...")
    print("\n")

    # Determine minimum and maximum values from the DataFrame
    min_year = min(df["startYear"])
    max_year = max(df["startYear"])

    # Handle start_year
    if start_year is None:
        start_year = min_year
    elif start_year < min_year or start_year > max_year:
        print(f"Provided start_year {start_year} is out of bounds.")
        print(f"The minimum value you can provide is {min_year} and the maximum is {max_year}.")

        # Input loop for valid start_year
        while True:
            try:
                start_year = int(input(f"Please enter a new start_year (between {min_year} and {max_year}): "))
                if start_year < min_year or start_year > max_year:
                    print(f"Invalid year. Must be between {min_year} and {max_year}.")
                else:
                    break  # Break if valid
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    # Handle end_year
    if end_year is None:
        end_year = max_year
    elif end_year < min_year or end_year > max_year:
        print(f"Provided end_year {end_year} is out of bounds.")
        print(f"The minimum value you can provide is {min_year} and the maximum is {max_year}.")

        # Input loop for valid end_year
        while True:
            try:
                end_year = int(input(f"Please enter a new end_year (between {max(min_year,start_year)} and {max_year}): "))
                if end_year < max(min_year, start_year) or end_year > max_year:
                    print(f"Invalid year. Must be between {max(min_year, start_year)} and {max_year}.")
                else:
                    break  # Break if valid
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    # Create the filter mask
    mask = (df["startYear"] >= start_year) & (df["startYear"] <= end_year)
    df = df[mask]

    # Check if the filtered DataFrame is empty
    if df.shape[0] == 0:
        print("Data for the provided year range turned out to be empty.")
        print("Please enter new year values.")

        # Input new start_year
        while True:
            try:
                start_year = int(input(f"Please enter a new start_year (between {min_year} and {max_year}): "))
                if start_year < min_year or start_year > max_year:
                    print(f"Invalid year. Must be between {min_year} and {max_year}.")
                else:
                    break  # Valid input
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        # Input new end_year
        while True:
            try:
                end_year = int(input(f"Please enter a new end_year (between {max(min_year, start_year)} and {max_year}): "))
                if end_year < max(min_year, start_year) or end_year > max_year:
                    print(f"Invalid year. Must be between {max(min_year, start_year)} and {max_year}.")
                else:
                    break  # Valid input
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        # Recursive call with valid new year values
        df = filter_data(df, start_year=start_year, end_year=end_year)

    return df

def summary_by_country(df):

    df = df[["tconst","country_name","averageRating"]]

    grouped = df.groupby(by="country_name")

    # Will be needed for calculating the average of the first n best movies per country
    def average_first_n(s, n):

        if n > len(s): return None

        return s.nlargest(n).mean()

    # Define the iteration limits
    limits = [i for i in range(10,201,10)]

    result = grouped.agg(count=('tconst', 'count')).reset_index()

    # Create average columns dynamically using a for loop
    for limit in limits:
        result[f'avg_first_{limit}'] = grouped['averageRating'].apply(lambda x: average_first_n(x, limit)).values


    return result

def ranking_countries(df):

    print("TASK 1 - country ranking")
    print("")
    print("")

    n = len(df.columns)
    print("Ranking of top countries with 10, 20, ..., 200 best movies,\nCountries with less than n movies are excluded from nth\nranking and those later.")

    for i in range(n-2):
        print(f"Ranking {i+1} - top 10 countries with {(i+1)*10} movies")
        df = df[df["count"] >= (i+1)*10]
        countries = df[["country_name",df.columns[i+2]]].sort_values(by=df.columns[i+2],ascending = False)["country_name"].values[:10]
        for i in range(len(countries)): print(f"\t{i+1}) {countries[i]}", end=" ")
        print("")


def find_GDP(df, country, year):

    GDP = df[df["Country Code"]==country][year].values[0]

    return GDP

def find_population(df, country, year):
    population = df[df["Country Code"]==country][year].values[0]

    return population

def weak_impact(df):

    df = df[["tconst","country_name","numVotes"]]

    grouped = df.groupby(by="country_name")

    result = grouped.agg(weak_impact=('numVotes', 'sum')).reset_index()

    return result

def strong_impact(df):

    df = df[["tconst","country_name","averageRating"]]

    grouped = df.groupby(by="country_name")

    result = grouped.agg(strong_impact=('averageRating', 'sum')).reset_index()

    return result

def weak_hegemony(df):

    ranks = df.drop(["strong_impact"],axis=1)

    # Add weak_impact rank column
    ranks = ranks.sort_values(by="weak_impact", ascending = False).reset_index(drop=True).reset_index(names="rank_weak_impact")
    # Add GDP rank column
    ranks = ranks.sort_values(by="latest_GDP", ascending = False).reset_index(drop=True).reset_index(names="rank_GDP")
    # Add population rank column
    ranks = ranks.sort_values(by="latest_population", ascending = False).reset_index(drop=True).reset_index(names="rank_population")
    # Add GDP/population ratio rank column
    ranks = ranks.sort_values(by="GDP/population", ascending = False).reset_index(drop=True).reset_index(names="rank_ratio")

    ranks["hegemony_wrt_GDP"] = ranks["rank_GDP"] - ranks["rank_weak_impact"]
    ranks["hegemony_wrt_population"] = ranks["rank_population"] - ranks["rank_weak_impact"]
    ranks["hegemony_wrt_ratio"] = ranks["rank_ratio"] - ranks["rank_weak_impact"]

    hegemon_GDP = ranks.sort_values("hegemony_wrt_GDP",ascending=False).iloc[0]["country_name"]
    hegemon_population = ranks.sort_values("hegemony_wrt_population",ascending=False).iloc[0]["country_name"]
    hegemon_ratio = ranks.sort_values("hegemony_wrt_ratio",ascending=False).iloc[0]["country_name"]


    print("Film hegemon with regard to GDP: ", hegemon_GDP,
          " with GDP rank: ", ranks[ranks["country_name"]==hegemon_GDP]["rank_GDP"].values[0]+1,
          " and weak impact rank: ", ranks[ranks["country_name"]==hegemon_GDP]["rank_weak_impact"].values[0]+1)
    print("")
    print("Film hegemon with regard to population: ", hegemon_population,
          " with population rank: ", ranks[ranks["country_name"]==hegemon_population]["rank_population"].values[0]+1,
          " and weak impact rank: ", ranks[ranks["country_name"]==hegemon_population]["rank_weak_impact"].values[0]+1)
    print("")
    print("Film hegemon with regard to GDP/population ratio: ", hegemon_ratio,
          " with the ratio rank: ", ranks[ranks["country_name"]==hegemon_ratio]["rank_ratio"].values[0]+1,
          " and weak impact rank: ", ranks[ranks["country_name"]==hegemon_ratio]["rank_weak_impact"].values[0]+1)    
    
def strong_hegemony(df):

    ranks = df.drop(["weak_impact"],axis=1)

    # Add weak_impact rank column
    ranks = ranks.sort_values(by="strong_impact", ascending = False).reset_index(drop=True).reset_index(names="rank_strong_impact")
    # Add GDP rank column
    ranks = ranks.sort_values(by="latest_GDP", ascending = False).reset_index(drop=True).reset_index(names="rank_GDP")
    # Add population rank column
    ranks = ranks.sort_values(by="latest_population", ascending = False).reset_index(drop=True).reset_index(names="rank_population")
    # Add GDP/population ratio rank column
    ranks = ranks.sort_values(by="GDP/population", ascending = False).reset_index(drop=True).reset_index(names="rank_ratio")

    ranks["hegemony_wrt_GDP"] = ranks["rank_GDP"] - ranks["rank_strong_impact"]
    ranks["hegemony_wrt_population"] = ranks["rank_population"] - ranks["rank_strong_impact"]
    ranks["hegemony_wrt_ratio"] = ranks["rank_ratio"] - ranks["rank_strong_impact"]

    hegemon_GDP = ranks.sort_values("hegemony_wrt_GDP",ascending=False).iloc[0]["country_name"]
    hegemon_population = ranks.sort_values("hegemony_wrt_population",ascending=False).iloc[0]["country_name"]
    hegemon_ratio = ranks.sort_values("hegemony_wrt_ratio",ascending=False).iloc[0]["country_name"]


    print("Film hegemon with regard to GDP: ", hegemon_GDP,
          " with GDP rank: ", ranks[ranks["country_name"]==hegemon_GDP]["rank_GDP"].values[0]+1,
          " and strong impact rank: ", ranks[ranks["country_name"]==hegemon_GDP]["rank_strong_impact"].values[0]+1)
    print("")
    print("Film hegemon with regard to population: ", hegemon_population,
          " with population rank: ", ranks[ranks["country_name"]==hegemon_population]["rank_population"].values[0]+1,
          " and strong impact rank: ", ranks[ranks["country_name"]==hegemon_population]["rank_strong_impact"].values[0]+1)
    print("")
    print("Film hegemon with regard to GDP/population ratio: ", hegemon_ratio,
          " with the ratio rank: ", ranks[ranks["country_name"]==hegemon_ratio]["rank_ratio"].values[0]+1,
          " and strong impact rank: ", ranks[ranks["country_name"]==hegemon_ratio]["rank_strong_impact"].values[0]+1)  

def hegemony(df, type, year,GDP_source,population_source):

    print("TASK 2 - cinematic hegemony")
    print("")
    print("")

    # Setting up the dataframe
    df_temp = df[["tconst","country_name","country_code"]]
    grouped = df_temp.groupby(by=["country_name","country_code"])
    result = grouped.agg(count=('tconst', 'count')).reset_index()

    result = pd.merge(result, weak_impact(df), on='country_name')
    df = pd.merge(result, strong_impact(df), on='country_name')
    df["latest_GDP"] = df["country_code"].apply(lambda x: find_GDP(GDP_source,x,str(year)))
    df["latest_population"] = df["country_code"].apply(lambda x: find_population(population_source,x,str(year)))
    df["GDP/population"] = df["latest_GDP"]//df["latest_population"]

    # Hegemony calculation

    if type == "weak": weak_hegemony(df)
    if type == "strong": strong_hegemony(df)

def encode(df):

    from sklearn.preprocessing import MultiLabelBinarizer
    
    # Create an instance of MultiLabelBinarizer
    mlb = MultiLabelBinarizer()

    # Fit and transform the genres in column 'a'
    one_hot_encoded = mlb.fit_transform(df['genres'])

    # Convert the result to a DataFrame for better readability
    one_hot_df = pd.DataFrame(one_hot_encoded, columns=mlb.classes_, index=df.index)

    return one_hot_df


def genres_analysis(df):
    '''
    It will take a df solely with columns: "country_name", "genres"
    '''

    # Convert the "genres" column into column of lists, nt strings
    df["genres"] = df["genres"].apply(lambda x: x.split(","))

    # one-hot encode
    one_hot_df = encode(df)

    # Combine the one-hot encoded DataFrame with the original DataFrame
    result = pd.concat([df, one_hot_df], axis=1)

    # Group by countries
    grouped = result.groupby("country_name")
    result_df = grouped.aggregate("sum").reset_index()

    return result_df

def generate_genres_raport(df):

    print("TASK 3 (own analysis) - hegemony in movie genre production")
    print("")
    print("")

    print("Countries with the most movies of a particular genre:")
    print("")

    for col_id in range(1,len(df.columns)-1):

        df_sorted = df.sort_values(by = df.columns[col_id], ascending = False)

        largest = df_sorted.iloc[0][df.columns[col_id]]
        winner = df_sorted.iloc[0]["country_name"]

        print(f"Country with the most {df.columns[col_id]} movies is {winner}, ({largest})")


