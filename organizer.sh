#!/usr/bin/env bash

if [[ ! -d "archive" ]]; then
    mkdir archive
    echo -e "Creating archive directory...\n"
else
    echo -e "Directory already exists\n"
fi

#Variable containing the timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

#Variable containing new file name for the grades.csv file.
archive_filename="grades_${timestamp}.csv"
# echo "$archive_filename"

if [[ -f "grades.csv" ]]; then
    mv grades.csv archive/$archive_filename
else
    echo -e "grades.csv file does not exist.\n"
    exit 1
fi

echo -e "Creating new csv file...\n"
touch grades.csv

echo -e "Appending archiving details to a log file...\n"
echo -e "Timestamp: $timestamp\n""Original file name: grades.csv\n""New archived filename: $archive_filename\n" >> organizer.log

echo -e "All done.\n"