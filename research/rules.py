"""
=========================================================
FreedomIQ Investment Rules
---------------------------------------------------------
This file contains all configurable investment thresholds.

Business logic should NEVER hardcode values.
Always import from this file.

Example:

from research.rules import PE_EXCELLENT
=========================================================
"""

# =========================================================
# SCORE WEIGHTS
# =========================================================

VALUATION_WEIGHT = 20
GROWTH_WEIGHT = 20
PROFITABILITY_WEIGHT = 20
FINANCIAL_STRENGTH_WEIGHT = 20
BUSINESS_QUALITY_WEIGHT = 20


# =========================================================
# VALUATION RULES
# =========================================================

PE_EXCELLENT = 15
PE_GOOD = 25

PEG_EXCELLENT = 1
PEG_GOOD = 2

PB_EXCELLENT = 3
PB_GOOD = 5

EV_EBITDA_EXCELLENT = 10
EV_EBITDA_GOOD = 15


# =========================================================
# GROWTH RULES
# =========================================================

REVENUE_GROWTH_EXCELLENT = 20
REVENUE_GROWTH_GOOD = 10

PROFIT_GROWTH_EXCELLENT = 20
PROFIT_GROWTH_GOOD = 10


# =========================================================
# PROFITABILITY RULES
# =========================================================

OPERATING_MARGIN_EXCELLENT = 20
OPERATING_MARGIN_GOOD = 10

ROE_EXCELLENT = 20
ROE_GOOD = 15

ROCE_EXCELLENT = 20
ROCE_GOOD = 15


# =========================================================
# FINANCIAL STRENGTH RULES
# =========================================================

DEBT_EQUITY_LOW = 50
DEBT_EQUITY_MEDIUM = 100

CURRENT_RATIO_GOOD = 2

INTEREST_COVERAGE_GOOD = 5


# =========================================================
# SCORE RANGES
# =========================================================

STRONG_BUY_SCORE = 90
BUY_SCORE = 75
HOLD_SCORE = 60
REDUCE_SCORE = 40


# =========================================================
# STAR RATINGS
# =========================================================

FIVE_STAR = "★★★★★"
FOUR_STAR = "★★★★☆"
THREE_STAR = "★★★☆☆"
TWO_STAR = "★★☆☆☆"
ONE_STAR = "★☆☆☆☆"