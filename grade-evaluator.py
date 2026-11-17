import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    empty_rows = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            #Making sure that any csv file would still run with this code if the headings had different capitalizations
            reader.fieldnames = [header.strip().lower() for header in reader.fieldnames]
            row_number = 1
            for row in reader:
                row_number += 1
                #This checks for a blank row 
                for value in row.values():
                    if value is not None and value != '':
                        break
                else:
                    print(f"Row {row_number} is blank. Skipping...")
                    continue
                for field in ['assignment', 'group', 'score', 'weight']:
                    #This finds individual empty rows/fields and appends them to the empty_rows list
                    if row[field] is None or row[field].strip() == '':
                        empty_rows.append(f"{field} field in row {row_number}")   
                #This makes it easy to print the empty rows, showing the user exactly which fields are empty    
                if empty_rows:
                    for item in empty_rows:
                        print(f"The {item} contains no data. Please try again.")
                    sys.exit(1)         
                # Convert numeric fields to floats for calculations
                try:
                    score = float(row['score'])
                except ValueError:
                    print(f"{row['assignment']}'s score field must be a number. Please try again.")
                    sys.exit(1)

                try:
                    weight = float(row['weight'])
                except ValueError:
                    print(f"{row['assignment']}'s weight field must be a number. Please try again.")
                    sys.exit(1)
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': score,
                    'weight': weight
                })
        #This checks whether or not the assignments list is empty. An empty list means that the specified input file is empty.        
        if not assignments:
            print(f"{filename} is empty. Please choose a file that contains the appropriate data.")
            sys.exit(1)

        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
   
    #Setting/creating variables for both formative and summative. 
    #These variables will hold the required total weights of both formative and summative.
    formative_total = 0
    summative_total = 0

    #These variables will hold the actual total scores earned in either formative and summative.
    formative_earned = 0
    summative_earned = 0
    resubmission_options = []
    
    #This loop checks the score validation to make sure it falls within a percentage score(0 -100).
    for assignment in data:

        if assignment["score"] < 0 or assignment["score"] > 100:
            print("Score must be a percentage(Between 0 - 100).")
            return

        if assignment["weight"] <= 0 or assignment["weight"] > 100:
            print("Weight must be a positive number greater than zero")
            return
        #Making sure it is case insensitive and accepts spaces with the word
        if assignment["group"].strip().lower() == "formative":
            
            #Updating the formative_total variable with the individual weights, combining them to get a total.
            formative_total += assignment["weight"]

            #Created this variable to use to calculate the score actually earned in the formative by the student.
            stud_formative_score = (assignment["score"]/100) * assignment["weight"]

            #Updating the formative_earned variable with the individual actual scores earned in the formative, combining them to get a total.
            formative_earned += stud_formative_score

        #Making sure it is case insensitive and accepts spaces with the word
        elif assignment["group"].strip().lower() == "summative":

            #Updating the summative_total variable with the individual weights, combining them to get a total.
            summative_total += assignment["weight"]

            #Created this variable to use to calculate the score actually earned in the summative.
            stud_summative_score = (assignment["score"]/100) * assignment["weight"]

            #Updating the summative_earned variable with the individual actual scores earned in the summative, combining them to get a total.
            summative_earned += stud_summative_score

        else:

            print("Something isn't right. Please try again.")
            return
    #These variables contain the total weights and actual scores respectively, to be used later in the program.
    total_weights = summative_total + formative_total
    total_score_earned = formative_earned + summative_earned
    
    #Calculating the formative percentage to determine if a student passes or fails.
    if formative_total == 60 and formative_earned <= 60:
        percent_score_formative = (formative_earned/formative_total) * 100
        # print(f"Student's formative score is {percent_score_formative}")

    else:
        print("Formative weights should be exactly 60. Please try again. Exiting program.")
        return

    #Calculating the summative percentage to determine if a student passes or fails.
    if summative_total == 40 and summative_earned <= 40:
        percent_score_summative = (summative_earned/summative_total) * 100
    else:
        print("Summative weights should be exactly 40. Please try again. Exiting program.")
        return

    #Determining whether a student passes or fails and validating the total score to make sure it's not more than a hundred
    if total_weights == 100 and total_weights >= 0:
        if percent_score_formative >= 50 and percent_score_summative >= 50:
            status = "PASSED"
        else:
            status = "FAILED"

    else:
        print("Total weights should be exactly 100. Exiting program.")
        return

    #Calculating the GPA 
    GPA = (total_score_earned/100)*5.0

    #Resubmission logic
    #This collects the final assignments that are eligible for resubmission
    resubmission_assignments = []
    for assignment in data:
        if assignment["group"].strip().lower() == "formative":
            if assignment["score"] < 50:
                resubmission_options.append(assignment)
    if resubmission_options:
        highest_weight = max(item["weight"] for item in resubmission_options)
        for item in resubmission_options:
            if item["weight"] == highest_weight:
                resubmission_assignments.append(item["assignment"])

    print(f"\n--- Processing Grades ---\n")

    print(f"Final Transcript\n")
    print(f"{'Assignment':<50} {'Category':<10} {'Grade(%)':>15} {'Weight':>12} {'Final Weight':>19}\n")
    for assignment in data:
        #The final weight variable her makes it easy for me to get the final weight without having to figure out a way to use the stud_formative or stud_summative scores variables.
        final_weight = (assignment['score']/100)*assignment['weight']
        print(f"{assignment['assignment']:<50} {assignment['group']:<10} {assignment['score']:>15} {assignment['weight']:>12} {final_weight:>19.2f}\n")
    print(f"{'Formatives(60)':<50} {formative_earned:>60.1f}")
    print(f"{'Summatives(40)':<50} {summative_earned:>60.1f}")
    print(f"{'GPA':<50} {GPA:>60.2f}")
    print(f"\n")
    print(f"{'Status':<50} {status:>60}")
    print(f"{'Available for resubmission':<50} {', '.join(resubmission_assignments):>60}\n")



if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
