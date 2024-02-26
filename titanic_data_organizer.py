import pandas as pd
import os

# read data from online resource
data_source = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
data = pd.read_csv(data_source)

# base dir
base_dir = os.getcwd() # interact with system
base_data_dir = f"{base_dir}/Data Titanic" # variable declaration with f-string

for survived in data["Survived"].unique(): # object looping
    first_subfolder = "Survived" # variable declaration
    if survived==0: # branching 
        first_subfolder = "Not Survived" # variable declaration

    # create 1st subfolder
    print(f"{first_subfolder}/")
    current_directory = f"{base_data_dir}/{first_subfolder}" # variable declaration with f-string
    if not os.path.exists(current_directory): # branching 
        os.makedirs(current_directory) # interact with system

    # create 2nd subfolder
    for embarked in data["Embarked"].unique(): # object looping
        second_subfolder = " "
        if embarked == "S": # branching 
            second_subfolder = "Southampton" # variable declaration
        if embarked == "C": # branching 
            second_subfolder = "Cherbourg" # variable declaration
        if embarked == "Q": # branching 
            second_subfolder = "Queenstown" # variable declaration
        if f"{embarked}" in 'SCQ': # branching 
            print("\t", f"{second_subfolder}/")
            current_directory = f"{base_data_dir}/{first_subfolder}/{second_subfolder}" # variable declaration with f-string
            if not os.path.exists(current_directory): # branching
                os.makedirs(current_directory) # interact with system
        
        # if Embarked is unknown
        if f"{embarked}" not in 'SCQ': # branching 
            current_directory = f"{base_data_dir}/{first_subfolder}/"
            filtered = data[
                          (data.Survived==survived) &
                          (data.Embarked.isnull())
                       ]
            if filtered.shape[0]>0: # branching 
                passengers = "passengers" # variable declaration
                if filtered.shape[0]==1: # branching 
                    passengers = passengers[:-1] # variable declaration
                print("\t", f"Intruder_({filtered.shape[0]} {passengers}).txt")
                filtered.to_csv(f"{current_directory}/Intruder__({filtered.shape[0]} {passengers}).txt", index=False)
            continue

        # create 3rd sub folder
        for sex in data["Sex"].unique(): # object looping
            print("\t\t", f"{sex.title()}/")
            third_subfolder = sex # variable declaration
            current_directory = f"{base_data_dir}/{first_subfolder}/{second_subfolder}/{third_subfolder}" # variable declaration with f-string
            if not os.path.exists(current_directory): # branching 
                os.makedirs(current_directory)

            # save filtered data in 3rd sub folder
            for ticket in data["Ticket"].unique(): # object looping
                filtered = data[
                    (data.Survived==survived) & # comparison and logical operation
                    (data.Embarked==embarked) &
                    (data.Sex==sex) &
                    (data.Ticket==ticket)
                ]
                if filtered.shape[0]>0: # branching 
                    passengers = "passengers" # variable declaration
                    if filtered.shape[0]==1: # branching 
                        passengers = passengers[:-1] # list slicing
                    print("\t\t\t", f"{ticket.replace('/','_')}_({filtered.shape[0]} {passengers}).txt")
                    filtered.to_csv(f"{current_directory}/{ticket.replace('/','_')}_({filtered.shape[0]} {passengers}).txt", index=False)