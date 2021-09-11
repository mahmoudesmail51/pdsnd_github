import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    city = ''
    month = ''
    day = ''
    filter = ''
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York, or Washington')
            if city.lower() not in ['chicago','new york','washington','newyork']:
                raise ValueError('Select only Chicago, New York or Washington only!')
            break
        except Exception as error:
            print(error)        
    
    #get user input for month (all, january, february, ... , june)
    while True:
        try:
            option = input('Would you like to filter by month, day, both, or not at all? Type \"all\" for no filter.')
            if option.lower() not in ['month','day','both','all']:
                raise ValueError('Select only for filtering options: month, day, both or all for no filtering.')
            elif option.lower() == 'month':
                month = get_month()
                day = 'all'
                filter = 'month'
            elif option.lower() == 'day':
                day = get_day()
                month = 'all'
                filter = 'day'
            elif option.lower() == 'both':
                month = get_month()
                day = get_day()
                filter = 'both'
            #the user choose all    
            else:
                day = month = filter = 'all'
            break  
        except Exception as error:
            print(error)

    print('-'*40)
    return city, month, day, filter

def get_month():
    """Retruns user's input for month field"""
    month = ''
    while True:
        try:
            print('Which month? January, February, March, April, May or June')
            month = input()
            if month.lower() not in ['january','february','march','april','may','june','all']:
                raise ValueError('Select only January, February, March, April, may, june only!')
            break
        except Exception as error:
            print(error)
    return month

def get_day():
    """ Returns user's input for day field """
    day = ''
    while True:
        try:
            day = input('Which day? Enter full day Sunday, Monday, Tuesday etc...')
            if day.lower() not in ['saturday','sunday','monday','tuesday','wednesday','thursday','friday']:
                raise ValueError('Select only one day of the week Sunday, Monday, etc...')
            break
        except Exception as error:
            print(error) 
    return day        

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

    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        #use the index of the months list to get the corresponding int
        month = months.index(month.lower()) +1
        
        #filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day of week if applicable
    if day != 'all':
        #filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df,filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[df['month'].mode()[0]-1]
    count_month = df[df['month'] == month].shape[0]
    print('The most common month: ',month.title(),' Count: ',count_month,' Filtered by: ',filter)

    #display the most common day of week
    day_of_week = df['day_of_week'].mode()[0]
    count_day = df[df['day_of_week'] == day_of_week].shape[0]
    print('The most common day of week: ',day_of_week,' Count: ',count_day,' Filtered by: ',filter)

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour = df['hour'].mode()[0]
    count_hour = df[df['hour'] == hour].shape[0]
    print('The most common start hour: ', hour,' Count: ',count_hour,' Filtered by: ',filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df,filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    count_start_station = df[df['Start Station'] == start_station].shape[0]
    print('The most common start station: ',start_station,' Count: ',count_start_station,' Filtered by: ',filter)
    
    #display most commonly used end station
    end_station = df['End Station'].mode()[0]
    count_end_station = df[df['End Station'] == end_station].shape[0]
    print('The most common end station: ',end_station,' Count: ',count_end_station,' Filtered by: ',filter)

    #display most frequent combination of start station and end station trip
    df['combined stations'] = df['Start Station'] + '-'+ df['End Station']
    popular_trip = df['combined stations'].mode()[0]
    count_popular_trip = df[df['combined stations'] == popular_trip].shape[0]
    print('The most popular trip: ', popular_trip,' Count: ',count_popular_trip,' Filtered by: ',filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df,filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time_travel = df['Trip Duration'].sum()
    count_of_trips = df['Trip Duration'].shape[0]
    print('Total travel time: ',total_time_travel,' Count: ',count_of_trips,' Filtered by: ',filter)
    
    #display mean travel time
    average_time_travel = df['Trip Duration'].mean()
    print('Average travel time: ',average_time_travel,' Filtered by: ',filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    #display counts of user types
    print('User types count:')
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    #check if gender column exists as there are some missing data
    if('Gender' in df.columns):
        gender_count = df['Gender'].value_counts()
        #display counts of gender
        print('Gender count:')
        print(gender_count)
    else:
        print('No gender data to share')

    
    #check if birth year column exists as there are some missing data
    if('Birth Year' in df.columns):
        #display earliest, most recent, and most common year of birth
        print('Earliest, most recent and most common year respectively: ')
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()
        print(int(earliest_year),int(most_recent_year),int(most_common_year))
    else:
        print('No birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """ Main menu for bikeshare descriptive statistics program"""

    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)
        time_stats(df,filter)
        station_stats(df,filter)
        trip_duration_stats(df,filter)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break    
    print('End of the bikeshare descriptive statistics program')

def display_raw_data(df):
    """ Function that interacts with user and prints raw data upon request."""

    run = 0
    while True:
        option = input('\nWould you like to view individual trip data? Enter yes or no.\n')
        if option.lower() !='no':
            temp_df = df.iloc[run * 5: (run+1)*5]
            run+=1 
            print(temp_df.head())
        else:
            break

if __name__ == "__main__":
    main()
  