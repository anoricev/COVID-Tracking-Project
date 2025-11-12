from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('data/processed/states_daily_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])

# Calculate rolling averages
df['positiveIncrease_7day_avg'] = df.groupby('state')['positiveIncrease'].rolling(window=7).mean().round(3).reset_index(level=0, drop=True).fillna(0)
df['deathIncrease_7day_avg'] = df.groupby('state')['deathIncrease'].rolling(window=7).mean().round(3).reset_index(level=0, drop=True).fillna(0)
df['positivityRate_7day_avg'] = df.groupby('state')['positivityRate'].rolling(window=7).mean().round(3).reset_index(level=0, drop=True).fillna(0)

metrics_map = {
    "New Cases (7-Day Avg)": "positiveIncrease_7day_avg",
    "New Deaths (7-Day Avg)": "deathIncrease_7day_avg",
    "Positivity Rate (7-Day Avg)": "positivityRate_7day_avg",
    "Current Hospitalizations": "hospitalizedCurrently",
    "Total Cases (Cumulative)": "positive",
    "Total Deaths (Cumulative)": "death"
}
all_states = sorted(df['state'].unique().tolist())
min_date = df['date'].min()
max_date = df['date'].max()

# --- Define UI ---
app_ui = ui.page_fluid(

    ui.panel_title("COVID-19 State Dashboard"),
    
    ui.navset_tab(
        
        # --- TAB 1 ---
        ui.nav_panel("State Deep-Dive",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_select("state_select", "Select State:", all_states, selected="IL"),
                    ui.input_select("metric_select", "Select Metric:", list(metrics_map.keys()), selected="positiveIncrease_7day_avg"),
                    ui.input_date_range("date_range", "Date Range:", 
                                      start=min_date,
                                      end=max_date,
                                      min=min_date,
                                      max=max_date
                                     )
                ),
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

        # --- TAB 2 ---
        ui.nav_panel("State Comparison",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_selectize("compare_states", "Select States to Compare:", 
                                     all_states, selected=["NY", "CA", "IL"], multiple=True),
                    ui.input_select("compare_metric", "Metric to Compare:", list(metrics_map.keys()), selected="positiveIncrease_7day_avg"),
                    ui.input_date_range("compare_date_range", "Date Range:", 
                                      start=min_date,
                                      end=max_date,
                                      min=min_date, 
                                      max=max_date
                                     )
                ),
                ui.card(
                    ui.output_plot("comparison_plot")
                )
            )
        )
    )
)

# --- Server Logic ---
def server(input, output, session):
    
    # Filter data for TAB 1
    @reactive.Calc
    def get_state_data():
        mask = (
            (df['state'] == input.state_select()) &
            (df['date'] >= pd.to_datetime(input.date_range()[0])) &
            (df['date'] <= pd.to_datetime(input.date_range()[1]))
        )
        return df[mask]

    # Filter data for TAB 2
    @reactive.Calc
    def get_comparison_data():
        mask = (
            (df['state'].isin(input.compare_states())) &
            (df['date'] >= pd.to_datetime(input.compare_date_range()[0])) &
            (df['date'] <= pd.to_datetime(input.compare_date_range()[1]))
        )
        return df[mask]

    # --- TAB 1 Output ---
    @reactive.Calc
    def get_state_latest_data():
        mask = (df['state'] == input.state_select())
        return df[mask].sort_values('date').iloc[-1]

    @render.text
    def val_total_cases():
        return f"{int(get_state_latest_data()['positive']):,}"

    @render.text
    def val_total_deaths():
        return f"{int(get_state_latest_data()['death']):,}"

    @render.text
    def val_hospitalized():
        return f"{int(get_state_latest_data()['hospitalizedCurrently']):,}"

    @render.plot
    def state_plot():
        data = get_state_data()
        if data.empty:
            return
        
        metric_label = input.metric_select()
        metric_col_name = metrics_map[metric_label] 
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data['date'], data[metric_col_name], color='#007bc2', linewidth=2)
        
        ax.set_title(f"{input.state_select()}: {metric_label} over time")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.tight_layout()
        return fig

    # --- TAB 2 Output ---
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

app = App(app_ui, server)