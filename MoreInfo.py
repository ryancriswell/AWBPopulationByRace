import pandas as pd
# This program will take in a csv formatted such as the example and saved in the same directory as the .py
# It outputs a .txt file in the same location filled with html code that is ready to copy and paste into our
# AWB more info page for Population by Race and Ethnicity.
# TODO all todo marks indicate locations where the code had to be changed to fit the 2020 census which
# TODO contains N/A for all 1-Year Estimates due to Covid-19.

def main():
    # create our output file
    f = open('outputfile.txt', 'w')
    # Get dataframe and basic info about it
    df, r, c = get_data_info()
    # Iterate by rows. Pandas doesn't count the head in our dataframe so 0 index for us will
    # be the first county. We step by 8 because each county has 8 entries.
    for i in range(0, r, 8):
        # Get county name
        location = df['Location'][i]

        # Get the interval (1 year or 5 year)
        if '1' in df['Estimate_Interval'][i]:
            #TODO 1 Year data for 2020 is missing, so we report 2019 data. See the same line below for corrections
            years = [df.columns.values[c - 2], df.columns.values[c - 3], df.columns.values[c - 7]]
            datalist = get_county_data(df, i, years)
            # set the interval for the column name and also for output
            interval = '1-Year Interval'
        else:
            # years is an array filled with year numbers (current year, current-1, current-5)
            years = [df.columns.values[c - 1], df.columns.values[c - 2], df.columns.values[c - 6]]
            datalist = get_county_data(df, i, years)
            # set the interval for the column name and also for output
            interval = '5-Year Interval'

        # Get the data for the US and WA fo given years and interval as a list
        wadatalist, usdatalist = get_wa_us_data(df, years, interval)
        # Output the county information as html code
        print_county(years_to_string(years, interval), datalist, location, interval, f)
        # Output Washington State information as html code
        print_wa(years_to_string(years, interval), wadatalist, interval, f)


# get the data for the county at row i
def get_county_data(df, i, years):
    datalist = []
    for j in range(8):
        # iterate for each year of the 3 years
        for k in range(3):
            # add the cell value to our list
            datalist.append(df[years[k]][i + j])
    return datalist


# get the data for the US and Washington
def get_wa_us_data(df, years, interval):
    # get the dataframe with just WA or US data for the correct interval
    df_wa = df.query('Location == "Washington State" & Estimate_Interval == @interval')
    df_us = df.query('Location == "United States" & Estimate_Interval == @interval')
    # reset the index so that we get 0 indexed sub-dataframes instead of keeping original row numbers
    df_wa.reset_index(inplace=True, drop=True)
    df_us.reset_index(inplace=True, drop=True)
    wadatalist, usdatalist = [], []
    for j in range(8):
        # iterate for each year of the 3 years
        for k in range(3):
            # add the cell value to our list
            wadatalist.append(df_wa[years[k]][j])
            usdatalist.append(df_us[years[k]][j])

    return wadatalist, usdatalist


# open and read csv into pandas dataframe. Returns basic info about the dataframe
def get_data_info():
    # Open our csv
    file = open('AWB Population By Race & Ethnicity.csv')
    # Create our dataframe
    df = pd.read_csv(file)
    file.close()

    # Get the number of rows and columns
    r, c = df.shape
    # Get year numbers for current, current-1, and current-5
    return df, r, c


# take in our list of years and the given interval and return a new list with strings for output
def years_to_string(years, interval):
    # For our 5-Year Interval we need to return the range of years
    if interval == '5-Year Interval':
        years0 = str(int(years[0]) - 4) + '-' + years[0]
        years1 = str(int(years[1]) - 4) + '-' + years[1]
        years2 = str(int(years[2]) - 4) + '-' + years[2]
    else:
        # for the 1-year interval we can just return the ints as string directly
        #TODO for this first use we are missing 2020 data so we -1 to get 2019 data
        years0 = years[0]
        years1 = years[1]
        years2 = years[2]
    return years0, years1, years2


# This function prints the html code to be sent to the more info pages for a given year and location
def print_county(years_strings, datalist, location, interval, f):
    #TODO if we have 1-year interval we add the note to the beginning that we are missing 2020 and are using 2019 data instead
    note = ''
    if interval == '1-Year Interval':
        note = '<p><em>Note: Due to the low survey response rate during the Covid-19 pandemic, the 1 year estimates of the ACS for 2020 will not be available.</em></p>\n'

    print(f'''{note}<p>During the {years_strings[0]} interval in <strong>{location}</strong>, the estimated non-white shares of the total population who were:</p>

<ul>
	<li>Hispanic (may be of any race) was {round(datalist[0] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(datalist[0] * 100 - datalist[1] * 100, 1)} points from {round(datalist[1] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[0] * 100 - datalist[2] * 100, 1)} points from {round(datalist[2] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
	<li>White (Non-Hispanic) was {round(datalist[3] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(datalist[3] * 100 - datalist[4] * 100, 1)} points from {round(datalist[4] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[3] * 100 - datalist[5] * 100, 1)} points from {round(datalist[5] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
	<li>Black or African-American (Non-Hispanic) was {round(datalist[6] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(datalist[6] * 100 - datalist[7] * 100, 1)} points from {round(datalist[7] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[6] * 100 - datalist[8] * 100, 1)} points from {round(datalist[8] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
	<li>American Indian (Non-Hispanic) was {round(datalist[9] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(datalist[9] * 100 - datalist[10] * 100, 1)} points from {round(datalist[10] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[9] * 100 - datalist[11] * 100, 1)} points from {round(datalist[11] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
	<li>Asian (Non-Hispanic) was {round(datalist[12] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(datalist[12] * 100 - datalist[13] * 100, 1)} points from {round(datalist[13] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[12] * 100 - datalist[14] * 100, 1)} points from {round(datalist[14] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
	<li>Native Hawaiian &amp; Pacific Islander (Non-Hispanic) was {round(datalist[15] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(datalist[15] * 100 - datalist[16] * 100, 1)} points from {round(datalist[16] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[15] * 100 - datalist[17] * 100, 1)} points from {round(datalist[17] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
	<li>Some other race was {round(datalist[18] * 100, 1)}%, changing by:
	<ul style="list-style-type:circle">
		<li>{round(datalist[18] * 100 - datalist[19] * 100, 1)} points from {round(datalist[19] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[18] * 100 - datalist[20] * 100, 1)} points from {round(datalist[20] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
	<li>Two or more races was {round(datalist[21] * 100, 1)}%, changing by:
	<ul style="list-style-type:circle">
		<li>{round(datalist[21] * 100 - datalist[22] * 100, 1)} points from {round(datalist[22] * 100, 1)}% during the {years_strings[1]} interval.</li>
		<li>{round(datalist[21] * 100 - datalist[23] * 100, 1)} points from {round(datalist[23] * 100, 1)}% during the {years_strings[2]} interval.</li>
	</ul>
	</li>
</ul>\n''', file=f)


# This function prints the html code to be sent to the more info pages for Washington State in a given year
def print_wa(years_strings, wadatalist, interval, f):
    # add a note to the end indicating the interval
    if interval == '5-Year Interval':
        note = '5-Year Estimates'
    else:
        note = '1-Year Estimates'

    print(f'''<p>During {years_strings[0]} in <strong>Washington State</strong>, the estimated non-white shares of the total population who were:</p>

<ul>
	<li>Hispanic (may be of any race) was {round(wadatalist[0] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[0] * 100 - wadatalist[1] * 100, 1)} points from {round(wadatalist[1] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[0] * 100 - wadatalist[2] * 100, 1)} points from {round(wadatalist[2] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
	<li>White (Non-Hispanic) was {round(wadatalist[3] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[3] * 100 - wadatalist[4] * 100, 1)} points from {round(wadatalist[4] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[3] * 100 - wadatalist[5] * 100, 1)} points from {round(wadatalist[5] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
	<li>Black or African-American (Non-Hispanic) was {round(wadatalist[6] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[6] * 100 - wadatalist[7] * 100, 1)} points from {round(wadatalist[7] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[6] * 100 - wadatalist[8] * 100, 1)} points from {round(wadatalist[8] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
	<li>American Indian (Non-Hispanic) was {round(wadatalist[9] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[9] * 100 - wadatalist[10] * 100, 1)} points from {round(wadatalist[10] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[9] * 100 - wadatalist[11] * 100, 1)} points from {round(wadatalist[11] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
	<li>Asian (Non-Hispanic) was {round(wadatalist[12] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[12] * 100 - wadatalist[13] * 100, 1)} points from {round(wadatalist[13] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[12] * 100 - wadatalist[14] * 100, 1)} points from {round(wadatalist[14] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
	<li>Native Hawaiian &amp; Pacific Islander (Non-Hispanic) was {round(wadatalist[15] * 100, 1)}%, changing by: 
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[15] * 100 - wadatalist[16] * 100, 1)} points from {round(wadatalist[16] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[15] * 100 - wadatalist[17] * 100, 1)} points from {round(wadatalist[17] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
	<li>Some other race was {round(wadatalist[18] * 100, 1)}%, changing by:
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[18] * 100 - wadatalist[19] * 100, 1)} points from {round(wadatalist[19] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[18] * 100 - wadatalist[20] * 100, 1)} points from {round(wadatalist[20] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
	<li>Two or more races was {round(wadatalist[21] * 100, 1)}%, changing by:
	<ul style="list-style-type:circle">
		<li>{round(wadatalist[21] * 100 - wadatalist[22] * 100, 1)} points from {round(wadatalist[22] * 100, 1)}% during {years_strings[1]}. </li>
		<li>{round(wadatalist[21] * 100 - wadatalist[23] * 100, 1)} points from {round(wadatalist[23] * 100, 1)}% during {years_strings[2]}.</li>
	</ul>
	</li>
</ul>

<p><strong><em>Note: </em></strong><em>ACS {note}.</em></p>
======================================================''', file=f)


main()
