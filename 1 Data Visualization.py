# %%
from matplotlib.pyplot import xlabel
import pandas as pd
from pandas.core.indexes.base import Index
from scipy import stats 
import seaborn as sns

df = pd.read_csv("2012.csv")

# %% describe the data type 

df.describe(include="all").to_csv("Column type.csv")

# %% Missing Values
df.isna().sum().to_csv("Missing Data.csv")

# %% Outliers boxplot
sns.boxplot(df["age"])

#%% Outliers boxplot
sns.boxplot(df["weight"])

# %% Duplicate Data 
# df.duplicated().sum()
duplicate = df[df.duplicated()]


# %% Outliers 
from tqdm import tqdm
cols = [ 
    "perobs", 
    "perstop", 
    "age", 
    "weight", 
    "ht_feet", 
    "ht_inch", 
    "datestop", 
    "timestop", 
    "xcoord", 
    "ycoord"
] 
for col in tqdm(cols, desc="convert to number"):
    df[col] = pd.to_numeric(df[col], errors="coerce")



# %%
df = df.dropna()

# %% datestop and timestop

df["datestop"] = df["datestop"].astype(str).str.zfill(8)
df["timestop"] = df["timestop"].astype(str).str.zfill(4)

# %%
from datetime import datetime

def make_datetime(datestop, timestop):
    year =int(datestop[-4:])
    month =int(datestop[:2])
    day =int(datestop[2:4])

    hour =int(timestop[:2])
    minute =int(timestop[2:])

    return datetime(year, month, day, hour, minute)
df["datetime"] = df.apply(
    lambda row:make_datetime(row["datestop"], row["timestop"]), axis=1
    )

# %% height to inch 

df["height"] = (df["ht_feet"] * 12 + df["ht_inch"]) * 2.54



# %% weight 
import seaborn as sns 

sns.distplot(df["height"])

# %% defining age and weight minimum and maximum range 
df = df[(df["age"] <= 110) & (df["age"] >= 5)]
df = df[(df["weight"] <= 350) & (df["weight"] >= 10)]

# %%
sns.countplot(df["datetime"].dt.month)

# %% 1. Attribute Visualization for age 
ax = sns.countplot(df["datetime"].dt.weekday)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"])
ax.set(xlabel="day of week", title="# of incidents by day of weeks")

ax.get_figure().savefig("test.jpg")

# %% Attribute Visualization for Weight 

sns.distplot(df["weight"])

# %% Attribute Visualization for Weight 

wx = sns.countplot(data=df, x="race")
value_label = pd.read_excel(
    ""
)

# %%
