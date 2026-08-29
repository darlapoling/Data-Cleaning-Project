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
print(df["patient_id"].is_unique)

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