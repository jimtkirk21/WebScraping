Largest Banks ETL Project
Description
This project implements an Extract, Transform, Load (ETL) pipeline to collect data on the world's largest banks from a Wikipedia page. It extracts bank names and their assets in USD, transforms these assets into GBP, EUR, and INR using a provided exchange rate file, and then loads the processed data into both a CSV file and a SQLite database. This solution is designed to provide structured economic data for analysis and demonstrates key data engineering practices.

Features
Web Scraping: Extracts bank names and assets from the "List of largest banks" Wikipedia page.

Data Transformation: Converts asset values from USD to GBP, EUR, and INR based on an external exchange rate CSV.

Data Persistence: Saves the transformed data into a CSV file (Largest_banks_data.csv) and a SQLite database (Largest_Banks.db).

Database Querying: Executes predefined SQL queries on the loaded database to demonstrate data accessibility.

Execution Logging: Records timestamps and messages for each stage of the ETL process in a log file (stage_log.txt).

Technologies Used
Python 3.x

requests: For making HTTP requests to fetch web page content.

BeautifulSoup4 (bs4): For parsing HTML and extracting data.

pandas: For efficient data manipulation and analysis using DataFrames.

numpy: For numerical operations, specifically rounding.

sqlite3: For connecting to and managing the SQLite database.

datetime: For generating timestamps for log entries.

Setup & Installation
To set up and run this project locally, follow these steps:

Clone the repository:

git clone https://github.com/your-username/largest-banks-etl.git
cd largest-banks-etl

(Replace your-username with your actual GitHub username)

Create a virtual environment (recommended):

python3.11 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required Python libraries:

python3.11 -m pip install -r requirements.txt

Download the exchange rate CSV file:
This project requires an exchange_rate.csv file. Download it into the project's root directory:

wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv

(If wget is not available on your system, you can manually download the file from the URL provided and place it in the project directory.)

Usage
To run the ETL pipeline:

Execute the main Python script:

python etl_banks.py

Output Files:

Largest_banks_data.csv: A CSV file containing the extracted and transformed bank data.

Largest_Banks.db: A SQLite database file containing the Largest_banks table.

stage_log.txt: A log file detailing the execution progress.

Console Output:
The script will print the extracted, transformed dataframes, and the results of several SQL queries (all contents, average assets per currency, and top 5 bank names) to the console. It will also print the content of the stage_log.txt file at the end.

Project Structure
largest-banks-etl/
├── etl_banks.py
├── requirements.txt
├── README.md
├── exchange_rate.csv  (downloaded separately)
├── .gitignore
└── (output files: Largest_banks_data.csv, Largest_Banks.db, stage_log.txt)

Supporting Files
etl_banks.py
This is the main Python script that orchestrates the ETL process, containing functions for data extraction, transformation, loading, and logging.

requirements.txt
This file lists all the Python dependencies required for the project.

requests==2.32.3
beautifulsoup4==4.12.3
pandas==2.2.2
numpy==1.26.4

(Note: These versions are provided as a common baseline. It's recommended to use the exact versions you developed with for full compatibility.)

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.