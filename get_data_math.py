import pandas as pd
import numpy as np
import json, os, time
from datetime import datetime
from urllib.request import urlopen
from dotenv import load_dotenv
load_dotenv()

def get_data_math() -> pd.DataFrame:
    """
    Fetches structured data related to mathematics research from multiple sources.

    Retrieves data from provided URLs (stored in environment variables) for 
    specific universities and years, combines them into a single DataFrame, and 
    returns the result.

    Returns:
        pandas.DataFrame: containing the combined data from all specified sources.
    """
    print()
    print(f'{" GETTING STRUCTURED DATA (Mat) ":=^46s}')

    # load config
    MATH_ITS_1 = os.getenv("MATH_ITS_1")
    MATH_ITS_2 = os.getenv("MATH_ITS_2")
    MATH_ITS_3 = os.getenv("MATH_ITS_3")

    univs = {
        "Institut Teknologi Sepuluh Nopember_1": MATH_ITS_1,
        "Institut Teknologi Sepuluh Nopember_2": MATH_ITS_2,
        "Institut Teknologi Sepuluh Nopember_3": MATH_ITS_3,
    }

    # define years to search
    years = list(range(2017,2025))

    # create empty dataframe to store all results
    mat_data = pd.DataFrame()

    # iterate over univs
    for univ in univs.keys():
        print(univ, end=" ")

        # iterate over years
        for year in years:
            time.sleep(.05)

            # if year is exists
            try:
                # open url
                response = urlopen(f"{univs[univ]}{year}/JSON/data.js")
                
                # extract
                data = json.loads(response.read())
                df = pd.DataFrame().from_records(data)

                # transform
                df["Univ"] = [univ]*df.shape[0]
                df["Year_"] = [year]*df.shape[0]
                df["ts"] = [datetime.now()]*df.shape[0]
                base_url = f"{univs[univ].split('cgi/')[0]}"

                if "uri" not in df.columns: 
                    df["uri"] = [np.nan]*df.shape[0] 
                if "eprintid" not in df.columns: 
                    df["eprintid"] = [np.nan]*df.shape[0] 

                df["uri"] = df.apply(lambda x: f"{base_url}{str(x.eprintid)}" if len(str(x.uri))<1 or isinstance(x.uri, float) else x.uri, axis=1)

                # concatenating data
                mat_data = pd.concat([mat_data, df])
                print(".", end='')
            
            except Exception as e:
                print("x", end="")
                continue
            
        print()

    # sleep to avoid rate limit 
    time.sleep(5)

    return mat_data

if __name__ == "__main__":
    data = get_data_math()
    
    # Save data
    data.to_csv(f"data_math.csv", index=False)