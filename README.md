# Quant Research

Systematic research environment for financial modeling and backtesting.

## Structure

- `src/` → core modules (data, indicators, strategies)  
- `notebooks/` → exploratory research  
- `tests/` → validation and unit tests  

## Setup

Clone the repository:  
```bash
git clone https://github.com/yourusername/Quant_research.git
cd Quant_research
```
Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate    # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Install the project in editable mode:
```bash
pip install -e .
```

## Usage

```bash
from src.data_manager import DataManager

dm = DataManager("SPY", period="1y")
dm.add_sma(20)
dm.add_sma(50)
dm.plot()
```

## Roadmap
- Data pipeline
- Indicator library
- Strategy engine
- Backtesting framework