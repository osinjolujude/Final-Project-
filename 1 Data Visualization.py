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

# %% Outliers boxplot age 
sns.boxplot(df["age"])

#%% Outliers boxplot weight
sns.boxplot(df["weight"])

# %% Duplicate Data 
# df.duplicated().sum()
duplicate = df[df.duplicated()]


# %%  pick important columns, convert them to numbers and coerce errors found in data
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



# %% drop NaN values from dataset
df = df.dropna()

# %% datestop and timestop conversion to meaningful usable datetime values

df["datestop"] = df["datestop"].astype(str).str.zfill(8)
df["timestop"] = df["timestop"].astype(str).str.zfill(4)

# %% Merge datestop and timestop together 
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

# %% convert height to inch 
df["height"] = (df["ht_feet"] * 12 + df["ht_inch"]) * 2.54

# %% converting xcoord and ycoord to Longitudes and Latitudes 
import pyproj

srs = "+proj=lcc +lat_1=41.03333333333333 +lat_2=40.66666666666666 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000.0000000001 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs"
p = pyproj.Proj(srs)
 
coords = df.apply(
    lambda r: p(r["xcoord"], r["ycoord"], inverse=True), axis=1
)
df["lat"] = [c[1] for c in coords]
df["lon"] = [c[0] for c in coords]

# %% Height Visualization

sns.distplot(df["height"])

# %% defining age and weight minimum and maximum range 
df = df[(df["age"] <= 110) & (df["age"] >= 5)]
df = df[(df["weight"] <= 350) & (df["weight"] >= 10)]

# %%
aw = sns.countplot(df["datetime"].dt.month)
aw.set_xticklabels(["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"])
aw.set(xlabel="Months", title="# of incidents by Month")

# %% 1. Attribute Visualization for days of week
ax = sns.countplot(df["datetime"].dt.weekday)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"])
ax.set(xlabel="day of week", title="# of incidents by day of weeks")

ax.get_figure().savefig("test.jpg")

# %% Attribute Visualization for Weight 

sns.distplot(df["weight"])

# %% Attribute Visualization for Weight 
import numpy as np

value_labels = pd.read_excel(
    "2012 SQF File Spec.xlsx", sheet_name="Value Labels", skiprows=range(4)
)
value_labels["Field Name"] = value_labels["Field Name"].fillna(method="ffill")

value_labels["Field Name"] = value_labels["Field Name"].str.lower()

value_labels["Value"] = value_labels["Value"].fillna(" ")

vl_mapping = value_labels.groupby("Field Name").apply(
    lambda x:dict(
        [(row["Value"], row["Label"]) for row in x.to_dict("records")]
    )
)

cols = [col for col in df.columns if col in vl_mapping]

for col in tqdm(cols):
    df[col] = df[col].apply(
        lambda val: vl_mapping[col].get(val, np.nan)
    )

# %%Attribute Visualization for race
wx = sns.countplot(data=df, y="race")

# %% Attribute Visualization for sex
wx = sns.countplot(data=df, x="sex")

# %% Attribute Visualization for forceuse
wx = sns.countplot(data=df, y="forceuse")

# %%

sns.countplot(x="city", data=df)

# %%
#wx = sns.countplot(data=df, y="perobs")

# %%

sns.scatterplot(data=df[:100], x="xcoord", y="ycoord")


# %%

import folium

m = folium.Map((40.7128, -74.0060))

for r in df[["lat", "lon"]][df["detailcm"]=="ROBBERY"][:500].to_dict("records"):
    folium.CircleMarker(location=(r["lat"], r["lon"]), radius=1).add_to(m)


# %%

sns.countplot(data=df, y="race", hue="city")

# %%
#sns.barplot(data=df, y="recstat")

# %%

pf_used = df[
    (df["pf_hands"] == "YES")
    |   (df["pf_wall"] == "YES")
    |   (df["pf_grnd"] == "YES")
    |   (df["pf_drwep"] == "YES")
    |   (df["pf_ptwep"] == "YES")
    |   (df["pf_baton"] == "YES")
    |   (df["pf_hcuff"] == "YES")
    |   (df["pf_pepsp"] == "YES")
    |   (df["pf_other"] == "YES")
]

sns.countplot(
    data=pf_used, 
    y="detailcm", 
    order=pf_used["detailcm"].value_counts(ascending=False).keys()[:10],
)

# %%
pfs= [col for col in df.columns if col.startswith("pf_")]
pf_counts = (df[pfs] == "YES").sum()
sns.barplot(y=pf_counts.index, x=pf_counts.values / df.shape[0])

# %%

df.to_pickle("data.pkl")


# %% drop columns that are not used in analysis
df = df.drop(
    columns=[
        # processed columns
        "datestop","timestop","ht_feet", "ht_inch","xcoord",
        "ycoord",
        # not useful
        "year",
        "recstat",
        "crimsusp",
        "dob",
        "ser_num",
        #"arstoffn",
        "sumoffen",
        "compyear",
        "comppct",
        "othfeatr",
        "adtlrept",
        "dettypcm",
        "linecm",
        "repcmd",
        "revcmd",
        # location of stop
        # only use coord and city
        "addrtyp",
        "rescode",
        "premtype",
        "premname",
        "addrnum",
        "stname",
        "stinter",
        "crossst",
        "aptnum",
        "state",
        "zip",
        "addrpct",
        "sector",
        "beat",
        "post",
    ]
)

# %% modify one column
df["trhsloc"] = df["trhsloc"].fillna("NEITHER")

# %% remove all rows with NaN
df = df.dropna()

# %% save dataframe to a file
df.to_pickle("data.pkl")

# %%

rf_sqf = df[
    (df["rf_vcrim"] == "YES")
    |   (df["rf_othsw"] == "YES")
    |   (df["rf_attir"] == "YES")
    |   (df["rf_vcact"] == "YES")
    |   (df["rf_rfcmp"] == "YES")
    |   (df["rf_verbl"] == "YES")
    |   (df["rf_knowl"] == "YES")
    |   (df["rf_furt"] == "YES")
    |   (df["rf_bulg"] == "YES")
]

sns.countplot(
    data=pf_used, 
    y="forceuse", 
    order=pf_used["forceuse"].value_counts(ascending=False).keys(),
)
# %%
