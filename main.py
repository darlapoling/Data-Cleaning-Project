#https://stackoverflow.com/questions/52072381/how-to-print-only-the-duplicate-elements-in-python-list
#https://realpython.com/python-data-cleaning-numpy-pandas/

from collections import Counter
import pandas as pd

#Reading CSV file while defining all empty values to be the same.
df = pd.read_csv(
    "messy_clinic_appointments.csv",
    na_values=["", "NaN", "nan", "null", "NULL", "empty", " "]
)
    #print(df.head())
    #print(df.tail())

def unique_values():
    print("Unique Values")
    #Checking for unqie 
    print(df['patient_id'].is_unique)

    df["patient_id"] = df["patient_id"].astype(str).str.strip()

    #Checking for repeated patient IDs. This is possible, for multiple visits, but must be investigated.
    print(df["patient_id"].is_unique) #False

    #Duplicate patient IDs exist, printing a list to be investigated. 
    dupe_ids = df["patient_id"].value_counts()
    dupe_ids = dupe_ids[dupe_ids > 1].index.tolist()
    print("Duplicate IDs:", dupe_ids)

    #duplicate_rows = df[df["patient_id"].duplicated(keep=False)]
    #print(duplicate_rows)
    print("hello!!!")

    result = df[df['patient_id'].isin(dupe_ids)]['patient_name']
    print(result)
    print(result.describe())

    #Replace patient_id values with a clean numeric index from 0, 1, 2, ...
    df.set_index('patient_id', inplace=True)
    df.index = range(len(df))
    print(df.head())

    #Check for duplicate patient names. This is possible but must be investigated. 
    print(df["patient_name"].is_unique) # False

    #Duplicate patient names exist, printing a list to be investigated. 
    dupe_names = df["patient_name"].value_counts()
    dupe_names = dupe_names[dupe_names > 1].index.tolist()
    print("Duplicate Names:", dupe_names)
    duplicate_rows = df[df["patient_name"].duplicated(keep=False)]
    duplicate_rows.drop(columns=['billing_amount','follow_up_required','department'], inplace=True)
    duplicate_rows = duplicate_rows.sort_values(by='patient_name')
    print(duplicate_rows)

def null_values():
    #Checking for empty values.
    print("Is Null?")
    print(df.isna().sum()) #50 flagged values in gender and 50 flagged values in billing_amount

    #Looking closer at the data.
    df_sorted = df.sort_values(by='billing_amount', ascending=True)
    df_sorted.drop(columns=['follow_up_required','department', 'booking_date','patient_id'], inplace=True)
    print(df_sorted)

    df_sorted1 = df.sort_values(by='gender', ascending=True)
    df_sorted1.drop(columns=['follow_up_required','department', 'booking_date','patient_id'], inplace=True)
    print(df_sorted1)
    
    #Dealing with empty of NaN values. First defining all to be the same.

    df_null = df[df.isna().any(axis=1) | (df == "").any(axis=1)]
    print('df_null: ',df_null) # 98 Rows that contain null values. This is 9.8% of the data.
    print(df_null[df_null["gender"].isna()][["patient_id", "patient_name", "gender", 'billing_amount']])
    print(df_null[df_null["billing_amount"].isna()][["patient_id", "patient_name", "gender","billing_amount"]])

def imputation_method():
    print("Imputation Method")

def standardize_data():
    print("Standardize Data")
    #Standardizing the dates
    #https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
    df['booking_date'] = pd.to_datetime(df['booking_date'], format = "mixed").dt.date
    df['appointment_date'] = pd.to_datetime(df['appointment_date'], format = "mixed").dt.date

    #Standardizing the gender values
    df['gender'] = df['gender'].str.lower().replace(['female', 'Female', 'F', 'f', '0'], 'female')
    df['gender'] = df['gender'].str.lower().replace(['male', 'Male', 'M', 'm', '1'], 'male')

    #Standardizing billing amounts to US dollars


    #Standardizing follow up needed values
    df['follow_up_required'] = df['follow_up_required'].str.lower().replace(['1', 'y', 'yes'], 'yes')
    df['follow_up_required'] = df['follow_up_required'].str.lower().replace(['0', 'n', 'no'], 'no')

def main():
    df.to_csv("cleaned_data1.csv", index=False)
    standardize_data()

    

    null_values()
    
    imputation_method()

    unique_values()


if __name__ == "__main__":
    main()


print(df.head())
df.to_csv("cleaned_data.csv", index=False)