# NOAA Fisheries Data Analysis
### Exploring West Coast Groundfish Bottom Trawl Survey (WCGBTS) Data with PostgreSQL and Python

## **Project Overview**
This project processes and analyzes NOAA's **West Coast Groundfish Bottom Trawl Survey (WCGBTS)** dataset. It retrieves, cleans, and loads fisheries data into a **PostgreSQL database**, then performs exploratory data analysis using SQL and Python.

### **Key Features:**
- **Automated Data Retrieval:** Downloads NOAA WCGBTS data via RESTful API, creating a flexible tool that can adapt over time as new data is added to the survey.   
- **Database Integration:** Stores structured data in a **PostgreSQL** database, allowing fast querying, filtering, and structured storage without repeatedly loading large files.   
- **Data Cleaning & Standardization:** Uses `pandas` to preprocess raw data and ensure consistent formats.   
- **SQL-Based Data Analysis:** Executes predefined queries to extract insights, simplifying repetitive analysis by storing queries and allowing the user to run them anytime.   
- **Visualizations:** Generates **trend plots & species distributions** using `matplotlib`.  

## **Project Structure**
```
NOAA_DATA/
│── data/                    # Stores downloaded raw data and generated plots
│── db/                      # Scripts for database queries and analysis
│   ├── fetch_db_data.py     # Retrieves and prints database records
│   ├── analyze_data.py      # Runs analysis & generates visualizations
│── sql/                     # SQL scripts for database setup
│   ├── create_tables.sql    # Defines database schema
│   ├── analysis_queries.sql # Contains reusable SQL queries
│── src/                     # Core database management logic
│   ├── db_manager.py        # Manages database connection & transactions
│── main.py                  # Orchestrates full ETL pipeline
│── .env.example             # Template for setting up environment configuration
│── README.md                # Project documentation
│── requirements.txt         # Dependencies
```

---

## **Setup & Installation**
### **1. Clone the Repository**
```bash
git clone https://github.com/emma-lewis/NOAA_Data.git
cd NOAA_Data
```

### **2. Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up PostgreSQL Database**
Install **PostgreSQL** if it is not already installed and create a database:
```bash
psql postgres
```
In the psql shell:
```sql
CREATE DATABASE noaa_data;
```
Create necessary tables:
```bash
psql -U your_username -d noaa_data -f sql/create_tables.sql
```

### **5. Configure Environment Variables**
Create a **.env** file in the project root by copying the example:
```bash
cp .env.example .env
```
Edit **.env** with your PostgreSQL credentials:
```ini
DB_NAME=noaa_data
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
### **6. Run the Project**
#### **A. Download, Clean, and Insert Data**
```bash
python main.py
```
- This **downloads, cleans, and inserts** data into PostgreSQL.

#### **B. Fetch Data**
```bash
python db/fetch_db_data.py
```
- This returns the **most prevalent species** (those appearing in the most sampling events) and the **most caught species** (those caught in highest total numbers), helping distinguish between widespread presence and local population density.

#### **C. Run Analysis & Generate Visualizations**
```bash
python db/analyze_data.py
```
- This saves visualizations to the data/ folder as:
  -  **data/Total_Catch_Weight.png**
  -  **data/Species_Count.png**.
---

## **Visualizations**
### **Total Catch Weight Over Time**
**What it shows:** Trends in **total fish catch weight per year**.

![Total Catch Weight Over Time](data/Total_Catch_Weight.png)

---

### **Species Count by Year**
**What it shows:** **Number of unique species caught per year**.

![Species Count by Year](data/Species_Count.png)

---

## **Acknowledgments**
This project uses publicly available fisheries data from the **West Coast Groundfish Bottom Trawl Survey** from NOAA's FRAM Data Warehouse.   

**Contact:** emlew21@gmail.com | https://github.com/emma-lewis
