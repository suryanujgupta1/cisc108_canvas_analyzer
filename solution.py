# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 12:12:37 2017

@author: acbart
"""
__version__ = 7

import canvas_requests
import matplotlib.pyplot as plt
from datetime import datetime


# 1
def print_user_info(user):
    '''
    Prints information about the user such as their name and title.

    Parameters:
        user (str): A user token
    Returns: None
    '''
    print("Name:", user['name'])
    print("Title:", user['title'])
    print("Primary Email:", user['primary_email'])
    print("Bio:", user['bio'])


# 2
def filter_available_courses(courses):
    '''
    Removes courses that are not available to the user.

    Parameters:
        courses (list of dict): A list of course dictionaries
    Returns: list of dict
    '''
    valid = []
    for course in courses:
        if course['workflow_state'] == 'available':
            valid.append(course)
    return valid


# 3
def print_courses(courses):
    """
    Iterates through the list of courses and prints the ID and name
    of each course

    Parameters:
        courses (list of dict): A list of course dictionaries
    Returns: None
    """
    for course in courses:
        print("\t", course["id"], ":", course["name"])


# 4
def get_course_ids(courses):
    """
    Iterates through the list of courses and extracts out their
    IDs.

    Parameters:
        courses (list of dict): A list of course dictionaries
    Returns: list of int
    """
    ids = []
    for course in courses:
        ids.append(course['id'])
    return ids


# 5
def choose_course(course_ids):
    """
    Prompts the user for a course ID and then returns it if it is
    one of the valid course IDs given.

    Parameters:
        course_ids (list of int): A list of course IDs
    Returns: int
    """
    PROMPT = "Choose a course from the list above:"
    chosen = None
    while chosen not in course_ids:
        chosen = int(input(PROMPT))
    return chosen


# 6
def summarize_points(submissions):
    """
    Prints out summary statistics for the student, including:
        How many points they have obtained
        How many points were possible in the course
        Their current final grade in the course

    Parameters:
        submissions (list of dict): A list of submission dictionaries
    Returns: None
    """
    possible = 0
    score = 0
    for sub in submissions:
        if sub['score'] is not None:
            points_possible = sub['assignment']['points_possible']
            group_weight = sub['assignment']['group']['group_weight']
            possible += points_possible * group_weight
            score += sub['score'] * group_weight
    print("Points possible so far:", possible)
    print("Points obtained:", score)
    print("Current grade:", round(100 * score / possible))


# 7
def summarize_groups(submissions):
    """
    Prints out the students' current grade for each group category.

    Parameters:
        submissions (list of dict): A list of submission dictionaries
    Returns: None
    """
    group_score = {}
    group_points = {}
    for sub in submissions:
        if sub['score'] is not None:
            group_name = sub['assignment']['group']['name']
            if group_name not in group_score:
                group_score[group_name] = 0
                group_points[group_name] = 0
            group_score[group_name] += sub['score']
            group_points[group_name] += sub['assignment']['points_possible']
    for name in group_score:
        score, points = group_score[name], group_points[name]
        print("*", name, ":", round(100 * score / points))


# 8
def plot_scores(submissions):
    '''
    Makes a histogram of the students' scores across all submitted
    assignments.

    Parameters:
        submissions (list of dict): A list of submission dictionaries
    Returns: None
    '''
    percent_scores = []
    for s in submissions:
        if s['assignment']['points_possible'] and s['score'] != None:
            percent_score = 100 * s['score'] / s['assignment']['points_possible']
            percent_scores.append(percent_score)
    plt.hist(percent_scores)
    plt.title("Distribution of Grades")
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.show()


# Helper function
def parse_date(a_date):
    '''
    Converts a date/time from a string into a datetime object.
    The string representation is assumed to be the regular Canvas one:
        YYYY/MM/DDTHH:MM:DDZ

    Parameters:
        a_date (str): A string representation of a date

    Returns:
        datetime: A Python datetime object
    '''
    return datetime.strptime(a_date, "%Y-%m-%dT%H:%M:%SZ")


# 8
def plot_grade_trends(submissions):
    '''
    For a given course and user, creates plots of a students' submissions
    in a course.

    Parameters:
        submissions (list of dict): A list of submission dictionaries
    Returns: None
    '''
    weighted_score = 0
    max_weighted_score = 0
    ungraded_max = 0
    running_low = []
    running_high = []
    running_max = []
    for s in submissions:
        # Group
        weighted_modifier = s['assignment']['group']['group_weight']
        # Score
        score = 0
        if s['score']:
            score = s['score']
        weighted_score += score * weighted_modifier
        # Points possible
        points_possible = s['assignment']['points_possible']
        if not s['graded_at']:
            ungraded_max += points_possible * weighted_modifier
        else:
            ungraded_max += score * weighted_modifier
        max_weighted_score += points_possible * weighted_modifier
        # Running sums
        running_low.append(100 * weighted_score)
        running_max.append(100 * max_weighted_score)
        running_high.append(100 * ungraded_max)
    print(running_max)
    print(max_weighted_score)
    # Normalize by maximum score
    running_high = [s / max_weighted_score for s in running_high]
    running_low = [s / max_weighted_score for s in running_low]
    running_max = [s / max_weighted_score for s in running_max]
    # Dates
    running_dates = []
    for s in submissions:
        running_dates.append(parse_date(s['assignment']['due_at']))
    # Plot trends
    plt.plot(running_dates, running_high, label="Highest", linestyle='--')
    plt.plot(running_dates, running_low, label="Lowest", linestyle='--')
    plt.plot(running_dates, running_max, label="Maximum")
    # Graphical styling
    plt.xticks(rotation=45)
    plt.legend(loc=(0, .5))
    plt.ylabel("Grade")
    plt.title("Grade Trend")
    plt.show()


# 10
def main(user_id):
    '''
    For a given user, displays information about one of their canvas courses.

    Parameters:
        user (str): A user token
    Returns: None
    '''
    # User
    user = canvas_requests.get_user(user_id)
    print_user_info(user)
    # Course
    courses = canvas_requests.get_courses(user_id)
    available_courses = filter_available_courses(courses)
    print_courses(available_courses)
    course_ids = get_course_ids(available_courses)
    course_id = choose_course(course_ids)
    # Submissions
    submissions = canvas_requests.get_submissions(user_id, course_id)
    # Statistics
    summarize_points(submissions)
    summarize_groups(submissions)
    # Plots
    plot_scores(submissions)
    plot_grade_trends(submissions)


if __name__ == "__main__":
    main('hermione')





































