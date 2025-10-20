import pandas as pd
import sys

final_file_name = 'css_chatgpt2023_research.csv'
csv_files_to_combine = [
    'css_chatgpt2023_research_march.csv',
    'css_chatgpt2023_research_may.csv',
    'css_chatgpt2023_research_april.csv',
    'css_chatgpt2023_research_december.csv'
]
csv_separator = ','


def combine_and_save_csvs(file_list, final_name, separator):
    #list to hold the dataframes read from files
    list_of_dfs = []

    for file in file_list:
        try:
            df = pd.read_csv(file, sep=separator, index_col=0)
            list_of_dfs.append(df)
            print(f"Successfully loaded: {file} ({len(df):,} rows)")
        except Exception as e:
            #to see if something went wrong
            print(f"ERROR reading file {file}: {e}")

    if not list_of_dfs:
        print("\nCombination not possible.")
        sys.exit(1)

    #combine all loaded dataframes
    df_combined = pd.concat(list_of_dfs, ignore_index=True)

    """During the process of combining the CSV files, two redundant columns are created which do not contribute to 
    the research and are consequently removed:
     
    Unnamed: 0: This column appears because the row numbers from the pandas DataFrame were saved by mistake. 
    This happened because the option index=True was used when saving the file, and later the file was read without 
    telling pandas to use the first column as the index (index_col=0 was not used). As a result, this column just 
    repeats the row numbers and does not give any useful information.

    parent_id: This column comes from the original data source (Reddit). It shows the ID of the post that came before. 
    This is important when collecting the data, because it helps show the structure of the conversation. But for our 
    research, which looks only at the content, this column is not needed, so we remove it.
    
    We drop these columns to ensure the final dataset remains clean, 
    focused, and efficient for research purposes"""

    columns_to_drop = ['parent_id', 'Unnamed: 0']
    #drop specified columns, errors='ignore' prevents failure if a column is missing
    df_final = df_combined.drop(columns=columns_to_drop, errors='ignore')

    df_final.to_csv(final_name, index=False, sep=separator)
    print(f"Saved final file: {final_name} ({len(df_final):,} total rows)")
    return df_final

if __name__ == "__main__":
    combine_and_save_csvs(csv_files_to_combine, final_file_name, csv_separator)