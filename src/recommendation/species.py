def recommend_species(ndvi, water, soil):
    """
    Recommend plantation species based on environmental factors
    """
    # Simple logic based on Indian native species
    if ndvi > 0.7 and water > 0.6 and soil > 0.7:
        # Excellent conditions
        return ["Neem (Azadirachta indica)", "Bamboo", "Peepal (Ficus religiosa)", 
                "Banyan (Ficus benghalensis)", "Arjun (Terminalia arjuna)"]
    
    elif ndvi > 0.5 and water > 0.4 and soil > 0.5:
        # Good conditions
        return ["Babool (Acacia nilotica)", "Khejri (Prosopis cineraria)", 
                "Ber (Ziziphus mauritiana)", "Amaltas (Cassia fistula)"]
    
    elif ndvi > 0.3 and water > 0.3:
        # Moderate conditions
        return ["Babool", "Khejri", "Dhak (Butea monosperma)", "Khair (Acacia catechu)"]
    
    else:
        # Poor conditions - hardy species
        return ["Babool", "Khejri", "Date Palm"]
