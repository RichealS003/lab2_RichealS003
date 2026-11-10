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
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    #Setting/creating the total variables for both formative and summative. 
    #These variables will hold the required total weights of both formative and summative.
    formative_total = 0
    summative_total = 0

    #These variables will hold the actual total scores earned in both formative and summative.
    formative_earned = 0
    summative_earned = 0
    resubmission_options = []
    
    #This loop checks the score validation to make sure it falls within a percentage score(0 -100).
    for assignment in data:

        if assignment["score"] < 0 or assignment["score"] > 100:
            print("Score must be a percentage(Between 0 - 100).")
            return
        
        if assignment["group"] == "Formative":
            
            #Updating the formative_total variable with the individual weights, combining them to get a total.
            formative_total += assignment["weight"]

            #Created this variable to use to calculate the score actually earned in the formative by the student.
            stud_formative_score = (assignment["score"]/100) * assignment["weight"]

            #Updating the formative_earned variable with the individual actual scores earned in the formative, combining them to get a total.
            formative_earned += stud_formative_score
                
            # print(resubmission_options)


        elif assignment["group"] == "Summative":

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
        print(f"Student's formative score is {percent_score_formative}")

    else:
        print("Formative weights should be exactly 60. Please try again.")
        return

    #Calculating the summative percentage to determine if a student passes or fails.
    if summative_total == 40 and summative_earned <= 40:
        percent_score_summative = (summative_earned/summative_total) * 100
        print(f"Student's summative score is {percent_score_summative}")
    else:
        print("Summative weights should be exactly 40. Please try again.")
        return

    #Determining whether a student passes or fails and validating the total score to make sure it's not more than a hundred
    if total_weights == 100 and total_weights >= 0:
        if percent_score_formative >= 50 and percent_score_summative >= 50:
            print("PASSED")
        else:
            print("FAILED")
    else:
        print("Total weights should be exactly 100.")
        return

    #Calculating the GPA 
    GPA = (total_score_earned/100)*5.0
    print(GPA)

    #Resubmission logic
    #This collects the final assignments that are eligible for resubmission
    resubmission_assignments = []
    for assignment in data:
        if assignment["group"] == "Formative":
            if assignment["score"] < 50:
                resubmission_options.append(assignment)
    if resubmission_options:
        highest_weight = max(item["weight"] for item in resubmission_options)
        for item in resubmission_options:
            if item["weight"] == highest_weight:
                resubmission_assignments.append(item["assignment"])
    else:
        print("No assignments are available for resubmission.")

    print(f"Available for resubmission \n{', '.join(resubmission_assignments)}")


 


    print("\n--- Processing Grades ---")
    
    # TODO: a) Check if all scores are percentage based (0-100)
    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    # TODO: c) Calculate the Final Grade and GPA
    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
