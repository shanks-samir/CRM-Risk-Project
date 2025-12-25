# CRM-Inspired Institutional Risk Engine

## Project Overview
This project mimics a **Risk & Compliance Management (CRM)** system used by Tier-1 banks to manage digital assets. It focuses on meeting **MaRisk** (Minimum Requirements for Risk Management) and **MiCA** (Markets in Crypto-Assets) standards.

Unlike standard crypto trackers, this tool prioritizes **Auditability** and **Regulatory Compliance** over simple price tracking.

## Key Features
* **Multi-Asset Data Pipeline**: Ingests real-time data for Native Assets (BTC/ETH), Delta-1 Certificates (ETFs), and Tokenized Bonds.
* **Monte Carlo VaR Model**: Calculates *Value at Risk* using 10,000 simulations per asset to model tail risks (95% confidence interval).
* **Market Conformity Audit**: A "Fair Market Value" check that flags trades executed outside the daily High/Low range (simulating "Fat Finger" prevention).
* **ESG Compliance Module**: Visualizes consensus mechanism energy intensity (PoW vs. PoS) using a radial polar chart to satisfy environmental disclosure rules.

## Technical Stack
* **Language**: Python 3.10+
* **Database**: SQLite (Relational DB for Audit Logs)
* **Visualization**: Streamlit (Dashboard), Matplotlib (Static Reporting)
* **Financial Math**: NumPy (Monte Carlo Simulations), Pandas (Time-series)

## Project Structure
```text
crm-risk-project/
├── data/               # SQLite Database (Auto-generated)
├── modules/            
│   ├── pipeline.py     # Data Ingestion & ETL
│   ├── risk_math.py    # Monte Carlo VaR Logic
│   └── conformity.py   # Fair Market Value Logic
├── app.py              # Streamlit Dashboard Entry Point
├── requirements.txt    # Dependencies
└── README.md           # Documentation


How to Run
------------

Follow these steps to initialize the environment and launch the engine:

### 1\. Install Dependencies

Ensure you have a virtual environment active, then install the required libraries:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

### 2\. Initialize Data & Run Risk Calculations

Execute the data pipeline module to fetch live market data, run the Monte Carlo simulations, and generate the audit log. Run this command from the root directory:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m modules.pipeline   `

> **Note:** This command creates the data/crm\_risk.db file and populates it with historical market context and mock trades (including simulated errors to test the "FAIL" state).

### 3\. Launch the Audit Dashboard

Start the Streamlit web interface to visualize the risk reports and the conformity audit trail:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   streamlit run app.py   `