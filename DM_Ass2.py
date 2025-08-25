# Dataset: [Math, Physics, Chemistry]
dataset = [
   [50, 70, 80],
   [90, 85, 60],
   [40, 60, 75],
   [100, 95, 90],
   [60, 75, 85]
]


# Number of rows and columns
rows = len(dataset)
cols = len(dataset[0])


# ---------------------------
# Helper functions
# ---------------------------
def mean(values):
   return sum(values) / len(values)


def std_dev(values):
   mu = mean(values)
   variance = sum((x - mu) ** 2 for x in values) / len(values)
   return variance ** 0.5


# Extract column
def get_column(data, col_index):
   return [row[col_index] for row in data]


# ---------------------------
# 1. Min-Max Normalization
# ---------------------------
min_max_norm = []
for j in range(cols):
   col = get_column(dataset, j)
   min_val, max_val = min(col), max(col)
   normalized_col = [(x - min_val) / (max_val - min_val) for x in col]
   min_max_norm.append(normalized_col)


# ---------------------------
# 2. Z-Score Normalization
# ---------------------------
z_score_norm = []
for j in range(cols):
   col = get_column(dataset, j)
   mu, sigma = mean(col), std_dev(col)
   normalized_col = [(x - mu) / sigma for x in col]
   z_score_norm.append(normalized_col)


# ---------------------------
# 3. Decimal Scaling Normalization
# ---------------------------
decimal_scaling_norm = []
for j in range(cols):
   col = get_column(dataset, j)
   max_abs = max(abs(x) for x in col)
   k = len(str(max_abs))  # number of digits
   normalized_col = [x / (10 ** k) for x in col]
   decimal_scaling_norm.append(normalized_col)


# ---------------------------
# Display Results
# ---------------------------
print("Original Dataset:")
for row in dataset:
   print(row)


print("\nMin-Max Normalization:")
for i in range(rows):
   print([round(min_max_norm[j][i], 4) for j in range(cols)])


print("\nZ-Score Normalization:")
for i in range(rows):
   print([round(z_score_norm[j][i], 4) for j in range(cols)])


print("\nDecimal Scaling Normalization:")
for i in range(rows):
   print([round(decimal_scaling_norm[j][i], 4) for j in range(cols)])
