import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

class ACAPolicyModel:
    """
    Simulates the 2023 'Family Glitch' structural break to evaluate 
    household eligibility migration and budgetary impact.
    """
    def __init__(self, sample_size=25000):
        self.sample_size = sample_size
        self.data = self._generate_synthetic_population()

    def _generate_synthetic_population(self):
        """Generates a dataset mimicking US demographics without using PII."""
        np.random.seed(42) # Ensures reproducible research
        
        # 1. Income as % of Federal Poverty Level (FPL) - Triangular Distribution
        fpl_percentage = np.random.triangular(100, 250, 650, self.sample_size)
        
        # 2. Employer-Sponsored Family Premiums - Normal Distribution
        family_premiums = np.random.normal(1100, 300, self.sample_size).clip(400, 2800)
        
        df = pd.DataFrame({
            'household_id': range(self.sample_size),
            'fpl_perc': fpl_percentage,
            'employer_monthly_premium': family_premiums
        })
        
        # 3. Derive Monthly Household Income (2024 FPL proxy: ~$25k/yr for family of 3)
        df['monthly_income'] = (df['fpl_perc'] * 25820 / 100) / 12
        return df

    def run_causal_analysis(self, threshold=0.0912):
        """Quantifies the impact of the regulatory fix on market migration."""
        # Calculate Affordability Ratio
        self.data['affordability_ratio'] = self.data['employer_monthly_premium'] / self.data['monthly_income']
        
        # Causal Break: Eligibility before was based on 'Individual' cost; now 'Family' cost.
        # This identifies the households newly eligible for subsidies.
        self.data['newly_eligible'] = self.data['affordability_ratio'] > threshold
        return self.data

    def export_artifacts(self, folder='data'):
        """Saves synthetic data for audit/review, establishing an ETL pipeline."""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        path = f"{folder}/synthetic_aca_households.csv"
        self.data.to_csv(path, index=False)
        print(f"[SUCCESS] Synthetic dataset exported to: {path}")

    def generate_sensitivity_plot(self, folder='plots'):
        """Visualizes how changes in the 9.12% threshold impact eligibility."""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        thresholds = [0.07, 0.08, 0.085, 0.0912, 0.095, 0.10, 0.11]
        migration_rates = []
        
        for t in thresholds:
            rate = (self.data['employer_monthly_premium'] / self.data['monthly_income'] > t).mean()
            migration_rates.append(rate * 100)

        plt.figure(figsize=(10, 5))
        plt.plot(thresholds, migration_rates, marker='o', linestyle='-', color='#2c3e50')
        plt.axvline(x=0.0912, color='r', linestyle='--', label='Actual Threshold (9.12%)')
        plt.title('Sensitivity Analysis: ACA Migration vs. Affordability Threshold')
        plt.xlabel('Regulatory Affordability Threshold')
        plt.ylabel('% Households Newly Eligible')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plot_path = f"{folder}/sensitivity_analysis.png"
        plt.savefig(plot_path)
        print(f"[SUCCESS] Visualization saved to: {plot_path}")

if __name__ == "__main__":
    # Initialize and execute the pipeline
    print("--- Initializing ACA Causal Inference Framework ---")
    model = ACAPolicyModel(sample_size=50000)
    
    # Run the model logic
    model.run_causal_analysis()
    
    # Generate data and visuals
    model.export_artifacts()
    model.generate_sensitivity_plot()
    
    # Print high-level Business Intelligence
    migration_rate = model.data['newly_eligible'].mean()
    print(f"\nFinal Analysis Results:")
    print(f"Total Population Simulated: 50,000")
    print(f"Projected Marketplace Migration Rate: {migration_rate:.2%}")