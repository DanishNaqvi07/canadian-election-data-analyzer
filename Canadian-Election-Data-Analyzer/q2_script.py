import csv
import argparse
import plotly.express as px


#helper function for sorting
#this tells python to sort using the percentage value
def get_ratio(item):
    return item["Ratio"]


def process_file(input_file, output_file):
    data = []

    #open the csv and read each row by column name
    with open(input_file, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                #get the province name and clean up extra spaces
                province = row["Province"].strip()

                #skip blank rows just in case
                if province == "":
                    continue

                #get the values we actually need from the table
                population = int(row["Population"].replace(",", "").strip())
                electors = int(row["Electors/Électeurs"].replace(",", "").strip())
                polling_stations = int(row["Total Polling Stations/Total des bureaux"].replace(",", "").strip())

                #avoid division by zero
                if population > 0:
                    #this calculates the percentage of electors relative to the population
                    ratio = (electors / population) * 100
                else:
                    ratio = 0

                #store everything in a dictionary so it is easy to sort and write later
                data.append({
                    "Province": province,
                    "Ratio": ratio,
                    "PollingStations": polling_stations
                })

            except (KeyError, ValueError):
                #if a row is missing data or has bad formatting just skip it
                continue

    #sort from highest percentage to lowest
    data.sort(key=get_ratio, reverse=True)

    #write the results into a new csv file
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)

        #header row
        writer.writerow(["Province", "Electors/Population (%)", "Total Polling Stations"])

        #write each province row
        for row in data:
            writer.writerow([
                row["Province"],
                f"{row['Ratio']:.2f}",
                row["PollingStations"]
            ])

    #make interactive bar graph
    provinces = [row["Province"] for row in data]
    ratios = [row["Ratio"] for row in data]
    polling_stations = [row["PollingStations"] for row in data]

    fig = px.bar(
        x=provinces,
        y=ratios,
        hover_data={
            "Province": provinces,
            "Electors/Population (%)": [f"{value:.2f}" for value in ratios],
            "Total Polling Stations": polling_stations
        },
        labels={
            "x": "Province",
            "y": "Electors/Population (%)"
        },
        title="Electors as a Percentage of Population by Province/Territory"
    )

    fig.update_layout(xaxis_tickangle=-45)
    fig.show()


def main():
    #lets us pass the input file in the terminal
    parser = argparse.ArgumentParser(description="process election csv data")
    parser.add_argument("input_file", help="input csv file")
    parser.add_argument(
        "-o",
        "--output",
        default="highest_polling_provinces.csv",
        help="output csv file"
    )

    args = parser.parse_args()

    process_file(args.input_file, args.output)


#if this file is run directly, start the program
if __name__ == "__main__":
    main()