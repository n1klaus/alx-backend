import { createClient } from 'redis';

const client = createClient();

(async () => {
  client.on('error', (err) => {
    console.error('Redis client not connected to the server: ', err.message);
  });

  client.on('connect', () => {
    console.log('Redis client connected to the server');
  });

  await client.connect();
})();
