from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

pairs_data = [
    {"id": "EURUSD", "pair": "EUR/USD"},
    {"id": "USDJPY", "pair": "USD/JPY"},
    {"id": "GBPUSD", "pair": "GBP/USD"},
    {"id": "USDCHF", "pair": "USD/CHF"},
    {"id": "AUDUSD", "pair": "AUD/USD"},
    {"id": "USDCAD", "pair": "USD/CAD"},
    {"id": "NZDUSD", "pair": "NZD/USD"},
    {"id": "EURGBP", "pair": "EUR/GBP"},
    {"id": "EURJPY", "pair": "EUR/JPY"},
    {"id": "GBPJPY", "pair": "GBP/JPY"},
    {"id": "AUDJPY", "pair": "AUD/JPY"},
    {"id": "CADJPY", "pair": "CAD/JPY"},
    {"id": "NZDJPY", "pair": "NZD/JPY"},
    {"id": "EURCHF", "pair": "EUR/CHF"},
    {"id": "GBPCHF", "pair": "GBP/CHF"},
    {"id": "AUDCHF", "pair": "AUD/CHF"},
    {"id": "CADCHF", "pair": "CAD/CHF"},
    {"id": "NZDCHF", "pair": "NZD/CHF"},
    {"id": "EURAUD", "pair": "EUR/AUD"},
    {"id": "GBPAUD", "pair": "GBP/AUD"},
    {"id": "AUDCAD", "pair": "AUD/CAD"},
    {"id": "EURNZD", "pair": "EUR/NZD"},
    {"id": "GBPNZD", "pair": "GBP/NZD"},
    {"id": "AUDNZD", "pair": "AUD/NZD"},
]

currencies_data = [
    {"id": "EUR", "currency": "EUR", "description": "Euro"},
    {"id": "USD", "currency": "USD", "description": "US Dollar"},
    {"id": "JPY", "currency": "JPY", "description": "Japanese Yen"},
    {"id": "GBP", "currency": "GBP", "description": "British Pound Sterling"},
    {"id": "CHF", "currency": "CHF", "description": "Swiss Franc"},
    {"id": "AUD", "currency": "AUD", "description": "Australian Dollar"},
    {"id": "CAD", "currency": "CAD", "description": "Canadian Dollar"},
    {"id": "NZD", "currency": "NZD", "description": "New Zealand Dollar"},
]


# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
class Pair(BaseModel):
    id: str
    pair: str

class Currency(BaseModel):
    id: str
    currency: str
    description : str

class InputData(BaseModel):
    balance : float
    risk_size: float
    stop_loss_pips: int
    transaction_size: float

@app.get('/pairs', response_model=list[Pair])
async def get_pairs() -> list[Pair]:
    return pairs_data

@app.get('/currencies', response_model=list[Currency])
def get_currencies() -> list[Currency]:
    return currencies_data

@app.post('/lot-size-calculator')
def submit_form(data: InputData):
    try:
        print("Received data:", data)  # Debugging: Print received data
        amount_risked = data.balance * data.risk_size / 100
        lot_size = amount_risked / (data.stop_loss_pips * data.transaction_size)
        result = {'amount_risked': round(amount_risked, 2), 
                  'lot_size': round(lot_size, 2)}
        print("Result:", result)  # Debugging: Print calculated result
        return result
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    except Exception as e:
        print("Error:", e)  # Debugging: Print any caught exceptions
        raise HTTPException(status_code=500, detail=str(e))
