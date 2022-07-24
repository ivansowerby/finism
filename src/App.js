import { useEffect, useState, useMemo } from "react";
import Chart from "react-apexcharts";
import './App.css';

// const proxyUrl = "https://cors-anywhere.herokuapp.com/"; // because of cors header problem
// const stocksUrl = `${proxyUrl}https://yahoo-finance-api.vercel.app/AAPL`;
const stocksUrl = 'https://yahoo-finance-api.vercel.app/AAPL';

async function getStocks(){
  const response = await fetch(stocksUrl);
  return response.json();
}

const round = (number) => {
  return number ? +(number.toFixed(2)) : null;
};

const directionEmojis = {
  up: "🚀",
  down: "💩",
  "": ""
}

const chart = {
  series: [{
    data: []
  }],
  options: {
    chart: {
      type: 'candlestick',
      height: 350
    },
    title: {
      text: 'CandleStick Chart',
      align: 'left'
    },
    xaxis: {
      type: 'datetime'
    },
    yaxis: {
      tooltip: {
        enabled: true
      }
    }
  },
};

// {
//   x: new Date(1538821800000),
//   y: [6625.95, 6626, 6611.66, 6617.58]
// },

function App() {
  const [price, setPrice] = useState(-1);
  const [prevPrice, setPrevPrice] = useState(-1);
  const [priceTime, setPriceTime] = useState(null);
  const [series, setSeries] = useState([{
    data: []
  }]);

  useEffect(() => {
    let timeoutid;
    async function getLatestPrice(){
      try{
        const data = await getStocks()
        console.log(data);
        const aapl = data.chart.result[0];
        setPrevPrice(price);
        setPrice(aapl.meta.regularMarketPrice.toFixed(2));
        setPriceTime(new Date(aapl.meta.regularMarketTime * 1000))
        const quote = aapl.indicators.quote[0];
        const prices = aapl.timestamp.map((timestamp, index) => ({
          x: new Date(timestamp * 1000),
          y: [quote.open[index], quote.high[index], quote.low[index], quote.close[index]].map(round)
        }));
        setSeries([{
          data: prices
        }]);
      }catch(error){
        timeoutid = setTimeout(getLatestPrice, 5000 * 2);
      }
    }
    getLatestPrice();
    return () => {
      clearTimeout(timeoutid);
    }
  }, [])

  const direction = useMemo(() => prevPrice < price ? "up" : prevPrice > price ? "down" : "", [prevPrice, price])

  return (
    <div>
      <div className="ticker">
        AAPL
      </div>
      <div className={["price", direction].join(" ")}>
        ${price} {directionEmojis[direction]}
      </div>
      <div className="price-time">
        {priceTime && priceTime.toLocaleTimeString()}
      </div>
      <Chart options={chart.options} series={series} type="candlestick" width="100%" height={320} />
    </div>
  );
}

export default App;
