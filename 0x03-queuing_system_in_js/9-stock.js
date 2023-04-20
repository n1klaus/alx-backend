import { createClient } from 'redis';
import express from 'express';
import { promisify } from 'util';

const app = express();
const client = createClient();
const PORT = 1245;

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

const get = promisify(client.get).bind(client);

function getItemById (id) {
  return listProducts.filter((item) => item.itemId === id)[0];
}

function reserveStockById (itemId, stock) {
  client.set(itemId, stock);
}

async function getCurrentReservedStockById (itemId) {
  const stock = await get(itemId);
  return stock;
}

app.get('/list_products', (req, res) => {
  res.status(200).json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  if (item) {
    const stock = await getCurrentReservedStockById(itemId);
    const resultItem = {
      itemId: item.itemId,
      itemName: item.itemName,
      price: item.price,
      initialAvailableQuantity: item.initialAvailableQuantity,
      currentQuantity: stock ? parseInt(stock) : item.initialAvailableQuantity
    };
    res.status(200).json(resultItem);
  } else {
    res.status(404).json({ status: 'Product not found' });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  if (!itemId) return res.status(404).json({ status: 'Product not found' });
  const item = getItemById(parseInt(itemId));
  if (!item) return res.status(404).json({ status: 'Product not found' });
  let currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock) {
    currentStock = parseInt(currentStock);
    if (currentStock > 0) {
      reserveStockById(itemId, currentStock - 1);
      res.status(200).json({ status: 'Reservation confirmed', itemId: itemId });
    } else {
      res.status(200).json({ status: 'Not enough stock available', itemId: itemId });
    }
  } else {
    reserveStockById(itemId, item.initialAvailableQuantity - 1);
    res.status(200).json({ status: 'Reservation confirmed', itemId: itemId });
  }
});

app.listen(PORT, () => {
  console.log(`app listening at http://localhost:${PORT}`);
});

client.on('connect', function () {
  console.log('Redis client connected to the server');
});

client.on('error', function (err) {
  console.log(`Redis client not connected to the server: ${err}`);
});
