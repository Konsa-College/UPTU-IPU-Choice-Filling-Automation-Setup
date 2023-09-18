import csv
import os
import shutil

# Define the input and output directories
input_dir = "./input_files/"
output_dir = "./output_files/"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the CSV file
csv_file = "data.csv"

with open(csv_file, mode="r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        email = row["email"]
        category = row["category"]

        # Check the category and set the source file accordingly
        if category == "fw":
            source_file = os.path.join(input_dir, "fw.pdf")
        elif category == "nofw":
            source_file = os.path.join(input_dir, "nofw.pdf")
        else:
            continue  # Skip if category is neither fw nor nofw

        # Remove "@" symbol from email and construct the destination file path

        # Modify the destination file name based on category
        if category == "fw":
            destination_file = os.path.join(output_dir, f"{email}_fw.pdf")
        else:
            destination_file = os.path.join(output_dir, f"{email}.pdf")

        # Copy the source file to the destination
        shutil.copyfile(source_file, destination_file)

print("Files copied successfully with modified filenames!")
