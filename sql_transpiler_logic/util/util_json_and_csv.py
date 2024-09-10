import csv
import json


def read_json_file(_json_filename: str):
    with open(_json_filename, "r") as json_file:
        json_content = json.load(json_file)

    return json_content


def write_json_file(_json_filename: str, content):
    with open(_json_filename, "w") as _json_file:
        json.dump(content, _json_file, indent=4)


def write_csv_file(filename: str, content):
    """
    Writes the given data to a CSV file.

    Args:
    data: A list of dictionaries, where each dictionary represents a row in the CSV file.
    filename: The name of the CSV file to write to.
    """

    with open(filename, 'w', newline='') as csv_file:
        fieldnames = list(content[0].keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in content:
            writer.writerow(row)