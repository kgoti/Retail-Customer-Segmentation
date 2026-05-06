"""
RFM Customer Segmentation Analysis
Recency · Frequency · Monetary

Segments customers into 8 strategic groups:
Champions, Loyal, Potential Loyalist, New Customer,
At Risk, Can't Lose Them, Lost, Hibernating
"""

import csv, os
from datetime import datetime
from collections import defaultdict

BASE = "/home/claude/projects/3_retail_segmentation"
analysis_date = datetime(2024, 1, 1)

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, headers):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)
    print(f"  ✓  {os.path.basename(path)} → {len(rows)} rows")

# ── Load data ────────────────────────────────────────────────────────────────
orders    = read_csv(os.path.join(BASE, "data/orders.csv"))
customers = read_csv(os.path.join(BASE, "data/customers.csv"))

# Filter delivered orders only
orders = [o for o in orders if o["status"] == "Delivered"]

# ── Compute RFM per customer ─────────────────────────────────────────────────
cust_data = defaultdict(lambda: {"dates": [], "total": 0.0, "orders": 0})
for o in orders:
    cid  = o["customer_id"]
    date = datetime.strptime(o["order_date"], "%Y-%m-%d")
    cust_data[cid]["dates"].append(date)
    cust_data[cid]["total"]  += float(o["total_amount"])
    cust_data[cid]["orders"] += 1

rfm_raw = []
for cid, d in cust_data.items():
    last_order = max(d["dates"])
    recency    = (analysis_date - last_order).days
    frequency  = d["orders"]
    monetary   = round(d["total"], 2)
    rfm_raw.append({"customer_id": cid, "recency": recency, "frequency": frequency, "monetary": monetary})

# ── Score R, F, M on 1–5 scale ───────────────────────────────────────────────
def score_quintile(values, reverse=False):
    sorted_vals = sorted(set(values), reverse=reverse)
    n = len(sorted_vals)
    scores = {}
    for i, v in enumerate(sorted_vals):
        scores[v] = max(1, min(5, int((i / n) * 5) + 1))
    return scores

recency_vals  = [r["recency"]   for r in rfm_raw]
freq_vals     = [r["frequency"] for r in rfm_raw]
monetary_vals = [r["monetary"]  for r in rfm_raw]

r_scores = score_quintile(recency_vals,  reverse=True)  # lower recency = better
f_scores = score_quintile(freq_vals,     reverse=False)
m_scores = score_quintile(monetary_vals, reverse=False)

# ── Assign segments ──────────────────────────────────────────────────────────
def assign_segment(r, f, m):
    rfm_score = r + f + m
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 3:
        return "Loyal Customers"
    elif r >= 4 and f <= 2:
        return "Potential Loyalist"
    elif r >= 4 and f == 1:
        return "New Customers"
    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"
    elif r <= 2 and f >= 4 and m >= 4:
        return "Can't Lose Them"
    elif r <= 2 and f <= 2:
        return "Lost"
    else:
        return "Hibernating"

rfm_results = []
for r in rfm_raw:
    rs = r_scores.get(r["recency"],   3)
    fs = f_scores.get(r["frequency"], 3)
    ms = m_scores.get(r["monetary"],  3)
    seg = assign_segment(rs, fs, ms)
    rfm_results.append({
        "customer_id":   r["customer_id"],
        "recency_days":  r["recency"],
        "frequency":     r["frequency"],
        "monetary":      r["monetary"],
        "r_score":       rs,
        "f_score":       fs,
        "m_score":       ms,
        "rfm_score":     rs + fs + ms,
        "segment":       seg
    })

write_csv(
    os.path.join(BASE, "data/rfm_segments.csv"),
    rfm_results,
    ["customer_id","recency_days","frequency","monetary","r_score","f_score","m_score","rfm_score","segment"]
)

# ── Segment Summary ───────────────────────────────────────────────────────────
seg_summary = defaultdict(lambda: {"count": 0, "total_revenue": 0.0, "avg_recency": 0, "avg_frequency": 0})
for r in rfm_results:
    s = r["segment"]
    seg_summary[s]["count"]         += 1
    seg_summary[s]["total_revenue"] += r["monetary"]
    seg_summary[s]["avg_recency"]   += r["recency_days"]
    seg_summary[s]["avg_frequency"] += r["frequency"]

summary_rows = []
for seg, v in seg_summary.items():
    n = v["count"]
    summary_rows.append({
        "segment":         seg,
        "customer_count":  n,
        "total_revenue":   round(v["total_revenue"], 2),
        "avg_revenue":     round(v["total_revenue"] / n, 2),
        "avg_recency_days":round(v["avg_recency"] / n, 1),
        "avg_frequency":   round(v["avg_frequency"] / n, 1)
    })
summary_rows.sort(key=lambda x: -x["total_revenue"])

write_csv(
    os.path.join(BASE, "data/segment_summary.csv"),
    summary_rows,
    ["segment","customer_count","total_revenue","avg_revenue","avg_recency_days","avg_frequency"]
)

print("\n=== SEGMENT DISTRIBUTION ===")
for s in summary_rows:
    print(f"  {s['segment']:<22} {s['customer_count']:>4} customers  |  €{s['total_revenue']:>12,.2f} revenue  |  Avg {s['avg_recency_days']} days since last order")
