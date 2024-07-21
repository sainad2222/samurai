import pandas as pd
import plotly.express as px
import numpy as np

def generate_chart(df):
    # Convert categorical columns to datetime where possible
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    numerical_cols = df.select_dtypes(include=[int, float]).columns

    for col in categorical_cols:
        df[col] = pd.to_datetime(df[col], errors='ignore')

    # Check for datetime-like columns
    datetime_cols = [col for col in df.columns if pd.api.types.is_datetime64_dtype(df[col])]

    if len(df) == 1:
        return
    elif 'id' in df.columns.str.lower().values:
        return
    
    elif any('id' in col.lower() for col in df.columns):
        return
    
    elif df.select_dtypes(include=[object]).shape[1] == df.shape[1]:
        return

    elif len(datetime_cols) == 1:
        date_col = datetime_cols[0]
        if len(numerical_cols) >= 1:
            less_than_one_cols = [col for col in numerical_cols if df[col].max() <= 1]
            other_numerical_cols = [col for col in numerical_cols if col not in less_than_one_cols]

            if less_than_one_cols:
                fig = px.line(df, x=date_col, y=less_than_one_cols, markers=True)
                for col in other_numerical_cols:
                    fig.add_scatter(x=df[date_col], y=df[col], mode='lines', name=col, yaxis='y2')
                fig.update_layout(title="Dual-Axis Line Chart",
                                  yaxis2=dict(title='Values > 1', overlaying='y', side='right'))
                return fig

    # Proceed with other cases if no datetime-like columns or other cases
    if len(categorical_cols) == 0:
        return None

    if len(categorical_cols) == 1 and len(numerical_cols) > 1:
        cat_col = categorical_cols[0]
        fig = px.line(df, x=cat_col, y=numerical_cols, markers=True)
        fig.update_layout(title="Line Chart")
        return fig

    elif len(categorical_cols) == 1 and len(numerical_cols) == 1:
        cat_col = categorical_cols[0]
        num_col = numerical_cols[0]
        if df[num_col].max() <= 1:
            fig = px.pie(df, names=cat_col, values=num_col)
            fig.update_layout(title="Pie Chart")
            return fig
        else:
            fig = px.bar(df, x=cat_col, y=num_col, color_discrete_sequence=["#00B899"])
            fig.update_layout(title="Bar Chart")
            for i, row in df.iterrows():
                fig.add_annotation(
                    x=row[categorical_cols[0]],
                    y=row[numerical_cols[0]],
                    text=f"{row[numerical_cols[0]]}",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-30,
                )
            return fig

    elif len(categorical_cols) == 2 and len(numerical_cols) == 1:
        cat_cols = categorical_cols
        num_col = numerical_cols[0]
        fig = px.bar(df, x=cat_cols[0], y=num_col, color=cat_cols[1], text_auto=True)
        fig.update_layout(title="Stacked Bar Chart", barmode='stack')
        return fig

    elif len(categorical_cols) == 1 and len(numerical_cols) > 1:
        cat_col = categorical_cols[0]
        fig = px.bar(df, x=cat_col, y=numerical_cols, color_discrete_sequence=["#00B899"])
        fig.update_layout(title="Bar Chart")
        for i, row in df.iterrows():
                fig.add_annotation(
                    x=row[categorical_cols[0]],
                    y=row[numerical_cols[0]],
                    text=f"{row[numerical_cols[0]]}",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-30,
                )
        return fig

    return None