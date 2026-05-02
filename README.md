# ACA Family Glitch Policy Simulation

## Methodology & Data Synthesis

### 1. Synthetic Population Generation
To evaluate the impact of the 2023 'Family Glitch' fix without utilizing PII, this model employs **Synthetic Data Generation**. We simulated 50,000 households to ensure statistical significance and to capture the variance in national employer-sponsored insurance (ESI) costs.

### 2. Distribution Selection & Reasoning
The model utilizes two primary distributions to mirror the 2023 economic landscape:

*   **Income Distribution (Triangular):** We selected a Triangular distribution ($Min: 100, Mode: 250, Max: 650$) over a standard Chi-Square to provide more granular control over the policy-relevant "subsidy sweet spot." By centering the mode at **250% FPL**, we simulate the high-density population eligible for both Enhanced Subsidies (via the IRA) and Cost-Sharing Reductions (CSRs).
*   **Premium Distribution (Gaussian):** Employer-sponsored family premiums are modeled using a **Normal Distribution** ($\mu=1100, \sigma=300$). This reflects the natural market variance where most premiums cluster around the national average, with outliers representing high-benefit and low-benefit firms.

### 3. Causal Logic: The Affordability Threshold
The core engine identifies "Marketplace Migration" by calculating the **Affordability Ratio (AR)**:
$$AR = \frac{Employer\_Family\_Premium}{Monthly\_Household\_Income}$$

If $AR > 9.12\%$, the household is flagged as `newly_eligible`. This simulates the 2023 structural break where eligibility shifted from individual-only costs to total family costs.

### 4. Monte Carlo Approach
By running 50,000 iterations, the model provides a **Sensitivity Analysis** that predicts how migration rates fluctuate if the federal government adjusts the 9.12% threshold.