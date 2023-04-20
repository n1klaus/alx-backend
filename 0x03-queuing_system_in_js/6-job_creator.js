import { createQueue } from 'kue';

const queue = createQueue();

const jobNotification = {
  phoneNumber: '12345678',
  message: 'OTP verification code'
};

const job = queue.create('push_notification_code', jobNotification)
  .save((error) => {
    if (error) throw err;
    console.log(`Notification job created: ${job.id}`);
  });

job
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed', () => {
    console.log('Notification job failed');
  });
