from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('data/processed/states_daily_cleaned.csv')
df2 = pd.read_csv('data/processed/us_daily_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])
df2['date'] = pd.to_datetime(df2['date'])

# Calculate rolling averages for state data
df['positiveIncrease_7day_avg'] = df.groupby('state')['positiveIncrease'].rolling(window=7).mean().round(3).reset_index(level=0, drop=True).fillna(0)
df['deathIncrease_7day_avg'] = df.groupby('state')['deathIncrease'].rolling(window=7).mean().round(3).reset_index(level=0, drop=True).fillna(0)

# Calculate rolling averages for national data
df2['positiveIncrease_7day_avg'] = df2['positiveIncrease'].rolling(window=7).mean().round(3).fillna(0)
df2['deathIncrease_7day_avg'] = df2['deathIncrease'].rolling(window=7).mean().round(3).fillna(0)

metrics_map = {
    "New Cases (7-Day Avg)": "positiveIncrease_7day_avg",
    "New Deaths (7-Day Avg)": "deathIncrease_7day_avg",
    "Current Hospitalizations": "hospitalizedCurrently",
    "Total Cases (Cumulative)": "positive",
    "Total Deaths (Cumulative)": "death"
}
all_states = sorted(df['state'].unique().tolist())
min_date = df['date'].min()
max_date = df['date'].max()

# --- Define UI ---
app_ui = ui.page_fluid(

    ui.panel_title("COVID-19 Dashboard"),
    
    ui.navset_tab(

        # --- TAB 1 ---
        ui.nav_panel("National Trend",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.div(
                        ui.input_select("national_metric", "Select Metric:", list(metrics_map.keys()), selected="positiveIncrease_7day_avg"),
                        ui.input_date_range("national_date_range", "Date Range:", 
                                        start=min_date, end=max_date,
                                        min=min_date, max=max_date),
                        style="width: 230px;"), 
                    width="300px"),
                ui.layout_columns(
                    ui.value_box("Total Cases", ui.output_text("val_total_cases_national")),
                    ui.value_box("Total Deaths", ui.output_text("val_total_deaths_national")),
                    ui.value_box("Current Hospitalized", ui.output_text("val_hospitalized_national")),
                ),
                ui.card(
                    ui.output_plot("national_plot")
                )
            )
        ),
        
        # --- TAB 2 ---
        ui.nav_panel("State Details",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.div(
                        ui.input_select("state_select", "Select State:", all_states, selected="IL"),
                        ui.input_select("metric_select", "Select Metric:", list(metrics_map.keys()), selected="positiveIncrease_7day_avg"),
                        ui.input_date_range("date_range", "Date Range:", 
                                            start=min_date, end=max_date,
                                            min=min_date, max=max_date), 
                    style="width: 230px;"), 
                    width="300px"),
                ui.layout_columns(
                    ui.value_box("Total Cases", ui.output_text("val_total_cases")),
                    ui.value_box("Total Deaths", ui.output_text("val_total_deaths")),
                    ui.value_box("Current Hospitalized", ui.output_text("val_hospitalized")),
                ),
                ui.card(
                    ui.output_plot("state_plot")
                )
            )
        ),

        # --- TAB 3 ---
        ui.nav_panel("State Comparison",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.div(
                        ui.input_selectize("compare_states", "Select States to Compare:", 
                                        all_states, selected=["NY", "CA", "IL"], multiple=True),
                        ui.input_select("compare_metric", "Metric to Compare:", list(metrics_map.keys()), selected="positiveIncrease_7day_avg"),
                        ui.input_date_range("compare_date_range", "Date Range:", 
                                        start=min_date, end=max_date,
                                        min=min_date, max=max_date),
                        ui.hr(),
                        ui.input_date("table_date_select", "Select Date for Table:", 
                                      value=max_date, min=min_date, max=max_date),
                        style="width: 230px;"), 
                    width="300px"),
                ui.card(
                    ui.output_plot("comparison_plot")
                ),
                ui.card(
                    ui.output_data_frame("comparison_data_table")
                )
            )
        )
    )
)

# --- Server Logic ---
def server(input, output, session):
    
    # Filter data for TAB 1
    @reactive.Calc
    def get_national_data():
        mask = (
            (df2['date'] >= pd.to_datetime(input.national_date_range()[0])) &
            (df2['date'] <= pd.to_datetime(input.national_date_range()[1]))
        )
        return df2[mask]

    # Filter data for TAB 2
    @reactive.Calc
    def get_state_data():
        mask = (
            (df['state'] == input.state_select()) &
            (df['date'] >= pd.to_datetime(input.date_range()[0])) &
            (df['date'] <= pd.to_datetime(input.date_range()[1]))
        )
        return df[mask]

    # Filter data for TAB 3
    @reactive.Calc
    def get_comparison_data():
        mask = (
            (df['state'].isin(input.compare_states())) &
            (df['date'] >= pd.to_datetime(input.compare_date_range()[0])) &
            (df['date'] <= pd.to_datetime(input.compare_date_range()[1]))
        )
        return df[mask]

    # --- TAB 1 Output ---
    @render.plot
    def national_plot():
        data = get_national_data()
        if data.empty:
            return

        metric_label = input.national_metric() 
        metric_col_name = metrics_map[metric_label] 
        
        fig, ax = plt.subplots(figsize=(12, 6))

        if "positiveIncrease" in metric_col_name:
            ax.bar(data['date'], data['positiveIncrease'], color='#d9534f', alpha=0.3, label="Daily Cases")
        elif "deathIncrease" in metric_col_name:
            ax.bar(data['date'], data['deathIncrease'], color='lightgray', alpha=0.6, label="Daily Deaths")

        ax.plot(data['date'], data[metric_col_name], color='#d9534f', linewidth=2, label=metric_label)
        
        ax.set_title(f"US National: {metric_label} over time")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        fig.tight_layout()
        return fig
    
    @reactive.Calc
    def get_national_latest_data():
        data = get_national_data()
        if data.empty:
            return None
        return data.sort_values('date').iloc[-1]
    
    @render.text
    def val_total_cases_national():
        latest_data = get_national_latest_data()
        if latest_data is None:
            return "N/A"
        return f"{int(latest_data['positive']):,}"

    @render.text
    def val_total_deaths_national():
        latest_data = get_national_latest_data()
        if latest_data is None:
            return "N/A"
        return f"{int(latest_data['death']):,}"

    @render.text
    def val_hospitalized_national():
        latest_data = get_national_latest_data()
        if latest_data is None:
            return "N/A"
        return f"{int(latest_data['hospitalizedCurrently']):,}"

    # --- TAB 2 Output ---
    @reactive.Calc
    def get_state_latest_data():
        data = get_state_data() 
        if data.empty:
            return None
        return data.sort_values('date').iloc[-1] 

    @render.text
    def val_total_cases():
        latest_data = get_state_latest_data()
        if latest_data is None:
            return "N/A"
        return f"{int(latest_data['positive']):,}"

    @render.text
    def val_total_deaths():
        latest_data = get_state_latest_data()
        if latest_data is None:
            return "N/A"
        return f"{int(latest_data['death']):,}"

    @render.text
    def val_hospitalized():
        latest_data = get_state_latest_data()
        if latest_data is None:
            return "N/A"
        return f"{int(latest_data['hospitalizedCurrently']):,}"

    @render.plot
    def state_plot():
        data = get_state_data()
        if data.empty:
            return
        
        metric_label = input.metric_select()
        metric_col_name = metrics_map[metric_label] 
        
        fig, ax = plt.subplots(figsize=(12, 6))

        if "positiveIncrease" in metric_col_name:
            ax.bar(data['date'], data['positiveIncrease'], color='lightblue', alpha=0.6, label="Daily Cases")
        elif "deathIncrease" in metric_col_name:
            ax.bar(data['date'], data['deathIncrease'], color='lightgray', alpha=0.6, label="Daily Deaths")
    
        ax.plot(data['date'], data[metric_col_name], color='#007bc2', linewidth=2, label=metric_label)
        
        ax.set_title(f"{input.state_select()}: {metric_label} over time")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        fig.tight_layout()
        return fig

    # --- TAB 3 Output ---
    @render.plot
    def comparison_plot():
        data = get_comparison_data()
        if data.empty:
            return

        metric_label = input.compare_metric()
        metric_col_name = metrics_map[metric_label] 
        
        fig, ax = plt.subplots(figsize=(12, 7))
        for state in input.compare_states():
            state_data = data[data['state'] == state]
            ax.plot(state_data['date'], state_data[metric_col_name], label=state, linewidth=2)
            
        ax.set_title(f"Comparing {metric_label}")
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.tight_layout()
        return fig
    
    @render.data_frame
    def comparison_data_table():
        
        selected_date = pd.to_datetime(input.table_date_select())
        selected_states = input.compare_states()
        
        mask = (
            (df['state'].isin(selected_states)) &
            (df['date'] == selected_date)
        )
        data = df[mask]
        
        if data.empty:
            return pd.DataFrame()

        cols_to_show = {
            'date': 'Date',
            'state': 'State',
            'positiveIncrease': 'New Cases',
            'positiveIncrease_7day_avg': 'New Cases (7-Day Avg)',
            'deathIncrease': 'New Deaths',
            'deathIncrease_7day_avg': 'New Deaths (7-Day Avg)',
            'hospitalizedCurrently': 'Hospitalized'
        }
        
        display_cols = {k: v for k, v in cols_to_show.items() if k in data.columns}
        data_filtered = data[display_cols.keys()].rename(columns=display_cols)
        data_filtered['Date'] = data_filtered['Date'].dt.strftime('%Y-%m-%d')
        
        return data_filtered.sort_values('State', ascending=True)

app = App(app_ui, server)