"""
FreedomIQ DCF Configuration

Three-scenario DCF with gradual growth fade
and WACC / terminal-growth sensitivity analysis.
"""

# ==========================================================
# Forecast assumptions
# ==========================================================

YEARS = 10


# ==========================================================
# Discount rate
# ==========================================================

DISCOUNT_RATE = 0.10


# ==========================================================
# Terminal growth
# ==========================================================

TERMINAL_GROWTH = 0.04


# ==========================================================
# Scenario adjustments
# ==========================================================

CONSERVATIVE_ADJUSTMENT = -0.03
BASE_ADJUSTMENT = 0.00
OPTIMISTIC_ADJUSTMENT = 0.03


# ==========================================================
# Growth boundaries
# ==========================================================

MIN_GROWTH = 0.03
MAX_GROWTH = 0.18


# ==========================================================
# Growth fade
# ==========================================================

FADE_FACTOR_YEAR_10 = 0.25


# ==========================================================
# DCF Sensitivity Analysis
# ==========================================================

# Discount-rate range used for sensitivity testing.

SENSITIVITY_DISCOUNT_RATES = (
    0.09,
    0.10,
    0.11,
    0.12,
)


# Terminal-growth range used for sensitivity testing.

SENSITIVITY_TERMINAL_GROWTHS = (
    0.03,
    0.04,
    0.05,
)