import pandas as pd
import numpy as np

va_path = pd.read_csv("output/va_path.csv")
va_path.columns = ["LOINC", "va_path"]
phs_path = pd.read_csv("output/phs_path.csv")
phs_path.columns = ["LOINC", "phs_path"]

print("Number of va paths: %i"%len(va_path))
print("Number of phs paths: %i"%len(phs_path))

df = pd.merge(va_path, phs_path, on="LOINC", sort=True).dropna()
print("Number of same LOINCs: %i"%(len(df)))

df.to_csv("joined_path.csv", index=False)


def find_common_roots(x,y):
	"""
	returns the common root.
	the function assumes that x has fewer nodes than y
	"""
	x = x.split(".")
	y = y.split(".")

	shared = []
	for i in range(len(x)):
		if x[i] == y[i]:
			shared.append(x[i])
	return ".".join(shared)


va_path = df["va_path"].to_list()
phs_path = df["phs_path"].to_list()
loinc = df["LOINC"].to_list()

shared_paths = []
diff_level = []
no_c_root = []

print("Mapping...")
for i in range(len(va_path)):
	# va_path should be the rolled up version of phs_path
	diff = va_path[i].count(".") - phs_path[i].count(".")

	if diff > 0:
		print("va path longer than phs at loinc id %s.\nVA: %s\nPHS:%s"%(loinc[i], va_path[i],phs_path[i]))
		c_root = find_common_roots(phs_path[i], va_path[i])

	else:
		c_root = find_common_roots(va_path[i], phs_path[i])

	shared_paths.append(c_root)

	if c_root:
		diff_level.append(phs_path[i].count(".")-c_root.count("."))
	else:
		diff_level.append(0)
		no_c_root.append(loinc[i]+" | VA: "+va_path[i]+" | PHS: "+phs_path[i])
		print("No common root at "+loinc[i]+" | VA: "+va_path[i]+" | PHS: "+phs_path[i])

print("Writting...")

df["common root"] = shared_paths
df["diff level"] = diff_level

df.to_csv("output/shared_root_summary.csv", index=False)
with open("output/no_shared_roots.txt", "w") as fp:
	fp.write("\n".join(no_c_root))


