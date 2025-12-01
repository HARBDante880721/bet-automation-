def calculate_potential_winnings(stake, odd):
    
    return round(stake * odd, 2)


def calculate_combo_odds(odds_list):
   
    total = 1.0
    for odd in odds_list:
        total *= odd
    return round(total, 4)


def is_close(a, b, tolerance=0.01):
    
    return abs(a - b) <= tolerance