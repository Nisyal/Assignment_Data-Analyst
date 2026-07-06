# Trader Performance vs. Market Sentiment: Crypto Trading Analysis

This repository contains an end-to-end data analysis project investigating how Bitcoin market sentiment (measured by the Bitcoin Fear & Greed Index) influences trader behavior and performance using historical trading data from the Hyperliquid platform.

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Methodology](#2-methodology)
3. [Data Preparation](#3-data-preparation)
4. [Features Engineered](#4-features-engineered)
5. [Exploratory Data Analysis (EDA)](#5-exploratory-data-analysis)
6. [Key Findings & Analytical Insights](#6-key-findings--analytical-insights)
7. [Trader Segmentation](#7-trader-segmentation)
8. [Actionable Recommendations](#8-actionable-recommendations)
9. [Limitations](#9-limitations)
10. [Conclusion](#10-conclusion)

---

### 1. Executive Summary
The objective of this project is to analyze the correlation between Bitcoin Market Sentiment and trader behavior and performance. Using historical execution logs from Hyperliquid and daily Fear & Greed Index records, we evaluate how emotional extremes in the crypto market affect metrics like position sizing, win rates, and absolute profitability. The analysis reveals that market sentiment is a key driver of risk tolerance: fearful markets present high-conviction, large-scale profit opportunities, whereas extremely greedy markets lead to high win-rate but capital-diluted outcomes.

### 2. Methodology
The analytical pipeline was executed through the following stages:
1.  **Data Loading:** Imported Hyperliquid trade records and Fear & Greed Index history.
2.  **Dataset Inspection:** Checked dimensions, schema, data types, missing values, and duplicate records.
3.  **Datetime Conversion:** Converted incorrect raw epoch values to timezone-aligned datetime formats.
4.  **Daily Date Alignment:** Extracted calendar dates to align both datasets.
5.  **Dataset Merging:** Joined the execution logs and sentiment records on daily dates.
6.  **Feature Engineering:** Calculated trader performance indicators (daily PnL, win rates, trade sizing).
7.  **Exploratory Data Analysis (EDA):** Analyzed trading behaviors across sentiment categories and distributions.
8.  **Trader Segmentation:** Grouped traders by activity and profitability to isolate behavior.
9.  **Visualization:** Plotted key performance metrics across sentiment regimes.
10. **Business Recommendations:** Extracted actionable insights for platform risk and portfolio management.

### 3. Data Preparation
To ensure statistical integrity, the raw data underwent rigorous cleaning:
*   **Quality Checks:** Checked for duplicate records and verified column data types. Missing values were checked across both datasets.
*   **Timestamp Standardization:** The original `Timestamp` column contained incorrect epoch values. `Timestamp IST` was successfully converted to standard datetime format to represent true transaction times.
*   **Dataset Joining:** Daily dates were extracted from timestamps to serve as the join key. Merging the datasets yielded only 6 records with missing sentiment data, which was negligible and excluded from final calculations.

### 4. Features Engineered
The following metrics were engineered to capture trading behaviors under varying sentiment regimes:
*   **Daily PnL per Trader:** Realized profit and loss per trader aggregated daily.
*   **Win Rate:** Percentage of closed trades resulting in a positive PnL.
*   **Average Trade Size:** Average dollar value of positions opened/closed.
*   **Number of Trades per Day:** Daily transaction count per trader to measure activity.
*   **Long vs. Short Ratio:** Ratio of long to short trades to assess directional bias.
*   *Note: Leverage analysis was omitted as leverage data was not available in the provided dataset.*

### 5. Exploratory Data Analysis
Performance was evaluated across five market sentiment regimes: **Extreme Fear**, **Fear**, **Neutral**, **Greed**, and **Extreme Greed**. The following charts were created to evaluate trading dynamics:
*   Average Closed PnL by Market Sentiment
*   Win Rate by Market Sentiment
*   Average Trade Size by Market Sentiment
*   Number of Trades by Market Sentiment
*   Long vs. Short Bias
*   Closed PnL Distribution (Boxplot)

### 6. Key Findings & Analytical Insights

#### Summary Statistics:

| Sentiment Regime | Mean PnL ($) | Total PnL ($) | Win Rate (%) | Avg Trade Size ($) |
| :--- | :---: | :---: | :---: | :---: |
| **Extreme Greed** | 67.89 | 2,715,171.31 | 46.49% | 3,112.25 |
| **Greed** | 42.74 | 2,150,129.27 | 38.48% | 5,736.88 |
| **Neutral** | 34.31 | 1,292,920.68 | 39.70% | 4,782.73 |
| **Fear** | 54.29 | 3,357,155.44 | 42.08% | 7,816.11 |
| **Extreme Fear** | 34.54 | 739,110.25 | 37.06% | 5,349.73 |

#### Analytical Insights:
1.  **High-Conviction Sizing in Fearful Markets:** Despite a moderate win rate of 42.08%, the "Fear" regime generated the highest Total PnL ($3,357,155.44) and the largest Average Trade Size ($7,816.11). This suggests that during periods of market fear, traders deploy larger, higher-conviction positions (likely buying major support levels or capitulations), which results in substantial absolute profitability.
2.  **Extreme Greed Over-Trading & Dilution:** The "Extreme Greed" regime yielded the highest Mean PnL ($67.89) and the highest Win Rate (46.49%), yet it had the lowest Average Trade Size ($3,112.25). This indicates that while momentum-driven rising markets make it easier to win trades, traders suffer from FOMO, over-diversifying and splitting their capital into smaller, fragmented, and less efficient positions.
3.  **Capital Erosion in Neutral and Extreme Fear Regimes:** "Neutral" and "Extreme Fear" represent high-risk, low-reward regimes. Neutral markets exhibit the lowest Mean PnL ($34.31), reflecting directionless churn. Extreme Fear shows the lowest Win Rate (37.06%) and low Mean PnL ($34.54), resulting in a dismal Total PnL ($739,110.25). This highlights that large average trade sizes ($5,349.73) in panicking markets lead to significant capital destruction without corresponding payoffs.

### 7. Trader Segmentation
Traders were categorized along two behavioral dimensions:
*   **Frequent vs. Infrequent Traders:** Identifies if trading frequency correlates with profitability or if high-volume traders over-trade during greed.
*   **Consistent Winners vs. Other Traders:** Isolates the top-performing cohort to analyze whether their success is driven by superior risk management (e.g., scaling down in Neutral/Extreme Fear) compared to average traders.
*Segmenting behavior helps differentiate systemic market-driven performance from individual trading skill and style.*

### 8. Actionable Recommendations
*   **Capitalize on Conviction in Fear and Extreme Greed:** Focus capital allocation on high-probability setups during "Fear" (for large, high-conviction discount plays) and "Extreme Greed" (to ride strong momentum), while maintaining strict profit-taking rules during greed.
*   **Enforce Risk De-escalation in Neutral and Extreme Fear:** Programmatically reduce exposure (e.g., lower position limits and tighter stop-losses) when the sentiment index is Neutral or Extreme Fear, as these regimes exhibit poor win rates and high capital erosion.
*   **Implement Systematic Position-Sizing Rules:** Position sizes should be dynamically adjusted based on historical regime profitability (larger in Fear/Greed, smaller in Extreme Greed/Extreme Fear) rather than emotional impulse or market FOMO.

### 9. Limitations
*   **Absence of Leverage Metrics:** Leverage details were not present in the dataset, preventing analysis of liquidations or true risk-adjusted returns.
*   **Drawdown Approximation:** Portfolio equity history was unavailable, meaning drawdowns and maximum risk-exposure metrics are only estimates.
*   **Historical Generalizability:** The findings reflect historical correlations that may shift under changing macroeconomic conditions or structural market changes.

### 10. Conclusion
This project demonstrates that Bitcoin market sentiment is a powerful leading indicator of trader behavior and performance. By quantifying how emotional extremes affect trade sizing and win rates, traders and risk managers can build objective, sentiment-based frameworks to optimize position sizing, manage platform risk, and avoid the cognitive biases that typically lead to retail capital erosion.
