import time
import pandas as pd
import numpy as np
import datetime
import calendar
import os

os.chdir('c:/Users/lasse/Desktop/Udacity/Udacity_Python')
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # define city as a global variable to use it in other functions as input
    global city
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    
    while True:
        city_input = input("""Please choose a city and enter "c": chicago, "n": new york city or "w": washington: """)
        if city_input.lower() not in ('c', 'n', 'w'):
            print("""Sorry this was not a valid input for a city, please choose a city and enter "c": chicago, "n": new york city or "w": washington: """)
            continue
        else:
            if city_input.lower() == "c":
                city = "chicago"
            elif city_input.lower() == "n":
                city = "new york city"
            elif city_input.lower() == "w":
                city = "washington"
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        filter_yes_no = input("""Do you want to filter by month (yes) or do you want to apply no month based filter (no)? Enter: "yes" or "no": """)
        if filter_yes_no.lower() not in ('yes', 'no'):
            print("""Sorry this was not a valid input, please type "yes" if you want to apply a filter by month or "no" if you do not want to apply a filter.""")
            continue
        # filter the choosed city data for available months and show a selection to the user.
        if filter_yes_no.lower() == "yes":
            df = pd.read_csv(CITY_DATA[city])
            df['Start Time'] = pd.to_datetime(df['Start Time'])
            df['month'] = df['Start Time'].dt.month
            unique_months = df['month'].unique()
            while True:
                month_input = int(input("""For the following months data are available {} based on the selected city {}. Please choose one month and enter as number, e.g. "1" for January: """.format(unique_months, city)))
                if month_input not in unique_months:
                    print("For the selected month are no data available. Enter a valid month from this list: {}: ".format(unique_months))
                else:
                    if month_input in unique_months:
                        break
            break
        else:
            if filter_yes_no.lower() == "no":
                month_input = None
            break
    month = month_input
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        filter_yes_no = input("""Do you want to filter by a day of the week (yes) or do you want to apply no day based filter (no)? Enter: "yes" or "no": """)
        if filter_yes_no.lower() not in ('yes', 'no'):
            print("""Sorry this was not a valid input, please type "yes" if you want to apply a filter by month or "no" if you do not want to apply a filter.""")
            continue
        while True:
            if filter_yes_no.lower() == "yes":
                day_input = int(input("""Please choice a day of the week and enter as number, e.g. "0" for Monday: """))
                if day_input not in (0, 1, 2, 3, 4, 5, 6):
                    print("""Sorry this was not a valid input, please type "0": Monday, "1": Tuesday, "2": Wednesday, "3": Thursday, "4": Friday, "5": Saturday, "6": Sunday.""")
                    continue
                if day_input in (0, 1, 2, 3, 4, 5, 6):
                    day = calendar.day_name[day_input]
                    break
            else:
                if filter_yes_no.lower() == "no":
                    day = None
                    break
        break
    return city, month, day
    
print('-'*40)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    os.chdir('c:/Users/lasse/Desktop/Udacity/Udacity_Python')
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month to create the new dataframe
    if month != None:
        df = df[df['month'] == month]
    # filter by day of week to create the new dataframe
    if day != None:
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month:', most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day:', most_common_day)

    # display the most common start hour
    most_common_starting_hour = df['hour'].mode()[0]
    print('The most common starting hour:', most_common_starting_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', most_commonly_used_start_station)

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', most_commonly_used_end_station)

    # display most frequent combination of start station and end station trip
    df['trip_combi'] = df['Start Station'] + df['End Station']
    most_frequent_combination = df['trip_combi'].mode()[0]
    print('most frequent combination of start station and end station trip:', most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total tavel time is: ", total_travel_time)

    # display mean travel time
    total_mean_travel_time = df['Trip Duration'].mean()
    print("The mean tavel time is: ", total_mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()
    print("The counts of user types are: ", counts_user_types)

    # Display counts of gender if available
    try:
        counts_gender = df['Gender'].value_counts()
        print("The counts of each gender are: ", counts_gender)
    except KeyError:
        print("The dataset for the selected city {} does not include data about the gender of users.".format(city))
        
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print("The earliest year of bith is: ", earliest_year)
        print("The most recent year of bith is: ", most_recent_year)
        print("The most common year of bith is: ", most_common_year)
    except KeyError:
        print("The dataset for the selected city {} does not include data about the birth year of users.".format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data():

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # get user input for raw data request
    while True:
        filter_yes_no = input("""Do you want to view the raw data set of the selected city {}? Enter: "yes" or "no": """.format(city))
        if filter_yes_no.lower() not in ('yes', 'no'):
            print("""Sorry this was not a valid input, please type "yes" if you want to view 5 rows of raw data or "no" if you do not want to view raw data.""")
            continue
        # load raw dataset for selected city and print out the first five rows. Request user input for additional rows and print five more rows if the user wants to view more rows. 
        if filter_yes_no.lower() == "yes":
            i = 5
            df = pd.read_csv(CITY_DATA[city])
            print(df.head(i))
            while True:
                filter_yes_no = input("""Do you want to view 5 more rows of the raw data set? Enter: "yes" or "no": """)
                if filter_yes_no.lower() not in ('yes', 'no'):
                    print("""Sorry this was not a valid input, please type "yes" if you want to view 5 more rows of raw data or "no" if you do not want to view 5 more rows of raw data.""")
                    continue
                if filter_yes_no.lower() == "yes":
                    i += 5
                    print(df.head(i))
                    continue
                else:
                    if filter_yes_no.lower() == "no":
                        break
        else:
            if filter_yes_no.lower() == "no":
                break
        break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
