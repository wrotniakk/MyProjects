import formulas
import argparse
import pandas as pd
import numpy as np
import time
import cProfile
import pstats

def main():

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Load TSV files from the specified folder.')
    
    # Add the folder path argument
    parser.add_argument('folder_path', type=str, help='Path to the folder containing .tsv files')
    parser.add_argument('--start_year', type=int, help='Starting year for the analysis')
    parser.add_argument('--end_year', type=int, help='Ending year for the analysis')

    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Load the TSV files into DataFrames

    calculate = input("Do you want to load country data from scratch or load it from preprocessed file?\n(Loading from scratch may take even 50min...) [y/n]: ")

    dataframes = formulas.load_data(args.folder_path,calculate)
    add_data = formulas.load_add_data(args.folder_path)
    
    dataframes = formulas.clean_data(dataframes)

    movies_df = formulas.merge_data(dataframes)
    movie_df_cleaned = formulas.post_clean(movies_df,add_data)

    # Narrow down to the years that are also found in the additional data

    max_GDP_list = list(add_data["countries_GDP.csv"].columns[4:-1])
    for i in range(len(max_GDP_list)): max_GDP_list[i] = int(max_GDP_list[i])
    max_GDP = max(max_GDP_list)

    max_population_list = list(add_data["countries_population.csv"].columns[4:-1])
    for i in range(len(max_population_list)): max_population_list[i] = int(max_population_list[i])
    max_population = max(max_population_list)

    minimum = min(max_GDP,max_population)

    movie_df_filtered = formulas.filter_data(movie_df_cleaned,start_year=1960, end_year=minimum)

    # Narrow down to the year range provided in the command line

    movie_df_filtered = formulas.filter_data(movie_df_cleaned,start_year=args.start_year, end_year=args.end_year)

    # TASK 1
    print("")
    print("")
    summary = formulas.summary_by_country(movie_df_filtered)
    formulas.ranking_countries(summary)

    # TASK 2
    print("")
    print("")
    formulas.hegemony(movie_df_filtered,"weak",minimum,add_data["countries_GDP.csv"],add_data["countries_population.csv"])

    # Task 3
    print("")
    print("")
    df_gen_an = formulas.genres_analysis(movie_df_filtered[["country_name","genres"]])
    formulas.generate_genres_raport(df_gen_an)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
        # Profile the code and write output to a .prof file
    with open('profiling_results.txt', 'w') as f:
        profiler = cProfile.Profile()   # Create a profiler instance
        profiler.enable()                # Start profiling
        main()                           # Run the main function
        profiler.disable()               # Stop profiling

        # Create a Stats object and write to the text file
        ps = pstats.Stats(profiler, stream=f)  # Stream results to the file
        ps.sort_stats('cumulative')    # Sort by cumulative time
        ps.print_stats()                # Print the stats to the file

    print("Profiling results stored in 'profiling_results.txt'.")
    