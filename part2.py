# %% read dataframe
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from pandas.core.indexes.base import ensure_index_from_sequences


df = pd.read_pickle("data.pkl")


# %% convert physical forces used columns to booleans
pfs = [col for col in df.columns if col.startswith("pf_")]
for col in pfs:
    df[col] = df[col] == "YES"


# %% manual one hot encoding for race / city
for val in df["race"].unique():
    df[f"race_{val}"] = df["race"] == val

for val in df["city"].unique():
    df[f"city_{val}"] = df["city"] == val

# %% convert inout to boolean
df["inside"] = df["inout"] == "INSIDE"

# %% convert arrest made to boolean
df["arstmade"] = df["arstmade"] == "YES"

# %% convert officer in Uniform to boolean
df["offunif"] = df["offunif"] == "YES"

# %% create armed column
df["armed"] = (
    (df["contrabn"] == "YES")
    | (df["pistol"] == "YES")
    | (df["riflshot"] == "YES")
    | (df["asltweap"] == "YES")
    | (df["knifcuti"] == "YES")
    | (df["machgun"] == "YES")
    | (df["othrweap"] == "YES")
)

#%%

df["reasonforFrisk"]= (
    (df["rf_vcrim"] == "YES")
    |   (df["rf_othsw"] == "YES")
    |   (df["rf_attir"] == "YES")
    |   (df["rf_vcact"] == "YES")
    |   (df["rf_rfcmp"] == "YES")
    |   (df["rf_verbl"] == "YES")
    |   (df["rf_knowl"] == "YES")
    |   (df["rf_furt"] == "YES")
    |   (df["rf_bulg"] == "YES")
)

# %% select columns for association rules mining
cols = [
    col
    for col in df.columns
    if col.startswith("pf_") or col.startswith("race_") or col.startswith("city_")
] + ["inside", "arstmade", "offunif", "reasonforFrisk", "armed"]

# %% apply frequent itemset mining
frequent_itemsets = apriori(df[cols], min_support=0.03, use_colnames=True)#[:20]

# %% apply association rules mining
rules = association_rules(frequent_itemsets, min_threshold=0.4)

# %% sort rules by confidence
rules.sort_values("confidence", ascending=False)

#%%
