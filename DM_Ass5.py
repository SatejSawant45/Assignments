import numpy as np
import matplotlib.pyplot as plt

# Example: bigger dataset with multiple groups
data_groups = {
    "Class A": [7, 8, 5, 6, 12, 14, 7, 9, 10, 15, 18, 3, 5, 8, 6],
    "Class B": [22, 25, 19, 30, 35, 28, 40, 42, 38, 29, 33, 31],
    "Class C": [100, 105, 110, 98, 120, 115, 130, 125, 140, 150, 135, 145]
}

# Function to compute five-number summary
def five_num_summary(data):
    minimum = np.min(data)
    q1 = np.percentile(data, 25)
    median = np.median(data)
    q3 = np.percentile(data, 75)
    maximum = np.max(data)
    return minimum, q1, median, q3, maximum

# Print five-number summaries for each group
print("📊 Five-Number Summaries:\n")
for name, values in data_groups.items():
    summary = five_num_summary(values)
    print(f"{name}: Min={summary[0]}, Q1={summary[1]}, Median={summary[2]}, Q3={summary[3]}, Max={summary[4]}")

# Plot multiple box plots
plt.figure(figsize=(8,6))
plt.boxplot(data_groups.values(), vert=True, patch_artist=True,
            labels=data_groups.keys(),
            boxprops=dict(facecolor="skyblue", color="navy"),
            medianprops=dict(color="red"))
plt.title("Box Plots for Multiple Classes")
plt.ylabel("Values")
plt.grid(True, axis="y", linestyle="--", alpha=0.7)
plt.show()
