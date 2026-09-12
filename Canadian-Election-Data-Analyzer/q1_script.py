# Question 1: Between the 43rd (2019) and 44th (2021) Canadian Federal
# Elections, was there a measurable change in the number of female MPs
# elected across political parties and provinces?
#
# Usage:
#   python3 q1_script.py province Ontario
#   python3 q1_script.py province All
#   python3 q1_script.py party Liberal

import sys
import csv

FILE_43 = "table7_43rd.csv"
FILE_44 = "table7_44th.csv"

# read command line arguments
if len(sys.argv) != 3:
    print("Usage: python3 q1_script.py <province|party> <value>")
    print("Example: python3 q1_script.py province Ontario")
    print("Example: python3 q1_script.py party Liberal")
    sys.exit()

filter_type = sys.argv[1].lower()   # either "province" or "party"
filter_value = sys.argv[2]          # e.g. "Ontario" or "Liberal"

if filter_type != "province" and filter_type != "party":
    print("First argument must be 'province' or 'party'")
    sys.exit()


# function to read one CSV file and return a list of rows
def read_csv(filename, year):
    rows = []
    with open(filename, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            province = row.get("Province", "").strip()
            party = row.get("Political Affiliation", "").strip()
            female = row.get("Female", "0").strip()

            # skip blank or summary rows
            if province == "" or province.lower() == "total" or province.lower() == "canada":
                continue

            # convert female seats to a number
            if female == "" or female == "-":
                female = 0
            else:
                female = int(female)

            rows.append({
                "province": province,
                "party": party,
                "female": female,
                "year": year
            })
    return rows


data = []
data = data + read_csv(FILE_43, 2019)
data = data + read_csv(FILE_44, 2021)

# filter the data based on user input
filtered = []
for row in data:
    if filter_type == "province":
        if filter_value.lower() == "all" or row["province"].lower() == filter_value.lower():
            filtered.append(row)
    else:
        if filter_value.lower() == "all" or row["party"].lower() == filter_value.lower():
            filtered.append(row)

if len(filtered) == 0:
    print("No results found for: " + filter_value)
    sys.exit()

# if filtering by province, group by party (and vice versa)
if filter_type == "province":
    group_by = "party"
else:
    group_by = "province"

# add up female seats per group per year
totals_2019 = {}
totals_2021 = {}

for row in filtered:
    group_name = row[group_by]

    if row["year"] == 2019:
        if group_name not in totals_2019:
            totals_2019[group_name] = 0
        totals_2019[group_name] = totals_2019[group_name] + row["female"]

    if row["year"] == 2021:
        if group_name not in totals_2021:
            totals_2021[group_name] = 0
        totals_2021[group_name] = totals_2021[group_name] + row["female"]

# combine into one list with change calculated
all_groups = set(list(totals_2019.keys()) + list(totals_2021.keys()))

results = []
for group_name in all_groups:
    seats_2019 = totals_2019.get(group_name, 0)
    seats_2021 = totals_2021.get(group_name, 0)
    change = seats_2021 - seats_2019
    results.append([group_name, seats_2019, seats_2021, change])

# sort by change descending (biggest improvement first)
results.sort(key=lambda x: x[3], reverse=True)

# print the results table
label = group_by.capitalize()

print("")
print("=" * 62)
print("  Q1 - Female MPs Elected  |  " + filter_type.capitalize() + ": " + filter_value)
print("  43rd Election (2019)  vs  44th Election (2021)")
print("=" * 62)
print("  " + label.ljust(26) + "  2019    2021  Change")
print("  " + "-" * 26 + "  ----    ----  ------")

total_2019 = 0
total_2021 = 0

for row in results:
    name = row[0]
    seats_2019 = row[1]
    seats_2021 = row[2]
    change = row[3]

    if change > 0:
        change_str = "+" + str(change)
    else:
        change_str = str(change)

    print("  " + name.ljust(26) + "  " + str(seats_2019).rjust(4) + "    " + str(seats_2021).rjust(4) + "  " + change_str.rjust(6))

    total_2019 = total_2019 + seats_2019
    total_2021 = total_2021 + seats_2021

total_change = total_2021 - total_2019
if total_change > 0:
    total_change_str = "+" + str(total_change)
else:
    total_change_str = str(total_change)

print("  " + "-" * 26 + "  ----    ----  ------")
print("  " + "TOTAL".ljust(26) + "  " + str(total_2019).rjust(4) + "    " + str(total_2021).rjust(4) + "  " + total_change_str.rjust(6))
print("=" * 62)
print("")
