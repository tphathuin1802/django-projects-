const ccxt = require("ccxt");

async function main() {
  const binance = new ccxt.binance();
  const price = await binance.fetchOHLCV("BTC/USDT", "1m");
  console.log(price);
}
main();

// O: Open: gia mo san
// H: High
