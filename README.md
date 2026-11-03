# CUSTOMER RETENTION DECISION SYSTEM

I built this project to answer a question every subscription business has: **we have a limited budget for retention offers, so which customers should get one?**

**Live app:** https://retention-engine.streamlit.app

## The problem

KKBox is a music streaming service with almost 1 million subscribers. About 9% of them leave each month. Giving everyone a discount wastes money, and giving it to the wrong people saves no one. I wanted to find the customers who are both likely to leave and worth keeping, and show how much money targeting them saves.

## How the project flows


I used Databricks for the large data because it was too big for my laptop, then moved to local Python once it was reduced to one row per customer.

## What I did

| Step | Notebook | What I did |
|---|---|---|
| 1 | `01_explore_data` | First look at the four KKBox files |
| 2 | `02_ETL_kkbox` | Cleaned and joined 18.4M logs and 1.4M payments in PySpark on Databricks, removing 4,200 invalid records |
| 3 | `02b_payment_history` | Rebuilt payment features using only data from before the prediction date |
| 4 | `03_analysis` | Found the main churn patterns (auto-renew off: 30% churn vs 4%) |
| 5 | `04_model` | Trained a LightGBM churn model and explained it with SHAP |
| 6 | `05_uplift` | Ran an A/B test and built an uplift model on 64,000 customers |
| 7 | `06_decision_engine` | Ranked customers by expected profit and set the best number to target |

## Key findings

- **I caught target leakage.** My first model scored well, but one input carried 77% of its importance. It used payment data from after the prediction date. I rebuilt the inputs from past payments only, and the honest model still scored **AUC 0.871**.
- **Auto-renew history is the main driver of churn**, which I confirmed with SHAP.
- **Offers work, but not equally for everyone.** In the A/B test, the email raised visits by 7.7 points (95% CI 7.0–8.3). My uplift model's top group responded about twice as strongly as the lowest.
- **Targeting by my model saves far more than random targeting.** On a NT$100,000 budget, my model gave a net profit of about **NT$126,780**, while random targeting **lost NT$77,412**.
- **The best cutoff is the top 11,302 customers**, for a maximum net profit of about NT$321,701.

## Assumptions

- A retention offer costs NT$50.
- An offer keeps 7.7% of at-risk customers, based on the lift I measured in the A/B test.
- The A/B test uses the Hillstrom email dataset, because KKBox has no record of offers being sent. The decision engine uses its measured lift as the offer success rate.

## Tools

Python (pandas, NumPy, scikit-learn, LightGBM, SHAP, matplotlib), PySpark, Databricks, Streamlit, Git and GitHub

## Data

- KKBox Churn Prediction Challenge (WSDM 2018), Kaggle
- Hillstrom Email Marketing dataset (MineThatData)

The raw data is not stored in this repo because of its size.

## About me

Bushra Fatima, Master of Data Science and Analytics student at the University of Calgary.
[LinkedIn](https://www.linkedin.com/in/bushraafatima) · [GitHub](https://github.com/bushra-fatima-hub)