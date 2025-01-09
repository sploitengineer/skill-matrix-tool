import matplotlib.pyplot as plt
import numpy as np

def generate_skill_matrix(languages, filename="static/skill_graph.png"):

    labels = list(languages.keys())
    values = list(languages.values())

    if len(labels) < 3:
        # Add dummy values for fewer than 3 languages
        labels += ["Dummy1", "Dummy2"][:3 - len(labels)]
        values += [0] * (3 - len(values))

    # Close the loop for the radar chart
    values += values[:1]
    labels += labels[:1]

    # Calculate the angles for the radar chart
    num_vars = len(labels)
    angles = [n / float(num_vars - 1) * 2 * np.pi for n in range(num_vars)]

    # Create the radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color="blue", alpha=0.25)
    ax.plot(angles, values, color="blue", linewidth=2)
    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels[:-1])  # Exclude the duplicate label

    # Save the graph with the specified filename
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
