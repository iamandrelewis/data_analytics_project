
from statistics import mean, median, mode

def calculate_analytics(rolls):
    """Calculate basic analytics from dice rolls."""
    try:
        return {
            "mean": mean(rolls),
            "median": median(rolls),
            "mode": mode(rolls),
            "count": len(rolls),
            "range": max(rolls) - min(rolls),
            "min": min(rolls),
            "max": max(rolls)
        }
    except Exception as e:
        print(f"Error calculating analytics: {e}")
        return {}
