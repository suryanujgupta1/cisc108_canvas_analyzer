"""
Project 4C
Canvas Analyzer
CISC108 Honors
Fall 2019

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.


"I have neither given nor received help on this assignment."
author: YOUR NAME HERE
"""
__version__ = 7
user = {
        "Name": "Hermione Granger",
        "Title": "Student",
        "Primary Email": "hgranger@hogwarts.edu",
        "Bio": "Interested in Magic, Learning, and House Elf Rights",
    }
# 1) main
import matplotlib.pyplot as plt
import canvas_requests
import datetime

def main (user_id):
    user = canvas_requests.get_user(user_id)
    print_user_info(user)
    #above is user info
    courses = canvas_requests.get_courses(user_id)
    filtered_courses = filter_available_courses(courses)
    print_courses(filtered_courses)
    #above is courses info
    course_ids = get_course_ids(courses)
    course_id = choose_course(course_ids)
    #above is course ids and course id info
    submissions = canvas_requests.get_submissions(user_id, course_id)
    summarize_points(submissions)
    summarize_groups(submissions)
    plot_scores(submissions)
    plot_grade_trends(submissions)
    #above is submissions info

'''
Consumes a string representing the user token (e.g., 'hermione') and calls all the other functions as shown in the 
diagram. The main function will be graded on Web-CAT based on the functions you have implemented; only include the 
functions you have implemented, but make sure you correctly call all the functions you do implement.
'''

# 2) print_user_info
def print_user_info(user:[dict]):
    print("Name: " + user["name"])
    print("Title: " +user["title"])
    print("Primary Email: " +user["primary_email"])
    print("Bio: " +user["bio"])

'''
Consumes a User dictionary and prints out the user's name, title, primary email, and bio. 
It does not return anything. Note: this function consumes a dictionary, not a string; 
it does NOT call the canvas_requests.get_user function, it consumes the result of calling 
the function.
'''

# 3) filter_available_courses
def filter_available_courses(classes:[dict])->[dict]:
    new={}
    for a_class in classes:
        if a_class["workflow_state"] is "available":
            new.append(a_class)
    return new

'''
Consumes a list of Course dictionaries and returns a list of Course dictionaries where the workflow_state key's 
value is 'available' (as opposed to 'completed' or something else).
'''

# 4) print_courses
def print_courses(courses:[dict]):
    for a_course in courses:
        print("\t", str(a_course["id"]) + " : " + a_course["name"])

'''
Consumes a list of Course dictionaries and prints out the ID and name of each course on separate lines.
'''

# 5) get_course_ids
def get_course_ids(courses:[dict])->[int]:
    new=[]
    for a_course in courses:
        new.append(a_course["id"])
    return new

'''
Consumes a list of Course dictionaries and returns a list of integers representing course IDs.
'''

# 6) choose_course
#numbers are  52,15,23, and 34. This function repeats until one of those #s in inputed. 
def choose_course(numbers:[int])->int:
  value=input("Enter course id: ")
  value=int(value)
  while value not in numbers:
    value=int(input("Enter course id: "))
  return value

'''
Consumes a list of integers representing course IDs and prompts the user to enter a valid ID, and then returns an 
integer representing the user's chosen course ID. If the user does not enter a valid ID, the function repeatedly 
loops until they type in a valid ID. You will need to use the input function to get the user's choice.
'''

# 7) summarize_points
def summarize_points(submissions:[dict]):
    points_obtained=0
    points_possible_so_far=0
    for a_sub in submissions:
        if a_sub["score"] is not None:
            group_weight = a_sub["assignment"]["group"]["group_weight"]
            score = a_sub["score"] * group_weight
            points_obtained += score
            current_grade = round(((points_obtained / score) * 100), 1)
            points = a_sub["assignment"]["points_possible"] * group_weight
            points_possible_so_far += points
        print("Current Grade: " + str(current_grade))
        print("Points possible so far: " + str(points_possible_so_far))
        print("Points Obtained: " + str(points_obtained))

'''
summarize_points: Consumes a list of Submission dictionaries and prints out three summary statistics about the 
submissions where there is a score (i.e. the submissions score is not None):
->Points possible so far: The sum of the assignments' points_possible multiplied by the assignment's group_weight.
->Points obtained: The sum of the submissions' score multiplied by the assignment's group_weight.
->Current grade: the Points obtained divided by the Points possible so far, multiplied by 100 and rounded. 
Note that you can use the built-in round function.
'''
# 8) summarize_groups
def summarize_groups(submissions:[dict]):
    group_score = {}
    group_points = {}
    for a_value in submissions:
        if a_value["score"] is not None:
            group_name = a_value["assignment"]["group"]["name"]
            if group_name not in group_score:
                group_score[group_name] = 0
                group_points[group_name] = 0
            group_score[group_name] += a_value["score"]
            group_points[group_name] += a_value["assignment"]["points_possible"]
    for a_name in group_score:
        score, points = group_score[a_name], group_points[a_name]
        print("*" + a_name + ":" + str(round((100*(score/points)))))

'''
Consumes a list of Submission dictionaries and prints out the group name and unweighted grade for each group.
The unweighted grade is the total score for the group's submissions divided by the total points_possible
for the group's submissions, multiplied by 100 and rounded. Like the summarize_points function, you should
ignore the submission without a score (i.e. the submission's score is None). You are recommended to apply the
Dictionary Summing Pattern to implement this function. This function is a little difficult, so you might want
to complete the next function first.
'''

# 9) plot_scores
import datetime
a_string_date = "2017-08-30T16:20:00Z"
due_at = datetime.datetime.strptime(a_string_date, "%Y-%m-%dT%H:%M:%SZ")

def plot_scores(submissions: [dict]):
    percent_of_scores = []
    for a_submission in submissions:
        if a_submission["assignment"]["points_possible"] and a_submission["score"] != None:
            percent_of_score = 100 * a_submission["score"] / a_submission["assignment"]["points_possible"]
            percent_of_scores.append(percent_of_score)
    plt.hist(percent_of_scores)
    plt.title("Distribution of Grades")
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.show()

'''
Consumes a list of Submission dictionaries and plots each submissions' grade as a histogram. 
The grade is calculated as the submission's score multiplied by 100 and divided by the assignment's points_possible. 
ou should only plot the submissions that have been graded (score is not None) and the assignment is worth more than 
0 points (points_possible is not truthy). Title your graph as "Distribution of Grades", label the X-axis as "Grades", 
and label the Y-axis as "Number of Assignments".
'''

# 10) plot_grade_trends
def plot_grade_trends (submissions:dict):
    lowest=[]
    highest=[]
    maximum=[]
    weight_score=0
    maxweight_score=0
    notgradedscore=0
    for a_sub in submissions:
        weightchanger=a_sub["assignment"]["group"]["group_weight"]
        score=0
        if a_sub["score"]:
            score=a_sub["score"]
        else:
            score=0
        weight_score+=score*weightchanger
        points_possible=a_sub["assignment"]["points_possible"]
        if a_sub["graded_at"] is not None:
            notgradedscore+=points_possible*weightchanger
        else:
            notgradedscore+=score*weightchanger
        maximum=[avalue/maxweight_score for avalue in maximum]
        lowest=[avalue/maxweight_score for avalue in lowest]
        maximum=[avalue/maxweight_score for avalue in highest]
        running_dates=[]
        print(maximum)
        print(maxweight_score)
        for a_sub in submissions:
            running_dates.append(a_sub["assignment"]["due_at"])
            plt.plot(running_dates, highest, label="Highest")
            plt.plot(running_dates, lowest, label="Lowest")
            plt.plot(running_dates, maximum, label="Maximum")
            plt.title("Grade Trend")
            plt.ylabel("Grade")
            plt.show()

'''
Consumes a list of Submission dictionaries and plots the grade trend of the submissions as a line plot.
The grade trend contains three lines (ordered by the assignments' due_at date) that show you the range of grades you
could get in the course:
->Highest: The running sum of graded submission scores followed by the running sum of points still possible from ungraded assignments.
->Lowest: The running sum of graded submission scores followed by the running sum if you scored 0 on all ungraded assignments.
->Maximum: The running sum of the points possible on all assignments in the course.
'''

# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.
if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')
    
    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')