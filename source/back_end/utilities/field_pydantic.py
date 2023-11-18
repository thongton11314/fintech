from pydantic import BaseModel, Field

MIN_DESCRIPTION = 50
MAX_DESCRIPTION = 150

class IncomeStatementInsights(BaseModel):
    revenue_health: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Provides insight into the company's total revenue, reflecting the health of the primary business activity.")
    operational_efficiency: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Analyzes the company's operating expenses relative to its revenue, indicating operational efficiency.")
    r_and_d_focus: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Highlights the company's investment in research and development, signifying its commitment to innovation.")
    debt_management: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Assesses the company's interest expenses, indicating its debt management strategy.")
    profit_retention: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Reviews the company's net income, showcasing profit after all expenses.")

class BalanceSheetInsights(BaseModel):
    liquidity_position: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Evaluates the company's ability to handle short-term obligations using liquid assets.")
    operational_efficiency: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Analyzes the efficiency of asset utilization to generate sales.")
    capital_structure: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Examines the company's mix of debt and equity financing.")
    inventory_management: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Studies the company's inventory turnover and management strategy.")
    overall_solvency: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Assesses the company's ability to meet long-term financial obligations.")
    assets_efficiency: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Analyzes how effectively the company's assets are used to generate sales.")

class CashFlowInsights(BaseModel):
    operational_cash_efficiency: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Evaluates the efficiency of cash generation from core operations.")
    investment_capability: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Highlights the company's reinvestment potential from operating cash flows.")
    financial_flexibility: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Assesses surplus cash after primary expenses, indicating financial flexibility.")
    dividend_sustainability: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Reviews the company's ability to sustain dividend payouts using net earnings.")
    debt_service_capability: str = Field(..., description=f"Must be between {MIN_DESCRIPTION} and {MAX_DESCRIPTION} words. Analyzes the company's ability to service debt from operational cash flows.")

class FiscalYearHighlights(BaseModel):
    performance_highlights: str = Field(..., description="Summarizes key financial and performance metrics for the fiscal year.")
    major_events: str = Field(..., description="Outlines significant events, acquisitions, or strategic pivots during the year.")
    challenges_encountered: str = Field(..., description="Enumerates challenges faced and strategies employed for resolution.")

class StrategyOutlookFutureDirection(BaseModel):
    strategic_initiatives: str = Field(..., description="Presents the company's main objectives and growth strategies for the forthcoming years.")
    market_outlook: str = Field(..., description="Provides insights into the expected market landscape, industry trends, and competition.")
    product_roadmap: str = Field(..., description="Describes planned product launches, expansions, and innovations.")

class RiskManagement(BaseModel):
    risk_factors: str = Field(..., description="Identifies primary risks and potential challenges.")
    risk_mitigation: str = Field(..., description="Details strategies to manage and mitigate identified risks.")

class CorporateGovernanceSocialResponsibility(BaseModel):
    board_governance: str = Field(..., description="Highlights the company's board composition, governance policies, and leadership dynamics.")
    csr_sustainability: str = Field(..., description="Describes the company's approach to environmental, community, and ethical practices.")

class InnovationRnD(BaseModel):
    r_and_d_activities: str = Field(..., description="Outlines the company's focus on research and development and key achievements.")
    innovation_focus: str = Field(..., description="Highlights areas of technological advancement, patents, or novel research.")
