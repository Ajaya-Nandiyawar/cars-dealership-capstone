import re

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    _analyzer = SentimentIntensityAnalyzer()
except ImportError:
    _analyzer = None

# Deterministic keywords fallback for offline / isolated environments
POSITIVE_WORDS = {
    "fantastic", "great", "excellent", "amazing", "good", "wonderful",
    "superb", "outstanding", "perfect", "love", "awesome", "best",
    "happy", "friendly", "helpful", "clean", "satisfied", "pleased"
}

NEGATIVE_WORDS = {
    "terrible", "awful", "horrible", "bad", "worst", "poor", "rude",
    "scam", "disappointed", "broken", "unhappy", "slow", "waste", "cheat"
}


def analyze_text_sentiment(text: str) -> dict:
    """
    Analyze sentiment of a text string.
    Returns:
        {
            "sentiment": "positive" | "negative" | "neutral",
            "score": float (-1.0 to 1.0),
            "label": "positive" | "negative" | "neutral"
        }
    """
    if not text or not text.strip():
        return {
            "sentiment": "neutral",
            "score": 0.0,
            "label": "neutral",
        }

    clean_text = text.strip()

    if _analyzer is not None:
        scores = _analyzer.polarity_scores(clean_text)
        compound = float(scores.get("compound", 0.0))
        if compound >= 0.05:
            sentiment_label = "positive"
        elif compound <= -0.05:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        return {
            "sentiment": sentiment_label,
            "score": round(compound, 4),
            "label": sentiment_label,
            "details": scores,
        }

    # Deterministic fallback based on lexical polarity
    words = re.findall(r"\b\w+\b", clean_text.lower())
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)

    if pos_count > neg_count:
        sentiment_label = "positive"
        score = 0.5 + min(0.5, (pos_count - neg_count) * 0.1)
    elif neg_count > pos_count:
        sentiment_label = "negative"
        score = -0.5 - min(0.5, (neg_count - pos_count) * 0.1)
    else:
        sentiment_label = "neutral"
        score = 0.0

    return {
        "sentiment": sentiment_label,
        "score": round(score, 4),
        "label": sentiment_label,
        "details": {"positive_matches": pos_count, "negative_matches": neg_count},
    }
