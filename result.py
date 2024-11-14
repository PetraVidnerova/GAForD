import sys
import pandas as pd
import numpy as np

DIR = sys.argv[1]

def extract_result(filename):
    df_run = []
    try:
        with open(f"{DIR}/{filename}", "r") as f:
            last_result = None
            i = 0 
            for line in f:
                if line.startswith("RESULT:"):
                    last_result = line.strip()
                    _, _, fixed_points, f = last_result.split()
                    df_run.append({
                        "iter": i,
                        "F": -float(f),
                        "fixed_points": fixed_points
                    })
                    i += 1
        df = pd.DataFrame(df_run)
        #        df.to_csv(f"{DIR}/{filename}.csv")
        return float(fixed_points), -float(f)
    except:
        return np.nan, np.nan

df_list = []
for rew in 0, 1, 4:
    for sim in range(10):
        for k in range(10):
            fixed_points, f = extract_result(f"rew{rew}_sim{sim}_{k}.log")
            df_list.append(
                {
                    "rew": rew,
                    "sim": sim,
                    "k": k,
                    "F": f,
                    "fixed_points": fixed_points
                }
            )

df = (
    pd.DataFrame(df_list)
    .pivot(index=["rew", "sim"], columns="k")
    .swaplevel(0, 1, axis=1)
)
#print(df)

df = (
    pd.DataFrame(df_list)
    .groupby(["rew", "sim"])["F"]
    .agg([ "min",  "median", "mean", "max"])
)
print(df)

