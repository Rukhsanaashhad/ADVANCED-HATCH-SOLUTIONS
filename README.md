# ADVANCED-HATCH-SOLUTIONS – Monthly Expense Manager  

**A Complete Expense Management System**  
Built with **Python + Streamlit** – specially designed for Jadeed Hatchery Karachi  

Live Demo: [Click Here](https://advanced-hatch-solutions.streamlit.app/)

## Features

- User Signup & Login (har employee ka alag account)  
- Multiple Months Support (April 2020, May 2025 – jitne chahe banao)  
- Zero se Start – koi default amount nahi, tum khud daalo  
- Live Auto Update – amount change karo, total turant update  
- Auto Save + Manual "SAVE" button with balloons  
- Add New Month anytime  
- Export Any Month to Excel (.xlsx) with one click  
- Clean, expandable UI (main heading → sub heading style)  
- Mobile + Desktop friendly  
- Data stored locally (json file) – no database needed  

## Tech Stack

- Python  
- Streamlit (Frontend + Backend)  
- Pandas & OpenPyXL (Excel export)  
- JSON-based persistent storage  

## How to Run Locally

```bash
# 1. Clone repo
git clone https://github.com/tuusername/jadeed-expense-manager.git
cd jadeed-expense-manager

# 2. Install requirements
pip install streamlit pandas openpyxl

# 3. Run the app
streamlit run app.py
