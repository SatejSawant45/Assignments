# Dataset: (Attribute Value, Support in Target Class, Support in Contrasting Class)
data = [
    ("CS", 40, 15),
    ("Math", 30, 25),
    ("Physics", 20, 35),
    ("Biology", 25, 10),
    ("Chemistry", 15, 20),
    ("Economics", 10, 30)
]

# Total tuples in target class
total_target = sum([row[1] for row in data])

print("Attribute\tTarget\tContrast\tt-weight\td-weight")
print("-"*65)

for attr, target_support, contrast_support in data:
    # Calculate t-weight
    t_weight = target_support / total_target
    
    # Calculate d-weight
    d_weight = target_support / (target_support + contrast_support)
    
    # Print results
    print(f"{attr:10}\t{target_support}\t{contrast_support}\t{t_weight:.2f}\t\t{d_weight:.2f}")
