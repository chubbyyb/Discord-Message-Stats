import glob
import pandas as pd
import plotly.graph_objects as go
 

def graph():

    # list all csv files only
    # Enter your path how the example is displayed (2 backslashes)
    csv_files = glob.glob('C:\\Users\\chubs\\Documents\\messageStats\\package\\messages\\*\\*.{}'.format('csv'))
    #print(csv_files)

    df_csv_concat = pd.concat([pd.read_csv(file) for file in csv_files ], ignore_index=True)
    #print(df_csv_concat)

    df_csv_concat.to_csv('concatenated_data.csv', index=False)

    # Clean the data and put it in new.csv
    df = pd.read_csv('concatenated_data.csv') 
    df['Timestamp'] = df['Timestamp'].astype('str').str.slice(0,10) 
    df.to_csv(path_or_buf='new.csv') 

    # Put the dates in dates.csv
    df = pd.read_csv('new.csv') # Read the clean CSV file
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d')
    df['Timestamp'].to_csv(path_or_buf='dates.csv',index_label='Messages') 

    # Equivelant of ctrl-fing a date and getting results count
    df = pd.read_csv('dates.csv')
    df1 = df.groupby('Timestamp').count().copy() 
    #print(df.groupby('Timestamp').count().to_string())
    #print(df.mean(numeric_only=True,skipna = True))
    df1.to_csv("df1.csv", sep=",")


    df = pd.read_csv('df1.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df1 = pd.read_csv('df1.csv')
    df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])


    # GET MISSING DATES --------------------------------------------------------------------------------

    # Get value of first row, first column
    first_val = pd.to_datetime(df1.loc[0, "Timestamp"],format='%Y-%m-%d')
    # Get value of last row, first column
    last_val = pd.to_datetime(df1.loc[df1.index[-1], "Timestamp"],format='%Y-%m-%d')

    missing_dates = pd.date_range(start = first_val, end = last_val ).difference(df1['Timestamp'])


    # Create a new DataFrame with missing dates
    new_rows = []
    for date in missing_dates:
        new_rows.append({"Timestamp": date, "Messages": 0})
    new_df = pd.DataFrame(new_rows)

    # Concatenate original DataFrame with new DataFrame and sort by date
    df = pd.concat([df, new_df]).sort_values("Timestamp")

    # Write new DataFrame to CSV
    df.to_csv("df1.csv", index=False)

    # END OF THIS BULLSHIT THAT TOOK ME 8 HOURS ----------------------------------------------------------




    # Define custom color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Generate graph using Figure Constructor
    fig = go.Figure(
        go.Scatter(
            x=df1["Timestamp"],
            y=df1["Messages"],
            mode="lines",
            line=dict(color=colors[0], width=2),
            marker=dict(color=colors[0], size=6)
        )
    )

    
    fig.update_layout(
        title="Message Stats",
        paper_bgcolor="#1c1e26",  # Sets background color outside of the graph
        plot_bgcolor="#0d1117",
        xaxis=dict(
            title="Time",
            linecolor="#7f7f7f",
            tickfont=dict(color="#1f77b4"),
            showgrid=False,
        ),
        yaxis=dict(
            title="Messages",
            linecolor="#7f7f7f",
            tickfont=dict(color="#1f77b4"),
            showgrid=False,
        ),
        font=dict(color="#1f77b4"),
    )

    fig.show()