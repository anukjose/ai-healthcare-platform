from collections import defaultdict


def detect_trend_old(values):

    if len(values) < 2:
        return "stable"

    if values[-1] > values[0]:
        return "increasing"

    elif values[-1] < values[0]:
        return "decreasing"

    return "stable"
def detect_trend(values):

    if len(values) < 2:
        return "stable"

    increases = 0
    decreases = 0

    # Compare consecutive values
    for i in range(1, len(values)):

        if values[i] > values[i - 1]:
            increases += 1

        elif values[i] < values[i - 1]:
            decreases += 1

    total_changes = increases + decreases

    if total_changes == 0:
        return "stable"

    increase_ratio = increases / total_changes
    decrease_ratio = decreases / total_changes

    # Mostly increasing
    if increase_ratio >= 0.75:
        return "increasing"

    # Mostly decreasing
    elif decrease_ratio >= 0.75:
        return "decreasing"

    # Very little variation
    variation = max(values) - min(values)

    avg = sum(values) / len(values)

    if avg != 0:

        variation_percent = variation / avg

        if variation_percent < 0.05:
            return "stable"

    # Otherwise
    return "fluctuating"

def generate_features(labs):

    grouped = defaultdict(list)

    # Group by test
    for lab in labs:
        grouped[lab["test"]].append(lab)

    facts = []
    summaries = []
    semantic_chunks = []

    # Process each test
    for test_name, entries in grouped.items():

        # Sort by date
        entries.sort(key=lambda x: x["date"])

        values = [e["value"] for e in entries]

        latest = entries[-1]

        trend = detect_trend(values)

        # -------------------------
        # 1. Exact Facts
        # -------------------------
        facts.extend(entries)

        # -------------------------
        # 2. Summary
        # -------------------------
        summary = {
            "patient_id": latest["patient_id"],
            "test": test_name,
            "latest_value": latest["value"],
            "trend": trend,
            "min_value": min(values),
            "max_value": max(values)
        }

        summaries.append(summary)

        # -------------------------
        # 3. Semantic Chunk
        # -------------------------
        history_lines = []

        for e in entries:
            history_lines.append(
                f"{e['date']}: {e['value']} {e['unit']}"
                )

        history_text = "\n".join(history_lines)

        chunk = (
            f"{test_name} history:\n"
            f"{history_text}\n"
            f"Overall pattern: {trend}."
            )

        semantic_chunks.append({
            "patient_id": latest["patient_id"],
            "chunk_type": "lab_summary",
            "content": chunk
        })

    print(f"✅ Generated {len(summaries)} summaries")
    print(f"✅ Generated {len(semantic_chunks)} semantic chunks")

    return facts, summaries, semantic_chunks