import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2

def graph_chi(k, test_statistic, p_value):
    """
    Visualizes a chi-square distribution with critical regions and highlights:
    - Test statistic
    - Rejection region (at 0.05 significance level)
    - Acceptance region for H_0

    Parameters:
        k (int): Degrees of freedom.
        test_statistic (float): Observed chi-square test statistic.
        p_value (float): P-value associated with the test statistic.
    """
    # 1. Critical chi-square value for 0.05 significance level (right-tailed test)
    critical_value = chi2.ppf(0.95, k)

    # 2. Generate x values for the chi-square distribution
    x = np.linspace(0, critical_value + 3, 1000)  # Ensure we go slightly beyond the critical region
    y = chi2.pdf(x, k)

    # 3. Create the plot
    fig = go.Figure()

    # Main chi-square distribution curve
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='blue'),
                             name=f'Chi-Square Distribution (k={k})'))

    # Fill for the acceptance region (H_0 region)
    fig.add_trace(go.Scatter(
        x=np.append(x[x <= critical_value], critical_value),
        y=np.append(y[x <= critical_value], 0),
        fill='tozeroy',
        line=dict(color='green'),
        name="Acceptance Region"
    ))

    # Fill for the rejection region
    fig.add_trace(go.Scatter(
        x=np.append(x[x > critical_value], critical_value),
        y=np.append(y[x > critical_value], 0),
        fill='tozeroy',
        line=dict(color='red'),
        name="Rejection Region"
    ))

    # Add vertical line for the test statistic
    fig.add_trace(go.Scatter(
        x=[test_statistic, test_statistic],
        y=[0, chi2.pdf(test_statistic, k)],
        mode='lines',
        line=dict(color='purple', dash='dash'),
        name=f"Test Statistic ({test_statistic:.2f})"
    ))

    # Add vertical line for the critical value
    fig.add_trace(go.Scatter(
        x=[critical_value, critical_value],
        y=[0, chi2.pdf(critical_value, k)],
        mode='lines',
        line=dict(color='black', dash='dot'),
        name=f"Critical Value ({critical_value:.2f})"
    ))

    # 4. Annotations
    fig.add_annotation(
        x=test_statistic, 
        y=chi2.pdf(test_statistic, k),
        text=f"Test Statistic = {test_statistic:.2f}<br>p-Value = {p_value:.4f}",
        showarrow=True, arrowhead=1
    )

    # fig.add_annotation(
    #     x=critical_value+0.75, 
    #     y=1.5,
    #     text=f"Rejection Region (α = 0.05)",
    #     showarrow=False
    # )

    # 5. Layout and customization
    fig.update_layout(
        title=f"Chi-Square Distribution with k={k} Degrees of Freedom",
        xaxis_title="Chi-Square Value",
        yaxis_title="Probability Density Function",
        legend=dict(x=0.7, y=1.0),
        template="plotly_white"
    )

    return fig
