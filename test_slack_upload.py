from app import upload_file_v2
import pandas as pd
import plotly.express as px


data = {
    'month': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01'],
    '# of activated': [100, 150, 200, 130, 180, 160],
    '# of acquired': [80, 120, 150, 110, 140, 130],
    '# of retained': [60, 100, 130, 90, 110, 105],
    '# of churned': [-30, -40, -50, -35, -45, -38]
}

df = pd.DataFrame(data)

# Create the stacked bar chart
fig = px.bar(df, x='month', y=['# of activated', '# of acquired', '# of retained', '# of churned'],
             title='Monthly User Metrics',
             labels={'value':'Count', 'month':'Month'},
             color_discrete_sequence=px.colors.qualitative.G10)
img = fig.to_image(format="png", width=800, height=600, scale=2)


upload_file_v2("C07DVELJPU0", img, "bar.png", "Bar for testing", "initial comment", "1721388970.104079")

