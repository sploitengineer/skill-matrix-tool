import plotly.graph_objects as go

def generate_skill_matrix(languages, filename="static/skill_graph.png"):
    """
    This generates a skill matrix graph with Plotly and save it as an image.
    """
    labels = list(languages.keys())
    values = list(languages.values())

    if len(labels) < 3:
        # Add dummy values for fewer than 3 languages
        labels += ["Dummy1", "Dummy2"][:3 - len(labels)]
        values += [0] * (3 - len(values))

    # Close the loop for the radar chart
    values += values[:1]
    labels += labels[:1]

    # Create the radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name="Skill Matrix",
        marker=dict(color="rgba(0,128,255,0.7)")
    ))

    # aesthetics
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) + 1],
                showline=True,
                showticklabels=True,
                tickformat=".0f",  # No scientific notation, no abbreviations
            )
        ),
        showlegend=False,
        title="Skill Matrix Graph",
        font=dict(family="Arial, sans-serif", size=12, color="#4a4a4a")
    )

    # Save the chart as a static image
    fig.write_image(filename)
