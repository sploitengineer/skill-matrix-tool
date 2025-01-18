import plotly.graph_objects as go

def generate_skill_matrix(languages, static_filename="static/skill_graph.png", interactive_filename="static/skill_graph.html", color="blue", opacity=1.0, size="medium"):



    valid_colors = {"blue": "rgba(0, 0, 255, {opacity})", "green": "rgba(0, 255, 0, {opacity})", "red": "rgba(255, 0, 0, {opacity})", "magenta": "rgba(255, 0, 255, {opacity})"}
    fill_color = valid_colors.get(color, "rgba(0, 0, 255, {opacity})").format(opacity=opacity)

    #
    # labels = list(languages.keys())
    # values = list(languages.values())

    # Sort and get the top 10 most used languages
    sorted_languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)[:10])
    labels = list(sorted_languages.keys())
    values = list(sorted_languages.values())


    if len(labels) < 3:
        # Add dummy values for fewer than 3 languages
        labels += ["Dummy1", "Dummy2"][:3 - len(labels)]
        values += [0] * (3 - len(values))

    # Normalize values to a smaller range (0 to 10)
    max_value = max(values) if max(values) > 0 else 1  # Avoid division by zero
    values = [v / max_value * 10 for v in values]

    # Close the loop for the radar chart
    values += values[:1]
    labels += labels[:1]

    # Adjust graph size
    if size == "small":
        graph_width, graph_height = 500, 400
    elif size == "large":
        graph_width, graph_height = 1000, 800
    else:  # Default to medium
        graph_width, graph_height = 700, 600

    # Create the radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        # fillcolor=color if opacity == 1.0 else f"rgba(0, 0, 255, {opacity})",
        fillcolor=fill_color,
        name="Skill Matrix",
        marker=dict(color="rgba(0,128,255,0.7)"),
        hovertemplate="<b>Skill:</b> %{theta}<br><b>Score:</b> %{r:.1f}/10<extra></extra>"  #To customize tooltips for each point on the graph
        ##Info about complicate above format code for my future self
        # %{theta}: Displays the skill name (language).
        # %{r:.1f}: Displays the score (normalized value) to one decimal place.
        # <extra></extra>: Removes the default extra information displayed by Plotly
    ))

    # aesthetics
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10], #Set fixed range after normalization
                showline=True,
                showticklabels=True,
                tickformat=".0f",  # No scientific notation, no abbreviations (Ensure plain numbers)
            )
        ),
        showlegend=False,
        title="Skill Matrix Graph",
        width=graph_width,
        height=graph_height,
        font=dict(family="Arial, sans-serif", size=12, color="#4a4a4a")
    )
    #Save the static image
    fig.write_image(static_filename)

    # Save the chart as an interactive HTML file
    fig.write_html(interactive_filename)
