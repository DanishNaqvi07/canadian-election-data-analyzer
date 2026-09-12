import csv
import argparse


# helper function used for sorting
# basically tells Python what value we want to sort the list by
def get_ratio(item):
    return item["Ratio"]


def process_file(input_file, output_file):
    data = []  # this will store all the processed province data

    # open the CSV file and read it using DictReader so we can access columns by name
    with open(input_file, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                # grab the columns we actually care about from the dataset
                province = row["Province"]

                # remove commas just in case the dataset has numbers like "1,234,567"
                # then convert them into integers so we can actually do math with them
                population = int(row["Population"].replace(",", ""))
                electors = int(row["Electors"].replace(",", ""))
                polling_stations = int(row["Total Polling Stations"].replace(",", ""))

                # calculate the ratio described in our milestone
                # (population / electors) * 100
                if electors > 0:
                    ratio = (population / electors) * 100
                else:
                    ratio = 0  # just a safety check to avoid division by zero

                # store everything we need for later sorting/output
                data.append({
                    "Province": province,
                    "Ratio": ratio,
                    "PollingStations": polling_stations
                })

            except (KeyError, ValueError):
                # if a row has missing or bad data, we just skip it
                # this keeps the program from crashing
                continue

    # sort the provinces from highest ratio to lowest
    # we use the helper function instead of lambda so it's clearer
    data.sort(key=get_ratio, reverse=True)

    # now write the results to a new CSV file
    with open(output_file, "w", newline='', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)

        # header row
        writer.writerow(["Province", "Population/Electors (%)", "Total Polling Stations"])

        # write each processed province row
        for row in data:
            writer.writerow([
                row["Province"],
                f"{row['Ratio']:.2f}",  # round to 2 decimal places
                row["PollingStations"]
            ])


def main():
    # argparse lets us pass the input file when running the script
    parser = argparse.ArgumentParser(description="Process election CSV data")

    parser.add_argument("input_file", help="Input CSV file")

    # optional output file argument (defaults to highest_polling_provinces.csv)
    parser.add_argument(
        "-o",
        "--output",
        default="highest_polling_provinces.csv",
        help="Output CSV file"
    )

    args = parser.parse_args()

    # run the main processing function
    process_file(args.input_file, args.output)


# standard Python entry point
if __name__ == "__main__":
    main()