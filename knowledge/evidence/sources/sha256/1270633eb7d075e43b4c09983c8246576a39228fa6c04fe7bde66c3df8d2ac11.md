**This High-Level Design (HLD) document outlines an anomaly detection system for DevOps metrics (CPU, memory, request traffic) using Isolation Forest.**

# ** Executive Summary**

- Objective: To detect operational incidents (infrastructure stress, DDoS attacks, memory leaks) in real-time by identifying anomalies in system metrics.
- Core ML Algorithm: Isolation Forest (via scikit-learn). It is chosen for its efficiency with high-dimensional data and unsupervised nature (no need for labeled "failure" data).
- Key Challenge: Adapting a non-temporal algorithm (Isolation Forest) to time-series data (DevOps metrics).

# ** System Architecture**

**The system follows a Batch Training / Real-time Inference architecture. ****IsolationForest**** does not support incremental learning (****partial_fit****), so we train on historical windows and infer on live streams.**

**High-Level Data Flow**

1. Metric Collection: Agents (e.g., Prometheus, Telegraf) scrape metrics.
2. Ingestion Layer: Metrics are buffered in a stream (e.g., Kafka) for real-time access and dumped to a Data Lake (e.g., S3/InfluxDB) for training.
3. Inference Service: Consumes live metrics, applies feature transformation, and queries the current model for an anomaly score.
4. Training Service: Periodically (e.g., daily) retrains models on the last $N$ days of data to account for drift.
5. Alerting: If anomaly_score < threshold, an alert is pushed to PagerDuty/Slack.

# ** Detailed Component Design**

## **Data Ingestion & Preprocessing (The "Time-Series" Adaptation)**

**Isolation Forest treats every data point as independent. To detect *temporal* anomalies (e.g., a spike is normal at 9 AM but abnormal at 3 AM), we must engineer features that give the model context.**

- Raw Metrics: cpu_usage_percent, requests_per_second.
- Feature Engineering (The "Secret Sauce"):

Instead of feeding just the raw value $x_t$, we feed a vector of features:

- - Differencing: $\Delta = x_t - x_{t-1}$ (Captures the *rate* of change, essential for detecting sudden spikes).

## **Model Training (Offline/Batch)**

- Frequency: Daily or Weekly.
- Data Window: Last 7–14 days (long enough to capture weekly seasonality).
- Algorithm: sklearn.ensemble.IsolationForest
- Key Hyperparameters: - contamination: The expected % of anomalies (e.g., 0.01). *Crucial to tune to avoid alert fatigue.* - n_estimators: 100 (default is usually sufficient). - max_samples: 256 (keeps the trees distinct and reduces overfitting).
- Output: A serialized model file (e.g., cpu_model_v1.joblib) pushed to a Model Registry (e.g., S3, MLflow).

## **Inference Service (Online)**

- Input: Live stream of metrics.
- State: The service must maintain a small state (sliding window) of recent metrics to calculate "Rolling Statistics" and "Lag Features" for the incoming data point.
- Logic:

```
Python

# 1. Receive new metric x_t
# 2. Retrieve last k metrics from memory cache (Redis or local)
# 3. Compute features (rolling_mean, hour_sin, etc.)
# 4. score = model.decision_function(features)
# 5. If score < threshold: trigger_alert()
```

# **Handling Specific DevOps Scenarios**

| **Scenario** | **Feature Strategy** | **Why?** |
| --- | --- | --- |
| **Sudden Spike (CPU)** | **Differencing ($x_t - x_{t-1}$)** | **Isolation Forest will easily isolate a point where the "rate of change" is vastly different from the cluster of normal rates.** |
| **Slow Memory Leak** | **Trend / Rolling Mean** | **A slow creep won't be anomalous in $x_t - x_{t-1}$, but the ****rolling_mean**** over 1 hour will eventually drift into an isolated region.** |
| **Traffic Drop (Outage)** | **Seasonality (Hour/Day)** | **0 requests is normal at 3 AM but anomalous at 10 AM. The ****hour_sin**** / ****hour_cos**** features force the tree to split based on time, isolating "low traffic + busy hour" into its own leaf.** |

# **Operational Considerations**

## **Scalability (The "Thousands of Metrics" Problem)**

**You cannot train one giant model for all 5,000 servers.**

- Strategy: Clustering/Grouping.

## **Feedback Loop (Human-in-the-loop)**

**ML models generate false positives.**

1. Alert includes buttons: [Acknowledge] and [False Alarm].
2. If [False Alarm] is clicked, save that data point.
3. Retraining: In the next training batch, explicitly weight these "False Alarm" points as *normal* or adjust the contamination parameter if too many alerts are generated.

# ** Evaluation Metrics**

**Since you rarely have labeled "anomaly" data initially, you cannot easily use Accuracy/Recall.**

- Proxy Metric: Reduction in Alert Volume. Compare the ML alerts vs. static threshold alerts (e.g., "CPU > 80%"). The ML model should remain silent during "expected" high load (e.g., backups) and alert only on unexpected behavior.
- SRE Feedback: Track "Actionable Alert Rate" (Percentage of alerts that led to a fix).