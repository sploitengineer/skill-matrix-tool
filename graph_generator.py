import matplotlib.pyplot as plt
import numpy as np

def generate_skill_matrix(languages):

    # Extract top languages
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    top_languages = sorted_languages[:6]
    labels = [lang for lang, _ in top_languages]
    values = [count for _, count in top_languages]

    # Normalize values for better visualization
    max_value = max(values)
    values = [v / max_value for v in values]

    # Create a hexagonal graph
    angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color="blue", alpha=0.25)
    ax.plot(angles, values, color="blue", linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Skill Matrix")

    # Save the graph
    plt.savefig("static/skill_graph.png")
    plt.close()
