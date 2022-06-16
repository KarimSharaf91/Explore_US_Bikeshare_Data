import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'chicago.csv', 'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv', 'New york city': 'new_york_city.csv',
              'new york city': 'new_york_city.csv', 'washington': 'washington.csv',
             'Washington': 'washington.csv' }

def check_input(input_str,input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read=input(input_str)
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Sorry, your input should be: chicago, new york city or washington")
                if input_type == 2:
                    print("Sorry, your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    print("Sorry, your input should be: saturday, sunday, ... friday, or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return input_read
#Function to figure out the filtering requirements of the user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   
    city = input("Choose the city name : (Chigaco, New york City, Washington) : ").lower()
    #Running this loop to ensure the correct user input gets selected else repeat
    while city not in CITY_DATA.keys():
        print("Please, Enter a Valid city name")
        city = input("Choose the city name (Chigaco, New york City, Washington) : ").lower()
    print("You have chosen {} as your city.".format(city.title()))

    #Creating a dictionary to store all the months including the 'all' option
    MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month= ''
    while month not in MONTH_DATA :
        print("\nPlease enter the month, between January to June, for which you're seeking the data:")
        print("\n(You may also opt to view data for all months, please type 'all' or 'All' or 'ALL' for that.)")
        month = input().lower()

        if month not in MONTH_DATA :
            print("\nInvalid input. Please try again in the accepted input format.")
            print("\nRestarting...")

    print("\nYou have chosen {} as your month.".format(month.title()))

    #Creating a list to store all the days including the 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week of your choice for which you're seeking the data:")
        print("\nAccepted input:\nDay name; not case sensitive (e.g. monday or MONDAY).\nDay name in title case (e.g. Monday).")
        print("\n(You can also put 'all' or 'All' to view data for all days in a week.)")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please try again in one of the accepted input formats.")
            print("\nRestarting...")

    print("\nYou have chosen {} as your day.".format(day.title()))
    print("\nYou have chosen to view data for city: {}, month/s: {} and day/s: {}.".format(city.upper(), month.upper(), day.upper()))
    print('-'*80)
    #Returning the city, month and day selections
    return city, month, day

#Function to load data from .csv files
def load_data(city, month, day):
    """ 
    "Loads data for the specified city and filters by month and day if applicable."
    
    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """  
        #Load data
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start hour'] = df['Start Time'].dt.hour

  
    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns
    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    """
    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    popular_month = df['month'].mode()[0]

    print("The Most Popular Month is : {}".format(popular_month))

    #display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print("\nThe Most Popular Day is : {}".format(popular_day))

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print("\nThe Most Popular Start Hour is : {}".format(popular_hour))

    #Prints the time taken to perform the calculation
    #You will find this in all the functions involving any calculation
    #throughout this program
    print("\nThis process took {} seconds.".format(time.time() - start_time))
    print('-'*80)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    """
    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print("The Most Commonly Used Start Station is : {}".format(common_start_station))

    #Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print("\nThe Most Commonly Used End Station is : {}".format(common_end_station))

    #Uses str.cat to combine two columsn in the df
    #Assigns the result to a new column 'Start To End'
    #Uses mode on this new column to find out the most common combination
    #of start and end stations
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print("\nThe Most Frequent Combination of Trips are from : {}.".format(combo))

    print("\nThis process took {} seconds.".format(time.time() - start_time))
    print('-'*80)

#Function for trip duration related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    """
    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
       """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Uses sum method to calculate the total trip duration
    total_duration = df['Trip Duration'].sum()
    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print("The Total Trip Duration is {} hours, {} minutes and {} seconds.".format(hour, minute, second))

    #Calculating the average trip duration using mean method
    average_duration = (df['Trip Duration'].mean().round())
    #Finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
    #This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print("\nThe average trip duration is {} hours, {} minutes and {} seconds.".format(hrs, mins, sec))
    else:
        print("\nThe average trip duration is {} minutes and {} seconds.".format(mins, sec))

    print("\nThis process took {} seconds.".format(time.time() - start_time))
    print('-'*80)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""
  
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #The total users are counted using value_counts method
    #They are then displayed by their types (e.g. Subscriber or Customer)
    user_type = df['User Type'].value_counts()

    print("The types of users by number are given below:\n\n{}".format(user_type))

    #This try clause is implemented to display the numebr of users by Gender
    #However, not every df may have the Gender column, hence this...
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("\nThe type of users by gender are given below:\n\n{}".format(gender))
    else:
        print("\nThere is no available 'Gender' column in this data.")

    #Similarly, this try clause is there to ensure only df containing
    #'Birth Year' column are displayed
    #The earliest birth year, most recent birth year and the most common
    #birth years are displayed
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {}\n\nThe most recent year of birth: {}\n\nThe most common year of birth: {}".format(earliest, recent, common_year))

    except:
        print("There are no birth year details in this file.")

    print("\nThis process took {} seconds.".format(time.time() - start_time))
    print('-'*80)

#Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city."""
    """ 
    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """ 
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the first 5 raws of data?     Enter Yes or No.\n")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view the following 5 raws of data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*80)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

    # Restarting option
        restart = input('\nWould you like to restart?     Enter Yes or No.\n')
        if restart.lower() == 'yes' or restart.lower() == 'Yes' :
            main()
        else :
            print ("The end of process, Thank you!")     
        
if __name__ == "__main__":
	main()