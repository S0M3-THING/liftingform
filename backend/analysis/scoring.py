def clamp(
    value,
    minimum=0,
    maximum=100
):

    return max(
        minimum,
        min(maximum, value)
    )


def weighted_score(
    metrics,
    weights
):

    total = 0
    total_weight = 0

    for metric, weight in weights.items():

        if metric not in metrics:
            continue

        total += (
            metrics[metric]
            * weight
        )

        total_weight += weight

    if total_weight == 0:
        return 0

    return clamp(
        total / total_weight
    )