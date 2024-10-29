import pandas as pd


def preprocess(df,region_df):

    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left', suffixes=('', '_region'))
    # dropping duplicates
    df = df.loc[:, ~df.columns.duplicated()]
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df