import pandas as pd

def extract_result(filename):
    with open(filename, "r") as f:
        last_result = None
        for line in f:
            if line.startswith("RESULT:"):
                last_result = line.strip()
    _, _, fixed_points, f = last_result.split()
    return fixed_points, f 

df_list = []
for rew in range(3):
    for sim in range(10):
        for k in range(10):
            fixed_points, f = extract_result(f"rew{rew}_sim{sim}_{k}.log")
            df_list.append(
                {
                    "rew": rew,
                    "sim": sim,
                    "k": k,
                    "F": -float(f),
                    "fixed_points": int(fixed_points)
                }
            )

df = (
    pd.DataFrame(df_list)
    .pivot(index=["rew", "sim"], columns="k")
    .swaplevel(0, 1, axis=1)
)
print(df)

df = (
    pd.DataFrame(df_list)
    .groupby(["rew", "sim"])["F"]
    .agg([ "min",  "mean", "max"])
)
print(df)

