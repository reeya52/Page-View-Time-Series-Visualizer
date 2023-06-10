import calendar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("C:/Users/Reeya/OneDrive/Desktop/Learning/fcc-forum-pageviews.csv").set_index("date")

# Clean data
df = df[(df["value"] >= df['value'].quantile(0.025)) & (df["value"] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot

    df.index = pd.to_datetime(df.index)
    # date_format = '%Y-%m'

    # plt.figure(figsize=(15, 10))
    fig, ax = plt.subplots(figsize=(15, 10))

    ax.plot(df.index, df['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # months = mdates.MonthLocator(bymonth=5, interval=5)
    # date_fmt = mdates.DateFormatter(date_format)
    # plt.gca().xaxis.set_minor_locator(months)
    # plt.gca().xaxis.set_major_formatter(date_fmt)

    # Save image and return fig (don't change this part)
    fig.savefig('C:/Users/Reeya/OneDrive/Desktop/Learning/line_plot.png')

    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_index = pd.to_datetime(df.index)
    year = df_index.year.to_series().reset_index(drop=True)
    month = df_index.month.to_series().reset_index(drop=True)
    month_values = []
    for val in month.values:
        month_values.append(calendar.month_name[val])

    month = pd.Series(month_values)
    value = df['value'].reset_index(drop=True)

    df_bar = pd.DataFrame({"year": year, "month": month, "value": value})

    df_groupby_avg = df_bar.groupby(['year','month']).mean().reset_index()

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(15, 10))  # Set the figure size

    # Get unique years and months
    years = df_groupby_avg['year'].unique()
    months = df_groupby_avg['month'].unique()

    # Sort the months in chronological order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December']
    months_sorted = sorted(months, key=lambda x: month_order.index(x))

    # Set the width of each bar
    bar_width = 0.05

    # Iterate over sorted months
    for i, month in enumerate(months_sorted):
        # Calculate the x position for each bar
    
        x = np.arange(len(years)) + (i * bar_width)
        
        # Get the count for the current month
        counts = df_groupby_avg[df_groupby_avg['month'] == month]['value'].tolist()

        if len(counts) < len(x):
            counts.insert(0, 0)
        
        # Plot the bars for the current month
        plt.bar(x, counts, width=bar_width, label=month)

    # Set the x-axis labels and tick positions
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.xticks(np.arange(len(years)) + (bar_width * (len(months_sorted) - 1)) / 2, years)

    # Sort and display the legend in the order of sorted months
    handles, labels = plt.gca().get_legend_handles_labels()
    sorted_legend = sorted(zip(labels, handles), key=lambda x: month_order.index(x[0]))
    labels, handles = zip(*sorted_legend)
    plt.legend(handles, labels)

    # Show the plot
    plt.tight_layout()  # Adjust spacing between subplots

    # Save image and return fig (don't change this part)
    fig.savefig('C:/Users/Reeya/OneDrive/Desktop/Learning/bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [datetime.datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S').date().strftime("%Y") for d in df_box.date]
    df_box['month'] = [datetime.datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S').date().strftime("%m") for d in df_box.date]
    
    df_box['month'] = [calendar.month_abbr[int(d)] for d in df_box.month.values]
    # Draw box plots (using Seaborn)
    plt.rcParams["figure.figsize"] = [15.00, 10]
    plt.rcParams["figure.autolayout"] = True
    fig, axes = plt.subplots(1, 2)
    sns.boxplot(df_box, x='year', y='value', ax=axes[0]).set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel='Page Views')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(df_box, x="month", y='value', ax=axes[1], order=month_order).set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel='Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('C:/Users/Reeya/OneDrive/Desktop/Learning/box_plot.png')
    return fig

if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()