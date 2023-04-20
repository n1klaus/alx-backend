import express from 'express';
import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';

const redisClient = createClient();
let reservationEnabled = true;
const queue = createQueue();
const app = express();
const PORT = 1245;

const getRedis = promisify(redisClient.get).bind(redisClient);

function reserveSeat (number) {
  redisClient.set('available_seats', number);
}

async function getCurrentAvailableSeats () {
  const seats = await getRedis('available_seats');
  return seats;
}

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.status(200).json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat', { seat: 1 })
    .save((error) => {
      if (error) {
        return res.status(404).json({ status: 'Reservation failed' });
      } else {
        res.status(200).json({ status: 'Reservation in process' });
      }
    })
    .on('complete', function () {
      console.log(`Seat reservation job ${job.id} completed`);
    })
    .on('failed', function (error) {
      console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
    });
});

app.get('/process', (req, res) => {
  res.status(200).json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const seat = await getCurrentAvailableSeats();
    if (parseInt(seat) === 0) reservationEnabled = false;
    if (parseInt(seat) > 0) {
      reserveSeat(parseInt(seat) - 1);
    } else {
	    done(Error('Not enough seats available'));
    }
    done();
  });
});

app.listen(PORT, () => {
  console.log(`app is listening http://localhost:${PORT}`);
});

redisClient.on('connect', function () {
  console.log('Redis client connected to the server');
});

redisClient.on('error', function (err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

reserveSeat(50);
