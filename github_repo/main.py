import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/kay/Documents")
DB_PATH = ROOT / "psychdataai.db"
CHART_PATH = ROOT / "psychdataai_ethnic_comparison.png"


def initialize_database() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS ethnic_mental_health")
    cur.execute(
        """
        CREATE TABLE ethnic_mental_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            utilization_rate REAL NOT NULL,
            access_rate REAL NOT NULL,
            treatment_rate REAL NOT NULL,
            stigma_score REAL NOT NULL,
            self_advocacy_score REAL NOT NULL,
            stereotype_summary TEXT NOT NULL,
            impact_summary TEXT NOT NULL
        )
        """
    )

    rows = [
        (
            "White",
            68.0,
            72.0,
            69.0,
            32.0,
            67.0,
            "Often treated as the default benchmark, which can hide the unique barriers experienced by other communities.",
            "White populations may still face stigma, but they are less likely to be stereotyped as culturally incompatible with mental health care.",
        ),
        (
            "Black/African American",
            48.0,
            55.0,
            50.0,
            64.0,
            58.0,
            "Stereotypes of strength, emotional suppression, or being 'too angry' can discourage open conversations about mental health.",
            "These beliefs can delay treatment, reduce trust in providers, and make self-advocacy harder in care settings.",
        ),
        (
            "Hispanic/Latino",
            47.0,
            52.0,
            49.0,
            61.0,
            56.0,
            "Cultural expectations around family duty, privacy, and machismo can create barriers to seeking help.",
            "Stigma and fear of judgment can reduce help-seeking and make people less likely to advocate for culturally appropriate care.",
        ),
        (
            "Asian American",
            43.0,
            50.0,
            47.0,
            59.0,
            54.0,
            "The 'model minority' stereotype can pressure people to appear high-functioning and suppress emotional distress.",
            "This can lead to underreporting symptoms, delayed care, and reluctance to challenge providers or seek support.",
        ),
        (
            "Native American/Alaska Native",
            40.0,
            46.0,
            42.0,
            72.0,
            51.0,
            "Historical trauma, cultural loss, and stereotypes of dysfunction or dependency can intensify stigma.",
            "These experiences can undermine trust, heighten barriers to care, and weaken self-advocacy when services are not culturally grounded.",
        ),
        (
            "Multiracial",
            46.0,
            53.0,
            48.0,
            58.0,
            57.0,
            "Identity invalidation and being treated as 'less authentic' can create emotional strain and skepticism toward systems.",
            "These pressures can make people feel unseen, avoid care, and struggle to assert their needs confidently.",
        ),
    ]

    cur.executemany(
        """
        INSERT INTO ethnic_mental_health (
            group_name,
            utilization_rate,
            access_rate,
            treatment_rate,
            stigma_score,
            self_advocacy_score,
            stereotype_summary,
            impact_summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    conn.close()


def load_comparisons() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT
            group_name,
            utilization_rate,
            access_rate,
            treatment_rate,
            stigma_score,
            self_advocacy_score,
            stereotype_summary,
            impact_summary
        FROM ethnic_mental_health
        WHERE group_name != 'White'
        ORDER BY utilization_rate ASC
        """
    ).fetchall()
    conn.close()

    baseline = {
        "utilization_rate": 68.0,
        "access_rate": 72.0,
        "treatment_rate": 69.0,
    }

    comparisons = []
    for row in rows:
        comparisons.append(
            {
                "group_name": row["group_name"],
                "utilization_rate": row["utilization_rate"],
                "access_rate": row["access_rate"],
                "treatment_rate": row["treatment_rate"],
                "stigma_score": row["stigma_score"],
                "self_advocacy_score": row["self_advocacy_score"],
                "stereotype_summary": row["stereotype_summary"],
                "impact_summary": row["impact_summary"],
                "util_gap": row["utilization_rate"] - baseline["utilization_rate"],
                "access_gap": row["access_rate"] - baseline["access_rate"],
                "treatment_gap": row["treatment_rate"] - baseline["treatment_rate"],
            }
        )
    return comparisons


def create_chart(comparisons: list[dict]) -> None:
    groups = [item["group_name"] for item in comparisons]
    util_gap = [item["util_gap"] for item in comparisons]
    access_gap = [item["access_gap"] for item in comparisons]
    treatment_gap = [item["treatment_gap"] for item in comparisons]
    stigma = [item["stigma_score"] for item in comparisons]
    advocacy = [item["self_advocacy_score"] for item in comparisons]

    x = np.arange(len(groups))
    width = 0.22

    fig, axes = plt.subplots(2, 1, figsize=(12, 9), constrained_layout=True)

    axes[0].bar(x - width, util_gap, width, label="Utilization gap vs White")
    axes[0].bar(x, access_gap, width, label="Access gap vs White")
    axes[0].bar(x + width, treatment_gap, width, label="Treatment gap vs White")
    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].set_title("Mental health service gaps versus White baseline")
    axes[0].set_ylabel("Percentage-point gap")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(groups, rotation=35, ha="right")
    axes[0].legend()
    axes[0].grid(axis="y", linestyle="--", alpha=0.4)

    axes[1].bar(x - width / 2, stigma, width, label="Stigma burden")
    axes[1].bar(x + width / 2, advocacy, width, label="Self-advocacy")
    axes[1].set_title("Stigma burden and self-advocacy by ethnic group")
    axes[1].set_ylabel("Score (0-100)")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(groups, rotation=35, ha="right")
    axes[1].legend()
    axes[1].grid(axis="y", linestyle="--", alpha=0.4)

    fig.suptitle("PsychDataAI: Mental Health Equity Snapshot")
    fig.savefig(CHART_PATH, dpi=300, bbox_inches="tight")
    plt.close(fig)


def print_summary(comparisons: list[dict]) -> None:
    print("PsychDataAI: Mental Health Equity Snapshot")
    print("=" * 48)
    print("An illustrative SQL-backed analysis comparing ethnic groups to White baseline data.\n")

    for item in comparisons:
        print(
            f"{item['group_name']}: utilization {item['utilization_rate']}% "
            f"(gap {item['util_gap']:+.1f} pts), access {item['access_rate']}% "
            f"(gap {item['access_gap']:+.1f} pts), treatment {item['treatment_rate']}% "
            f"(gap {item['treatment_gap']:+.1f} pts)"
        )
        print(f"  Stereotype: {item['stereotype_summary']}")
        print(f"  Impact: {item['impact_summary']}\n")

    print(f"Chart saved to: {CHART_PATH}")


def main() -> None:
    initialize_database()
    comparisons = load_comparisons()
    create_chart(comparisons)
    print_summary(comparisons)


if __name__ == "__main__":
    main()
