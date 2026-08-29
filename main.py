#https://stackoverflow.com/questions/52072381/how-to-print-only-the-duplicate-elements-in-python-list
#https://realpython.com/python-data-cleaning-numpy-pandas/

from collections import Counter

import pandas as pd

df = pd.read_csv("messy_clinic_appointments.csv")

#print(df.head())

#print(df.tail())

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

#All of the duplicate names appear to be independent individuals. They are either very different in age of different genders. When they are similar in age the appointment dates confirm that it is impossible for them to be the same person, as with the two Christopher Lopez's. 