import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Create a list of valid month and day of the week inputs, this can be used to check the user input
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December' 'All']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday', 'All']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(
        'Please input the city you would like to filter for: ').lower()

    while city not in CITY_DATA.keys():
        city = input(
            'The city you have selected is not one of the permissable 3 options [chicago, new york city, washington]: ').lower()

    filter_option = input(
        'Would you like to filter by "month", "day", "both", or not at all? Type "none" for no time filter: ').lower()

    while filter_option not in ['month', 'day', 'both', 'none']:
        filter_option = input(
            'Sorry that input didn\'t match. Please select from ["month", "day", "both", "none"]: ').lower()

    if filter_option == 'none':
        # set month and day to 'All' because the user does not want to apply a time filter
        month = 'All'
        day = 'All'

    elif filter_option == 'month':
        # Set day to 'All' as the user only wants to filter by the month
        day = 'All'
        # Get user input for the month from January to June inclusive
        month = input(
            'Please input the month you would like to filter for or select \'All\' if you would not like to filter by a month: ').title()

        while month not in months:
            month = input(
                'Sorry that input didn\'t match. Please select the month January to June or type \'All\': ').title()

    elif filter_option == 'day':
        # Set month to 'All' as the user only wants to filter by the day
        month = 'All'
        # Get user input for the day of the week from Monday to Sunday inclusive
        day = input('Please input the day of the week you would like to filter for or select \'All\' if you would not like to filter by a day of the week: ').title()

        while day not in days:
            day = input(
                'Sorry that input didn\'t match. Please select the day of the week Monday to Sunday or type \'All\': ').title()

    else:
        # Get user input for both month and day of the week as the user has selected both
        # Get user input for the month from January to June inclusive
        month = input(
            'Please input the month you would like to filter for or select \'All\' if you would not like to filter by a month: ').title()

        while month not in months:
            month = input(
                'Sorry that input didn\'t match. Please select the month January to June or type \'All\': ').title()

        # Get user input for the day of the week from Monday to Sunday inclusive
        day = input('Please input the day of the week you would like to filter for or select \'All\' if you would not like to filter by a day of the week: ').title()

        while day not in days:
            day = input(
                'Sorry that input didn\'t match. Please select the day of the week Monday to Sunday or type \'All\': ').title()

    print('The filters you selected are city: {} month: {} day: {}'.format(
        city, month, day))

    print('-'*40)
    return city, month, day


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
    # read csv data for city of user's choice
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Create start month day and hour columns to answer the frequent times of travel descriptive statistics questions
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # Create travel time and hours columns fromt the start and end time columns to answer the travel time description statistics questions
    df['Trip Duration Hours'] = (
        (df['End Time'] - df['Start Time']) / pd.Timedelta(hours=1)).round(2)

    df['Trip Duration Minutes'] = (
        ((df['End Time'] - df['Start Time']) / pd.Timedelta(hours=1))*60).round(2)

    # Create a start and end station concatenate column to help answer the station descriptive statistice questions
    df['Trip Stations'] = df['Start Station'] + '_' + df['End Station']

    if month != 'All':

        df = df[df['Start Month'] == month]

    if day != 'All':

        df = df[df['Start Day'] == day]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'All':
        if day == 'All':
            # display the most common month
            print('Most Popular Start Month: {}'.format(
                df['Start Month'].mode()[0]))
            # display the most common day of week
            print('Most Popular Start Day of the Week: {}'.format(
                df['Start Day'].mode()[0]))
        else:
            # display the most common month
            print('Most Popular Start Month: {}'.format(
                df['Start Month'].mode()[0]))

    else:
        if day == 'All':
            # display the most common day of week
            print('Most Popular Start Day of the Week: {}'.format(
                df['Start Day'].mode()[0]))

    # display the most common start hour
    print('Most Popular Start Hour: {} Count = {}'.format(df['Start Hour'].mode()[
          0], df[df['Start Hour'] == df['Start Hour'].mode()[0]]['Start Time'].count()))

    # Display the filters that were used to get this result
    print('\nThe filters you selected are city: {} month: {} day: {}'.format(
        city, month, day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is: {}. Count = {}'.format(df['Start Station'].mode()[
          0], df[df['Start Station'] == df['Start Station'].mode()[0]]['Start Time'].count()), '\n')

    # display most commonly used end station
    print('The most common end station is: {}. Count = {}'.format(df['End Station'].mode()[
          0], df[df['End Station'] == df['End Station'].mode()[0]]['Start Time'].count()), '\n')

    # display most frequent combination of start station and end station trip
    start_station, end_station = (df['Trip Stations']).mode()[0].split('_')

    print('The most common combination of start and end stations is: {} and {}. Count = {}'.format(
        start_station, end_station, df[df['Trip Stations'] == df['Trip Stations'].mode()[0]]['Start Time'].count()))

    # Display the filters that were used to get this result
    print('\nThe filters you selected are city: {} month: {} day: {}'.format(
        city, month, day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if month != 'All':

        if day != 'All':
            # Both month and day filters were selected so include reference to the mnonth and the day in the output statement
            print('The total travel time in {} was: {} hours or {} minutes or {} seconds on {}s in {}'.format(city, df['Trip Duration Hours'].sum(
            ).round(2), df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2), day, month), '\n')

            print('The average travel time per ride in {} was: {} hours or {} minutes or {} second on {}s in {}'.format(
                city, df['Trip Duration Hours'].mean().round(2), df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2), day, month))

        else:
            # Only month filters were selected so include reference to the month in the output statement
            print('The total travel time in {} was: {} hours or {} minutes or {} seconds in {}'.format(city, df['Trip Duration Hours'].sum(
            ).round(2), df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2), month), '\n')

            print('The average travel time per ride in {} was: {} hours or {} minutes or {} seconds in {}'.format(
                city, df['Trip Duration Hours'].mean().round(2), df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2), month))

    else:

        if day != 'All':
            # Only day filters were selected so include reference to the day in the output statement
            print('The total travel time in {} was: {} hours or {} minutes or {} second on {}s'.format(city, df['Trip Duration Hours'].sum(
            ).round(2), df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2), day), '\n')

            print('The average travel time per ride in {} was: {} hours or {} minutes or {} seconds on {}s'.format(
                city, df['Trip Duration Hours'].mean().round(2), df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2), day))

        else:
            # No filters were selected so do not include any reference to the month or day in the output statement
            print('The total travel time in {} was: {} hours or {} minutes or {} seconds'.format(city, df['Trip Duration Hours'].sum(
            ).round(2), df['Trip Duration Minutes'].sum().round(2), df['Trip Duration'].sum().round(2)), '\n')

            print('The average travel time per ride in {} was: {} hours or {} minutes or {} seconds'.format(
                city, df['Trip Duration Hours'].mean().round(2), df['Trip Duration Minutes'].mean().round(2), df['Trip Duration'].mean().round(2)))

    # Display the filters that were used to get this result
    print('\nThe filters you selected are city: {} month: {} day: {}'.format(
        city, month, day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type and Count:', '\n {}'.format(
        df.groupby(df['User Type'])['Start Time'].count()), '\n')

    # Display counts of gender
    if city in ['chicago', 'new york city']:
        print('Gender and Count:', '\n {}'.format(
            df.groupby(df['Gender'])['Start Time'].count()))
    else:
        print('No Gender data is available in the washington dataset')

    # Display earliest, most recent, and most common year of birth
    if city in ['chicago', 'new york city']:
        print('\nThe earliest birth year is: {}'.format(
            int(df['Birth Year'].min())))

        print('\nThe most recent birth year is: {}'.format(
            int(df['Birth Year'].max())))

        print('\nThe most common birth year is: {} Count = {}'.format(int(df['Birth Year'].mode()[
              0]), df[df['Birth Year'] == df['Birth Year'].mode()[0]]['Start Time'].count()))

    else:
        print('\nNo Birth Year data is available in the washington dataset')

    # Display the filters that were used to get this result
    print('\nThe filters you selected are city: {} month: {} day: {}'.format(
        city, month, day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)

        df.drop(['Start Month', 'Start Day', 'Start Hour', 'Trip Duration Hours',
                 'Trip Duration Minutes', 'Trip Stations'], axis=1, inplace=True)

        pd.set_option('display.max_columns', None)

        view_data = 'First Run'
        x = 0
        y = 5

        while view_data.lower() not in ['yes', 'no']:
            view_data = input(
                'Would you like to view the individual trip data? Type \'yes\' or \'no\'.')

        while view_data.lower() == 'yes' and x <= len(df)-1:

            print(df[x:y])

            view_data = input(
                'Would you like to view the individual trip data? Type \'yes\' or \'no\'.')

            x += 5
            y += 5

            if y > len(df):
                y = len(df)

            while view_data.lower() not in ['yes', 'no']:
                view_data = input(
                    'Would you like to view the individual trip data? Type \'yes\' or \'no\'.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Have a nice day')
            break


if __name__ == "__main__":
    main()
