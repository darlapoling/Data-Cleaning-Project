#https://stackoverflow.com/questions/52072381/how-to-print-only-the-duplicate-elements-in-python-list
#https://realpython.com/python-data-cleaning-numpy-pandas/

from collections import Counter
import pandas as pd

#Reading CSV file while defining all empty values to be the same.
df = pd.read_csv(
    "messy_clinic_appointments.csv",
    na_values=["", "NaN", "nan", "null", "NULL", "empty"]
)
#print(df.head())
#print(df.tail())

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

#These are tricky examples of null values in the data. For both, they are MCAR (Missing Completely at Random). For billing_amount, the null values may represent patients who did not pay or did not have a payment due. For gender, null values may represent non-binary patients or patients of other genders. However, in the Kaggle for this dataset, it says the values are missing values, so we will treat both variables as such and choose an imputation method.

#For gender, I will use name-based imputation. Other common methods for gender include mode-based imputation, which generalizes the data, and MICE (Multivariate Imputation by Chained Equations), which uses logistic regression and is robust, but increases the scope of the project. MICE will be considered at a later date. I choose name-based imputation because the nammes are familiar to me as an English-speaker and I can look up gender probabilities of names through Census data. 

#Gender imputation: The average age of the patients is 53.75 years old. This leads to a search for baby name gender statistics in 1973. The SSA (Social Security Administration) provides a means of searching their records for the popularity of baby names by year. https://www.ssa.gov/oact/babynames/ Through this, I can access a list of the top 100 names for the year 1973. If the name is on the list of a gender, it will be imputated to be the corresponding gender. If the name is associated with both or neither of the genders, then the gender will be imputed to be female

#Dealing with empty of NaN values. First defining all to be the same.

df_null = df[df.isna().any(axis=1) | (df == "").any(axis=1)]
print('df_null: ',df_null) # 98 Rows that contain null values. This is 9.8% of the data.
print(df_null[df_null["gender"].isna()][["patient_id", "patient_name", "gender", 'billing_amount']])
print(df_null[df_null["billing_amount"].isna()][["patient_id", "patient_name", "gender","billing_amount"]])

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
df.to_csv("cleaned_data1.csv", index=False)

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

print(df.head())
df.to_csv("cleaned_data.csv", index=False)

print(df["age"].mean())
print(df["gender"].mode())