# 🍬 Nassau Candy Factory Optimization System

## 📌 Project Overview
This project builds a **Decision Intelligence System** for Nassau Candy Distributor to improve logistics performance by optimizing factory assignments.

The system uses **Machine Learning + Optimization Logic** to:
- Predict shipping lead time
- Simulate factory reassignment scenarios
- Recommend the best factory for each product

---

## 🎯 Problem Statement
Currently, Nassau Candy assigns products to factories using static rules, leading to:
- High delivery time
- Increased shipping distance
- Reduced profit margins
- No system to test alternative assignments

---

## 🎯 Objective
- Predict delivery lead time using ML
- Optimize factory assignment
- Reduce shipping delays
- Improve operational efficiency

---

## 🧠 Methodology

### 1. Data Preprocessing
- Converted date columns
- Created **Lead Time = Ship Date - Order Date**
- Removed missing values

### 2. Feature Engineering
- Encoded categorical variables:
  - Product
  - Region
  - Ship Mode

### 3. Model Building
- Used **Random Forest Regressor**
- Input features:
  - Product
  - Region
  - Ship Mode
  - Sales
  - Units
- Output:
  - Lead Time (days)

---

## ⚙️ Advanced Logic

### 🚚 Distance-Based Optimization
- Each factory has coordinates
- Distance calculated between factory and region
- Lead time adjusted based on distance

### 💰 Profit Impact
- Profit score estimated using:
  - Sales
  - Distance cost

### 🔁 Scenario Simulation
- Each product is tested across all factories
- System compares performance and ranks best option

---

## 📊 Key Features
- Lead Time Prediction
- Factory Recommendation System
- Profit Impact Analysis
- Interactive Dashboard (Streamlit)
- Graph Visualization

---

## 🖥️ Dashboard Features

### 1. Predict Lead Time
- Select product, region, ship mode
- Get estimated delivery time

### 2. Factory Recommendation
- Shows best factories ranked by:
  - Delivery time
  - Profit score

### 3. KPI Metrics
- Lead Time Reduction (%)
- Efficiency Improvement

### 4. Visualization
- Bar chart of factory vs lead time

---

## 📦 Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib

---

## ▶️ How to Run the Project

### Step 1: Install dependencies
```bash
pip install -r requirements.txt