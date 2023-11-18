# Define paths, get files from current root
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

# Import needed libraries, functions
import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go

# Import needed libraries, my libraries & functions
from source.back_end.utilities.pydantic_models import IncomeStatementInsights
from source.back_end.utilities.utils import insights, safe_float, generate_pydantic_model
from source.back_end.utilities.field import inc_stat_attributes, inc_stat_fields
from source.back_end.utilities.field2 import inc_stat, inc_stat_attributes


#AV_API_KEY = st.secrets["av_api_key"]
#OPENAI_API_KEY = st.secrets["openai_api_key"]
AV_API_KEY = "IG746NOPEXGCM4BS"

def safe_divide(numerator, denominator):
    """Safely divide two numbers, considering possible "N/A" values or zero denominator."""
    if "N/A" in (numerator, denominator) or denominator == 0:
        return "N/A"
    return numerator / denominator

def charts(data):
    """Extract and return financial data arrays from the annual reports for plotting."""
    dates = []
    total_revenue = []
    net_income = []
    interest_expense = []

    for report in reversed(data["annualReports"]):
        dates.append(report["fiscalDateEnding"])
        total_revenue.append(report["totalRevenue"])
        net_income.append(report["netIncome"])
        interest_expense.append(report["interestAndDebtExpense"])

    return {
        "dates": dates,
        "total_revenue": total_revenue,
        "net_income": net_income,
        "interest_expense": interest_expense
    }
    
def metrics(data):
    """Calculate and return various financial metrics based on the data."""
    # Extract values
    grossProfit = safe_float(data.get("grossProfit"))
    totalRevenue = safe_float(data.get("totalRevenue"))
    operatingIncome = safe_float(data.get("operatingIncome"))
    costOfRevenue = safe_float(data.get("costOfRevenue"))
    costofGoodsAndServicesSold = safe_float(data.get("costofGoodsAndServicesSold"))
    sellingGeneralAndAdministrative = safe_float(data.get("sellingGeneralAndAdministrative"))
    ebit = safe_float(data.get("ebit"))
    interestAndDebtExpense = safe_float(data.get("interestAndDebtExpense"))
    netIncome = safe_float(data.get("netIncome"))

    # Calculate metrics
    gross_profit_margin = safe_divide(grossProfit, totalRevenue)
    operating_profit_margin = safe_divide(operatingIncome, totalRevenue)
    net_profit_margin = safe_divide(netIncome, totalRevenue)
    cost_efficiency = safe_divide(totalRevenue, (costOfRevenue + costofGoodsAndServicesSold))
    sg_and_a_efficiency = safe_divide(totalRevenue, sellingGeneralAndAdministrative)
    interest_coverage_ratio = safe_divide(ebit, interestAndDebtExpense)

    # Returning the results
    return {
        "gross_profit_margin": gross_profit_margin,
        "operating_profit_margin": operating_profit_margin,
        "net_profit_margin": net_profit_margin,
        "cost_efficiency": cost_efficiency,
        "sg_and_a_efficiency": sg_and_a_efficiency,
        "interest_coverage_ratio": interest_coverage_ratio,
    }

def income_statement(symbol, fields_to_include, openAI_user_key):
    """
    Fetch and process the income statement for a given company symbol.
    Return metrics, chart data, and insights for the specified fields.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }

    response = requests.get(url, params=params)
    
    # Error handling for the API request
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    data = response.json()
    if not data:
        print(f"No data found for {symbol}")
        return None
    
    # Print out to terminal
    print(data)
    
    chart_data = charts(data)
    report = data["annualReports"][0]
    met = metrics(report)

    data_for_insights = {
        "annual_report_data": report,
        "historical_data": chart_data,
    }

    ins = {}
    for i, field in enumerate(inc_stat_attributes):
        if fields_to_include[i]:
            response = insights(field, "income statement", data_for_insights, str({field: inc_stat[field]}), openAI_user_key)
            ins[field] = response

    return {
        "metrics": met,
        "chart_data": chart_data,
        "insights": ins
    }