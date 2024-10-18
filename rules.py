# total revenue

import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # diplay purpose only
    WHITE = 4  # data is missing for this field

# This is a already written for your reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index):
    """Calculate total revenue from financial data."""
    try:
        return data["financials"][financial_index]["pnl"]["lineItems"]["net_revenue"]
    except (KeyError, IndexError):
        return 0

def total_borrowing(data: dict, financial_index):
    """Calculate ratio of total borrowings to total revenue."""
    try:
        financials = data["financials"][financial_index]
        long_term = financials["bs"]["liabilities"]["long_term_borrowings"] or 0
        short_term = financials["bs"]["liabilities"]["short_term_borrowings"] or 0
        total_borrowings = long_term + short_term
        revenue = total_revenue(data, financial_index)
        return total_borrowings / revenue if revenue != 0 else float('inf')
    except (KeyError, IndexError):
        return 0

def iscr(data: dict, financial_index):
    """Calculate Interest Service Coverage Ratio."""
    try:
        financials = data["financials"][financial_index]
        pnl = financials["pnl"]["lineItems"]
        
        # Get profit before interest and tax
        pbit = pnl["profit_before_interest_and_tax"]
        
        # Get depreciation
        depreciation = pnl["depreciation"]
        
        # Get interest expenses
        interest = pnl["interest"]
        
        # Calculate ISCR: (PBIT + Depreciation + 1) / (Interest + 1)
        # Adding 1 to denominator to avoid division by zero
        return (pbit + depreciation + 1) / (interest + 1)
    except (KeyError, IndexError):
        return 0

def iscr_flag(data: dict, financial_index):
    """Determine flag color based on ISCR value."""
    try:
        iscr_value = iscr(data, financial_index)
        return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED
    except:
        return FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    """Determine flag color based on total revenue exceeding 50 million."""
    try:
        revenue = total_revenue(data, financial_index)
        return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED
    except:
        return FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    """Determine flag color based on borrowing to revenue ratio."""
    try:
        ratio = total_borrowing(data, financial_index)
        return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
    except:
        return FLAGS.AMBER