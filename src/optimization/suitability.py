def compute_suitability(ndvi, water, soil):
    """
    Compute suitability score (0-100) based on environmental factors
    """
    # Weighted average with emphasis on vegetation
    score = (ndvi * 0.4 + water * 0.3 + soil * 0.3) * 100
    
    # Add some randomness to simulate micro-variations
    import random
    score += random.uniform(-5, 5)
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    return round(score, 1)
