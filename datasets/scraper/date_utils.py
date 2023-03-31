from datetime import datetime, timedelta
STD_FMT = "%B %d, %Y"

def is_older_than_5yrs(date_str,date_format=STD_FMT):

    # Parse the date string into a datetime object using the specified date format
    date = datetime.strptime(date_str, date_format)

    # Calculate the date that was 5 years ago from today
    five_years_ago = datetime.now() - timedelta(days=365*5)

    # Compare the parsed date to the date 5 years ago
    if date < five_years_ago:
        return True
    else:
        return False

# Given an input String "* 10 Months *" or "* 10 days" or "* 10 Years", this function 
# returns if it the date is older than 5 years
def is_older_than_5_yrs_str(inputstr):
    inputstr=inputstr.lower()
    x=inputstr.split()
    idx = -1
    timeframe = 'Days'
    total_time = 0
    for i in range(len(x)-1):
        # print(x[i],x[i+1])
        if 'month' in x[i+1]:
            idx = i
            timeframe = 'Months'
            break
        if 'day' in x[i+1]:
            idx = i
            timeframe = 'Days'
            break
        if 'year' in x[i+1]:
            idx = i
            timeframe = 'Years'
            break
    if idx == -1:
        return -1
    try:
        if int(x[i]) is not None:
            if timeframe == 'Days':
                total_time += int(x[i])
            elif timeframe == 'Months':
                total_time += int(x[i])*30
            else:
                total_time +=int(x[i])*365
    except:
        return -1
    return total_time>5*365

    
def get_latest(date_arr,date_format=STD_FMT):
    dates = [datetime.strptime(date_str, date_format) for date_str in date_arr]

    # Find the latest date in the list of datetime objects
    latest_date = max(dates)

    # Convert the latest date back to the original format and return it
    latest_date_str = datetime.strftime(latest_date, date_format)
    return latest_date_str

def standardize(date_format, date_str):
    # Parse the date string into a datetime object using the specified date format
    date = datetime.strptime(date_str, date_format)
    # Convert the datetime object to the standardized date format
    standardized_date = date.strftime(STD_FMT)

    return standardized_date

