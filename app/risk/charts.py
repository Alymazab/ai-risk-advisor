import math
import matplotlib.pyplot as plt


def generate_risk_chart(scores: dict):
    categories = list(scores.keys())
    values = list(scores.values())

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(categories, values)
    ax.set_ylim(0, 100)
    ax.set_title("NIST Function Risk Scores")
    ax.set_ylabel("Risk Score")
    ax.tick_params(axis="x", rotation=25)

    return fig


def generate_radar_chart(scores: dict):
    labels = list(scores.keys())
    values = list(scores.values())

    if not labels:
        labels = ["GOVERN", "MAP", "MEASURE", "MANAGE"]
        values = [0, 0, 0, 0]

    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    values += values[:1]
    angles += angles[:1]

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 100)
    ax.set_title("AI Risk Posture Radar", pad=20)

    return fig


def generate_likelihood_impact_matrix(likelihood_score: int, impact_score: int):
    fig, ax = plt.subplots(figsize=(6, 5))

    matrix = [
        [1, 2, 3],
        [2, 3, 4],
        [3, 4, 5],
    ]

    ax.imshow(matrix)

    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])

    ax.set_xticklabels(["Low", "Medium", "High"])
    ax.set_yticklabels(["Low", "Medium", "High"])

    ax.set_xlabel("Likelihood")
    ax.set_ylabel("Impact")
    ax.set_title("Likelihood vs Impact Matrix")

    x = 0 if likelihood_score < 34 else 1 if likelihood_score < 67 else 2
    y = 0 if impact_score < 34 else 1 if impact_score < 67 else 2

    ax.scatter(x, y, s=350, marker="o")
    ax.text(x, y, "AI\nRisk", ha="center", va="center", fontsize=10, fontweight="bold")

    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(matrix[i][j]), ha="center", va="center")

    return fig