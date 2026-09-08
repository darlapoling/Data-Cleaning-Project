#These are tricky examples of null values in the data. For both, they are MCAR (Missing Completely at Random). For billing_amount, the null values may represent patients who did not pay or did not have a payment due. For gender, null values may represent non-binary patients or patients of other genders. However, in the Kaggle for this dataset, it says the values are missing values, so we will treat both variables as such and choose an imputation method.

#For gender, I will use name-based imputation. Other common methods for gender include mode-based imputation, which generalizes the data, and MICE (Multivariate Imputation by Chained Equations), which uses logistic regression and is robust, but increases the scope of the project. MICE will be considered at a later date. I choose name-based imputation because the nammes are familiar to me as an English-speaker and I can look up gender probabilities of names through Census data. 

#Gender imputation: The average age of the patients is 53.75 years old. This leads to a search for baby name gender statistics in 1973. The SSA (Social Security Administration) provides a means of searching their records for the popularity of baby names by year. https://www.ssa.gov/oact/babynames/ Through this, I can access a list of the top 100 names for the year 1973. If the name is on the list of a gender, it will be imputated to be the corresponding gender. If the name is associated with both or neither of the genders, then the gender will be imputed to be female




#All of the duplicate names appear to be independent individuals. They are either very different in age of different genders. When they are similar in age the appointment dates confirm that it is impossible for them to be the same person, as with the two Christopher Lopez's. 