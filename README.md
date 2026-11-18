# ALU Transcript Generator

## 1. Project Overview

The ALU Transcript Generator is a Python and Bash-based project designed to process student assignment grades, calculate academic performance, and organize grade records.

The Python program reads assignment data from a CSV file, validates the input, calculates weighted grades and GPA, determines the student's academic status, and identifies eligible formative assignments for resubmission.

The Bash script manages the grade records by archiving an existing `grades.csv` file and creating a new empty CSV file for future records.

## 2. Project Features

- Reads student assignment records from a CSV file.
- Accepts CSV headers with different capitalization and surrounding spaces.
- Checks for missing files, blank rows, and empty fields.
- Validates that scores are between 0 and 100.
- Validates that assignment weights are positive and do not exceed 100.
- Calculates weighted formative and summative scores.
- Ensures that formative assignments total 60% and summative assignments total 40%.
- Calculates the student's overall GPA on a 5.0 scale.
- Determines whether the student passes or fails.
- Identifies formative assignments below 50% that qualify for resubmission consideration.
- Selects the eligible formative assignment or assignments with the highest weight.
- Archives previous grade records using a Bash script.

## 3. Project Structure

The project uses the following files:

```text
ALU-Transcript-Generator/
│
├── grade_evaluator.py
├── organizer.sh
├── grades.csv
├── organizer.log
└── archive/
```

| File or directory | Purpose |
|---|---|
| `grade_evaluator.py` | Reads, validates, and evaluates student grades. |
| `organizer.sh` | Archives existing grade records and creates a new CSV file. |
| `grades.csv` | Contains assignment names, categories, scores, and weights. |
| `organizer.log` | Records details of the archiving operation. |
| `archive/` | Stores previously archived grade files. |

## 4. CSV Input Format

The grade evaluator expects a CSV file containing four required columns:

| Column | Description |
|---|---|
| `assignment` | Name of the assignment. |
| `group` | Assignment category: Formative or Summative. |
| `score` | Student's score as a percentage. |
| `weight` | Percentage weight assigned to the assessment. |

Example:

```csv
assignment,group,score,weight
Assignment 1,Formative,80,20
Assignment 2,Formative,65,20
Assignment 3,Formative,75,20
Assignment 4,Summative,70,20
Assignment 5,Summative,80,20
```

The evaluator normalizes CSV headers by removing surrounding spaces and converting them to lowercase.

For example, `ASSIGNMENT`, `Assignment`, and ` assignment ` are recognized as `assignment`.

## 5. Python Grade Evaluator

### `load_csv_data()`

This function handles the input and validation process.

Its responsibilities include:

- Prompting the user to enter a CSV filename.
- Checking whether the specified file exists.
- Opening and reading the CSV file using `csv.DictReader`.
- Normalizing the CSV headers.
- Skipping completely blank rows.
- Checking required fields for missing values.
- Converting scores and weights into numeric values.
- Reporting invalid numeric inputs.
- Returning validated assignment records as a list of dictionaries.

### `evaluate_grades(data)`

This function processes the assignment records and calculates the student's academic performance.

**A. Score validation**

Each assignment score must fall between 0 and 100.

**B. Weight validation**

Each assignment weight must be greater than zero and must not exceed 100.

**C. Category weight validation**

The assessment weights must satisfy the following requirements:

| Assessment category | Required total weight |
|---|---:|
| Formative | 60% |
| Summative | 40% |
| Overall | 100% |

**D. Weighted score calculation**

The weighted contribution of an assignment is calculated using:

Weighted Contribution = (Score / 100) × Assignment Weight

The program accumulates the weighted contributions separately for formative and summative assessments.

**E. Category percentage calculation**

The formative and summative percentages are calculated separately to determine whether the student meets the minimum passing requirement.

**F. GPA calculation**

The GPA is calculated on a 5.0 scale:

GPA = (Total Weighted Grade / 100) × 5.0

**G. Pass/fail determination**

A student passes only when both conditions are satisfied:

- Formative percentage is at least 50%.
- Summative percentage is at least 50%.

If either category falls below 50%, the student's status is FAILED.

**H. Resubmission eligibility**

The program checks formative assignments with scores below 50%.

Among those assignments, it identifies the assignment or assignments with the highest weight. Where multiple eligible assignments share the highest weight, all are included in the resubmission list.

## 6. Transcript Output

The evaluator displays a transcript containing:

- Assignment name
- Assessment category
- Grade percentage
- Assignment weight
- Final weighted contribution
- Formative weighted score
- Summative weighted score
- GPA
- Final academic status
- Available resubmission assignments

## 7. Bash Grade File Organizer

The `organizer.sh` script automates the management of grade records.

Its operations include:

1. Checking whether an `archive` directory exists.
2. Creating the directory if it does not exist.
3. Generating a timestamp.
4. Renaming and moving the existing `grades.csv` file into the archive directory.
5. Creating a new empty `grades.csv` file.
6. Appending the timestamp and archiving details to `organizer.log`.

Archived filenames follow this format:

```text
grades_YYYYMMDD-HHMMSS.csv
```

## 8. Technologies Used

- **Python 3:** CSV processing, data validation, grade calculations, and transcript generation.
- **Bash:** File management, archiving, timestamp generation, and log recording.
- **CSV:** Storage format for assignment records.

No external Python libraries are required.

## 9. How to Run the Project

### Step 1: Prepare the CSV file

Ensure that your `grades.csv` file contains the required columns:

`assignment`, `group`, `score`, and `weight`.

### Step 2: Run the Python evaluator

From the project directory, execute:

```bash
python3 grade_evaluator.py
```

When prompted, enter the name of the CSV file you want to process.

### Step 3: Run the Bash organizer

To archive the current grade records and create a fresh CSV file, execute:

```bash
bash organizer.sh
```

The script will perform the archiving and logging operations.

## 10. Project Learning Objectives

This project demonstrates practical skills in:

- Python file handling and CSV processing.
- Data validation and exception handling.
- Lists and dictionaries.
- Loops and conditional statements.
- Functions and modular programming.
- Mathematical calculations and percentage-based grading.
- Bash scripting and command-line operations.
- File and directory management.
- Timestamp generation and logging.

## 11. Conclusion

The ALU Transcript Generator combines Python programming and Bash scripting to demonstrate how student grade records can be processed, evaluated, and organized.

The project applies input validation, weighted grade calculations, academic performance evaluation, resubmission identification, and automated file archiving in a single workflow.
