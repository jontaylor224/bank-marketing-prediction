# Bank Marketing Prediction

## Project Overview

Can information available about a customer and prior marketing campaign interactions help a bank prioritize customers who may subscribe to a term deposit?

This project uses the UCI Bank Marketing dataset to explore customer subscription behavior and develop machine learning classification models that estimate the likelihood of a customer subscribing to a term deposit.

The intended business application is to help marketing teams prioritize outreach rather than contact all customers indiscriminately.

**Prediction timing:** The primary model excludes `duration` because call duration is only known after the current call. Including it would introduce target leakage for a pre-call prediction model.

## Dataset and Attribution

- **Source:** [UCI Machine Learning Repository — Bank Marketing, Dataset 222](https://archive.ics.uci.edu/dataset/222/bank+marketing)
- **DOI:** [10.24432/C5K306](https://doi.org/10.24432/C5K306)
- **Authors:** Sérgio Moro, Paulo Rita, and Paulo Cortez (2014)
- **License listed by UCI:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- **Selected file:** `bank-full.csv`
- **Dataset size:** 45,211 rows, 16 input variables, and one target variable (`y`)
- **Original file format:** Semicolon-delimited CSV

The target variable indicates whether a customer subscribed to a term deposit (`yes` or `no`).

The dataset contains 5,289 subscriptions (approximately 11.7% of observations), making this an imbalanced classification problem.

Retain appropriate attribution in reports and adapted materials. Review the UCI dataset page and CC BY 4.0 terms before redistributing dataset copies or derivatives.

## Repository Structure

```text
bank-marketing-prediction/
├── data/
│   └── raw/
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   └── 02_model_development.ipynb
├── src/
│   └── download_data.py
├── .gitignore
├── README.md
└── requirements.txt
```

Raw data is excluded from Git. The dataset can be downloaded using the provided script.

## Setup and Reproduction

Requires Python 3.10 or later.

### 1. Clone the repository

```bash
git clone https://github.com/jontaylor224/bank-marketing-prediction.git
cd bank-marketing-prediction
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the dataset

```bash
python src/download_data.py
```

The downloader retrieves the official UCI archive and extracts `bank-full.csv` into `data/raw/`.

### 5. Run the notebooks

Start Jupyter:

```bash
jupyter lab
```

Run the notebooks in order:

1. `01_exploratory_data_analysis.ipynb`
2. `02_model_development.ipynb`

## Analytical Methodology

### Exploratory Data Analysis

The exploratory analysis examined:

- Dataset structure and data quality.
- Target distribution and class imbalance.
- Customer demographics and financial characteristics.
- Contact methods and campaign timing.
- Previous campaign outcomes and contact history.
- Numerical feature distributions, skewness, and outliers.

Important observations included:

- Only approximately 11.7% of customers subscribed.
- Customers previously contacted by the bank had a higher historical subscription rate than customers with no previous contact.
- Subscription rates varied across contact methods, months, and previous campaign outcomes.
- Several numerical features exhibited substantial skewness.

These are descriptive associations and should not be interpreted as causal relationships.

### Feature Engineering and Prediction Timing

The modeling workflow incorporated several decisions to ensure that the features were appropriate for pre-call prediction:

- Excluded `duration` to prevent target leakage.
- Replaced `campaign` with `contacts_before_current_call`, calculated as `campaign - 1`, to represent contacts made before the current call.
- Converted `pdays` into two features:
  - `previously_contacted`: indicates whether the customer had been contacted previously.
  - `days_since_previous_contact`: represents elapsed days, with the sentinel value `-1` replaced by zero and distinguished using the binary indicator.
- Retained `previous` and `poutcome` to represent prior campaign history.
- Initially preserved `unknown` categorical values as explicit categories rather than treating them as missing values.

### Model Development

The following models were developed:

- Majority-class baseline using `DummyClassifier`.
- Logistic Regression with class weighting and standardized numerical features.
- Random Forest with class weighting and unscaled numerical features.

Preprocessing and classification were combined using scikit-learn pipelines.

The data was divided into stratified training and test sets using an 80/20 split. A separate validation split from the training data was used for threshold selection.

### Evaluation Metrics

Because the target is imbalanced, model performance was evaluated using:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Average Precision (PR-AUC)

Confusion matrices were also examined to understand false positives and false negatives.

## Final Model Results

The Random Forest classifier with a classification threshold of 0.40 was selected as the preferred model based on its validation-set F1 score.

Final performance was measured on the held-out test set.

| Metric | Random Forest (0.40) |
|---|---:|
| Accuracy | 87.00% |
| Precision | 45.05% |
| Recall | 50.76% |
| F1 Score | 47.73% |
| ROC-AUC | 80.28% |
| Average Precision | 45.20% |

### Confusion Matrix

| | Predicted No | Predicted Yes |
|---|---:|---:|
| Actual No | 7,330 | 655 |
| Actual Yes | 521 | 537 |

The model correctly identified 537 of the 1,058 actual subscribers, while missing 521.

Of the 1,192 customers predicted as potential subscribers, 537 actually subscribed.

### Model Comparison

| Model | Threshold | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.50 | 26.71% | 62.38% | 37.40% |
| Logistic Regression | 0.65 | 46.28% | 43.48% | 44.83% |
| Random Forest | 0.50 | 51.55% | 39.22% | 44.55% |
| Random Forest | 0.40 | 45.05% | 50.76% | 47.73% |

The Random Forest at 0.40 provided the strongest balance of precision and recall among the tested configurations.

The threshold was selected using validation data, not the held-out test results. It is the best F1 threshold among the values evaluated, not necessarily the optimal threshold for financial return.

## Feature Importance

Permutation importance was calculated using Average Precision as the scoring metric.

The most influential features were:

1. Month of contact
2. Contact method
3. Outcome of the previous marketing campaign
4. Housing loan status
5. Days since the previous contact

These findings suggest that campaign timing, communication channel, and prior campaign history contain substantial predictive information.

Feature importance identifies predictive associations, not causal effects. Correlated features and historical marketing practices may influence the observed importance values.

## Business Recommendations

Based on the analysis, the bank could consider:

1. Using predicted subscription probabilities to prioritize customers for outreach.
2. Investigating historical differences in subscription rates across contact months.
3. Evaluating the effectiveness of different communication channels.
4. Incorporating previous campaign outcomes when prioritizing follow-up contacts.
5. Testing different classification thresholds based on outreach capacity, acquisition costs, and the expected value of a subscription.

The model should be considered a decision-support tool rather than an automated replacement for marketing judgment.

## Limitations and Future Work

Several limitations should be considered before operational use:

- **Historical data:** Customer behavior and campaign effectiveness may change over time.
- **Class imbalance:** Only approximately 11.7% of customers subscribed, making accuracy alone an inadequate measure of performance.
- **No causal inference:** Predictive relationships do not establish that changing a feature or marketing practice will increase subscriptions.
- **Generalizability:** The analysis uses one historical bank marketing dataset. Results should be validated against newer campaigns and other customer populations.
- **Threshold selection:** F1 does not incorporate actual marketing costs or subscription value. Financially optimized threshold selection would require those inputs.
- **Potential bias:** Customer characteristics should be reviewed for fairness, privacy, and applicable regulatory requirements.
- **Prediction-time assumptions:** The engineered campaign-contact feature assumes `campaign - 1` represents contacts completed before the current call.

Future work could include probability calibration, cost-sensitive threshold optimization, additional model comparisons, and validation on more recent campaign data.

## Conclusion

This project demonstrates an end-to-end classification workflow using the UCI Bank Marketing dataset.

Exploratory data analysis identified patterns in customer characteristics and historical campaign activity. Logistic Regression and Random Forest models were developed, evaluated against a baseline, and compared using metrics appropriate for an imbalanced classification problem.

The Random Forest model with a 0.40 classification threshold achieved the strongest F1 score on the held-out test set among the configurations evaluated.

The findings suggest that historical customer and campaign information can help prioritize potential term-deposit subscribers. Further validation and business-focused evaluation would be necessary before deploying the model in a real marketing environment.
