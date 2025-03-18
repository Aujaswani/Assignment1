#!/usr/bin/env python3
'''
OPS445 Assignment 1 - Winter 2025
Program: assignment1.py 
Author: Aujaswani Rajput
The python code in this file (a1_[Student_id].py) is original work written by
Aujaswani Rajput. No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.
'''
 


import sys
from datetime import datetime, timedelta



def day_of_week(year: int, month: int, date: int) -> str:
    """Based on the algorithm by Tomohiko Sakamoto to calculate the day of the week."""
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    offset = {1: 0, 2: 3, 3: 2, 4: 5, 5: 0, 6: 3, 7: 5, 8: 1, 9: 4, 10: 6, 11: 2, 12: 4}
    
    if month < 3:
        year -= 1  # Adjust the year for January and February
    
    num = (year + year // 4 - year // 100 + year // 400 + offset[month] + date) % 7
    return days[num]

def mon_max(month, year):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if leap_year(year) else 28
    else:
        return 0


def after(date: str) -> str:
    
    str_year, str_month, str_day = date.split('-')
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)
    
    tmp_day = day + 1  # next day
    
    if tmp_day > mon_max(month, year):
        to_day = tmp_day % mon_max(month, year)  
        tmp_month = month + 1
    else:
        to_day = tmp_day
        tmp_month = month + 0
    
    if tmp_month > 12:
        to_month = 1
        year = year + 1
    else:
        to_month = tmp_month + 0
    
    next_date = f"{year}-{to_month:02}-{to_day:02}"
    
    return next_date


def usage():
    print("Usage: python3 assignment1.py [options]")
    print("Options:")
    print("  -d, --date <YYYY-MM-DD>       Print the day of the week for the given date")
    print("  -a, --after <YYYY-MM-DD>      Print the date for the next day of the given date")
    print("  -l, --leap <year>             Check if the given year is a leap year")
    print("  -v, --valid <YYYY-MM-DD>      Check if the given date is valid")
    print("  -c, --count <start_date> <stop_date>  Count the number of weekend days between the given dates")
    print("  OR: simply provide two dates without flags to count weekend days.")

def leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)



def valid_date(date: str) -> bool:
    if len(date) != 10 or date[4] != '-' or date[7] != '-':
        return False
    
    year, month, day = date.split('-')
    
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False
    
    year, month, day = int(year), int(month), int(day)
    
    if month < 1 or month > 12:
        return False
    
    max_day = mon_max(month, year)
    if day < 1 or day > max_day:
        return False
    
    return True

def day_count(start_date: str, stop_date: str) -> int:
    start_year, start_month, start_day = map(int, start_date.split('-'))
    end_year, end_month, end_day = map(int, stop_date.split('-'))
    
    start = datetime(start_year, start_month, start_day)
    end = datetime(end_year, end_month, end_day)
    
    if start > end:
        start, end = end, start
    
    count = 0
    while start <= end:
        if start.weekday() in [5, 6]:
            count += 1
        start += timedelta(days=1)
    
    return count

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        usage()
        return

    if args[0] in ("-d", "--date") and len(args) == 2:
        date = args[1]
        if valid_date(date):
            y, m, d = date.split('-')
            print(day_of_week(int(y), int(m), int(d)))
        else:
            usage()

    elif args[0] in ("-a", "--after") and len(args) == 2:
        date = args[1]
        if valid_date(date):
            print(after(date))
        else:
            usage()

    elif args[0] in ("-l", "--leap") and len(args) == 2:
        year = int(args[1])
        print("Yes" if leap_year(year) else "No")

    elif args[0] in ("-v", "--valid") and len(args) == 2:
        print("Valid" if valid_date(args[1]) else "Invalid")

    elif (args[0] in ("-c", "--count") and len(args) == 3) or len(args) == 2:
        # Either using count flag or just two dates without flags
        start, end = args[-2], args[-1]
        if valid_date(start) and valid_date(end):
            dates = sorted([start, end])
            count = day_count(dates[0], dates[1])
            print(f"The period between {dates[0]} and {dates[1]} includes {count}")
        else:
            usage()
    else:
        usage()

if __name__ == "__main__":
    main()