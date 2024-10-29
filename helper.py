import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        # Grouping by 'Year' if we are dealing with a specific country
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        # Grouping by 'region' for overall tally or yearly tally for all regions
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    # Adding total column for medal counts
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Casting columns to integers
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')  # Changed 'total' to 'Total' for consistency

    return x



def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col]).groupby('Year').size().reset_index(name=col)
    nations_over_time = nations_over_time.sort_values('Year')  # Sort by 'Year' column
    return nations_over_time



def most_successful(df, selected_sport):
    # Filter based on the selected sport if it's not 'Overall'
    if selected_sport != 'Overall':
        temp_df = df[df['Sport'] == selected_sport]
    else:
        temp_df = df

    # Get the top 15 athletes based on counts
    name_counts = temp_df['Name'].value_counts().reset_index()
    name_counts.columns = ['Name', 'Count']  # Rename columns explicitly

    # Merge based on the Name column
    top_athletes_df = name_counts.head(15).merge(df, on='Name', how='left')[['Name', 'Count', 'Sport', 'Event']]
    return top_athletes_df.drop_duplicates(subset='Name')

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, selected_country):
    # Filter the DataFrame for the selected country
    temp_df = df[df['region'] == selected_country]

    # Get top 10 athletes based on counts and reset index with custom column names
    name_counts = temp_df['Name'].value_counts().reset_index()
    name_counts.columns = ['Name', 'Count']  # Rename to 'Name' and 'Count' explicitly

    # Merge on 'Name' to bring in 'Sport' and 'Event' details
    top10_df = name_counts.head(10).merge(df, on='Name', how='left')[['Name', 'Count', 'Sport', 'Event']]

    # Remove duplicate names to show only unique top athletes
    return top10_df.drop_duplicates(subset='Name')


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
