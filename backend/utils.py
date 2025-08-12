# utils.py

def is_garbage(label, confidence):
    """
    Returns True if the detected label is considered garbage
    and meets the confidence threshold.
    """
    return confidence >= 0.80  # 80% threshold

def get_garbage_price(label):
    """
    Returns the price per kg for the given garbage material.
    """
    prices = {
        "newspaper": "₹15/kg",
        "aluminium": "₹120/kg",
        "glass_bottle": "₹20/kg",
        "plastic_bottle": "₹25/kg"
    }
    return prices.get(label, "₹0")
