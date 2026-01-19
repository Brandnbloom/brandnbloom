def engagement_rate(likes: int, comments: int, followers: int) -> float:
    if followers <= 0:
        return 0.0
    return round(((likes + comments) / followers) * 100, 2)
