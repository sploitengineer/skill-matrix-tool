import matplotlib.pyplot as plt

def generate_skill_matrix(languages, filename="static/skill_graph.png"):

    labels = list(languages.keys())
    values = list(languages.values())

    if len(labels) < 3:
        # Add dummy values for fewer than 3 languages
        labels += ["Dummy1", "Dummy2"]
        values += [0, 0]

    # Close the loop for the radar chart
    values += values[:1]
    labels += labels[:1]

    # Create the radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
    ax.fill(angles, values, color="blue", alpha=0.25)
    ax.plot(angles, values, color="blue", linewidth=2)
    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Save the graph with the specified filename
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
