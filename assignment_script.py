import pandas as pd

df = pd.read_csv("https://github.com/dustywhite7/Econ8310/raw/master/AssignmentData/cookie_cats.csv")

print("First few rows of the data: ", df.head(), "\n")
print("Column and dtypes: ", df.dtypes, "\n")

# Basic cleaning and type checks. Makes sure that retention variables are numeric (0/1). 
# If not, they will be converted.
for col in ["retention_1", 'retention_7']:
    if df[col].dtype != "int64" and df[col].dtype != "float64":
        df[col] = df[col].astype(int)

print("No. of rows: ", len(df))
print("Unique versions: ", df["version"].unique(), "\n")

# Overall retention rates
overall_retention1 = df["retention_1"].mean()
overall_retention7 = df["retention_7"].mean()

print("1-day retention rate (overall): {:.3%}".format(overall_retention1))
print("7-day retention rate (overall): {:.3%}\n".format(overall_retention7))

# Retention rates by version
grouped = df.groupby("version").agg(
    n_users=("userid", "count"),
    retention1_rate=("retention_1", "mean"),
    retention7_rate=("retention_7", "mean")
).reset_index()

print("Retention by version: ", grouped, "\n")



for _, row in grouped.iterrows():
    version = row["version"]
    n = row["n_users"]
    r1 = row["retention1_rate"]
    r7 = row["retention7_rate"]
    print(f"Version: {version}")
    print(f"  Number of users:          {n}")
    print(f"  1-day retention rate:     {r1:.3%}")
    print(f"  7-day retention rate:     {r7:.3%}")
    print()


# Computing the effect of moving the gate
control_version = "gate_30"
treatment_version = "gate_40"

control = grouped[grouped["version"] == control_version].iloc[0]
treatment = grouped[grouped["version"] == treatment_version].iloc[0]

effect_retention1 = treatment["retention1_rate"] - control["retention1_rate"]
effect_retention7 = treatment["retention7_rate"] - control["retention7_rate"]

print("Effect of moving the gate from level 30 to level 40:")
print("---------------------------------------------------")
print("1-day retention:")
print(f"  Control ({control_version}):   {control['retention1_rate']:.3%}")
print(f"  Treatment ({treatment_version}): {treatment['retention1_rate']:.3%}")
print(f"  Difference (treatment - control): {effect_retention1:.3%}")
print()

print("7-day retention:")
print(f"  Control ({control_version}):   {control['retention7_rate']:.3%}")
print(f"  Treatment ({treatment_version}): {treatment['retention7_rate']:.3%}")
print(f"  Difference (treatment - control): {effect_retention7:.3%}")
print()