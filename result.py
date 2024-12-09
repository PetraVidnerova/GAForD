import sys
import pandas as pd
import numpy as np

DIR = sys.argv[1]
PREFIX = sys.argv[2]

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
#for rew in 0, 1, 2, 3:
for sim in range(39):
    for k in range(10):
        fixed_points, f = extract_result(f"{PREFIX}_sim{sim}_{k}.log")
        assert fixed_points == 0, f"{PREFIX}_sim{sim}_{k}.log"
        df_list.append(
            {
                "sim": sim,
                "k": k,
                "F": f,
#                "fixed_points": fixed_points
            }
        )

df = (
    pd.DataFrame(df_list)
    .pivot(index=["sim"], columns="k")
    .swaplevel(0, 1, axis=1)
)
df.columns = df.columns.droplevel(1)
print(df)

df.to_csv(f"export_results/GA_full_results_{PREFIX}.csv", index=False, header=False)


df = (
    pd.DataFrame(df_list)
    .groupby(["sim"])["F"]
    .agg([ "min",  "median", "mean", "max"])
)
print(df)
df.to_csv(f"export_results/GA_result_statistics_{PREFIX}.csv")

