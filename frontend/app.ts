import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

interface Trade {
  id?: number;
  symbol: string;
  price: number;
  timestamp: Date;
}

const fetchTrades = async () => {
  try {
    const response = await axios.get(`${API_URL}/trades`);
    displayTrades(response.data);
  } catch (error) {
    console.error("Error fetching trades:", error);
  }
};

const createTrade = async (trade: Trade) => {
  try {
    const response = await axios.post(`${API_URL}/trades`, trade);
    console.log('Trade created:', response.data);
    fetchTrades();
  } catch (error) {
    console.error("Error creating trade:", error);
  }
};

const updateTrade = async (id: number, trade: Trade) => {
  try {
    const response = await axios.put(`${API_URL}/trades/${id}`, trade);
    console.log('Trade updated:', response.data);
    fetchTrades();
  } catch (error) {
    console.error("Error updating trade:", error);
  }
};

const deleteTrade = async (id: number) => {
  try {
    await axios.delete(`${API_URL}/trades/${id}`);
    console.log('Trade deleted');
    fetchTrades();
  } catch (error) {
    console.error("Error deleting trade:", error);
  }
};

const displayTrades = (trades: Trade[]) => {
  const tradesElement = document.getElementById('trades');
  if (tradesElement) {
    tradesElement.innerHTML = trades.map(trade => 
      `<div>${trade.symbol} - ${trade.price} - ${new Date(trade.timestamp).toLocaleString()}</div>`
    ).join('');
  }
};

const initFormSubmission = () => {
  const form = document.getElementById('tradeForm') as HTMLFormElement;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const formData = new FormData(form);
    const trade: Trade = {
      symbol: formData.get('symbol') as string,
      price: parseFloat(formData.get('price') as string),
      timestamp: new Date(formData.get('timestamp') as string),
    };
    
    await createTrade(trade);
  });
};

const init = () => {
  fetchTrades();
  initFormSubmission();
};
  
document.addEventListener('DOMContentLoaded', init);