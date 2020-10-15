# %%
import pandas as pd
import seaborn as sns

df = pd.read_csv("2012.csv")

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
    order=pf_used["detailcm"]#.value_counts(ascending=False)#.keys()[:10],
)
# %%
pfs = 