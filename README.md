# 🛒 Retail Sales & Customer Segmentation (RFM Analysis)

**Tools:** Python · SQL · Power BI
**Domain:** E-Commerce / Retail Analytics
**Level:** Intermediate

---

## 📌 Project Overview

Segments 1,000 e-commerce customers using the **RFM model** (Recency, Frequency, Monetary) — one of the most widely used customer analytics frameworks in retail and CRM.

The project covers:
- Generating realistic order data across 8 product categories
- Computing RFM scores in Python (no external libraries)
- Segmenting customers into 6 strategic groups
- SQL queries for category, channel, and trend analysis
- Power BI dashboard for marketing and CRM teams

---

## 📁 Repository Structure

```
3_retail_segmentation/
│
├── data/
│   ├── customers.csv        # 1,000 customers (country, channel, join date)
│   ├── orders.csv           # 4,778 orders across 8 categories
│   ├── rfm_segments.csv     # RFM scores + segment per customer (output)
│   └── segment_summary.csv  # Aggregated segment statistics (output)
│
├── python/
│   ├── generate_data.py     # Dataset generator
│   └── rfm_segmentation.py  # RFM scoring + segmentation engine
│
├── sql/
│   └── analysis_queries.sql # 8 analytical queries
│
└── README.md
```

---

## 🧠 RFM Framework

| Metric    | Definition                          | Scoring |
|----------|-------------------------------------|---------|
| Recency  | Days since last purchase            | 1–5 (5 = most recent) |
| Frequency| Number of orders                    | 1–5 (5 = most orders) |
| Monetary | Total spend (€)                     | 1–5 (5 = highest spend) |

### Customer Segments

| Segment            | Behaviour                                      | Action              |
|-------------------|------------------------------------------------|---------------------|
| 🏆 Champions       | Bought recently, buy often, spend most         | Reward them         |
| 💛 Loyal Customers | Buy regularly, good spend                      | Upsell & reward     |
| 🌱 Potential Loyalist | Recent buyers, average frequency            | Build loyalty       |
| 😴 Hibernating     | Below average recency, frequency, spend        | Win-back campaign   |
| ⚠️ At Risk         | Past champions, haven't bought recently        | Reactivate urgently |
| 💀 Lost            | Lowest recency and frequency scores            | Low-cost re-engage  |

---

## 📊 Key Results

| Segment            | Customers | Revenue (€)  |
|-------------------|-----------|--------------|
| Potential Loyalist | 505       | 232,080      |
| Loyal Customers    | 150       | 149,197      |
| Champions          | 36        | 47,607       |
| Hibernating        | 120       | 42,766       |
| Lost               | 171       | 37,977       |

---

## 🚀 How to Run

```bash
# Step 1 – Generate data
python python/generate_data.py

# Step 2 – Run RFM segmentation
python python/rfm_segmentation.py

# Step 3 – Load CSVs into Power BI
# Step 4 – Run SQL queries for deeper analysis
```

---

*Built as part of a Data & BI Analyst portfolio targeting the German job market.*
