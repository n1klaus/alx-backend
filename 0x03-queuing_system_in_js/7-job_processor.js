import { createQueue, Job } from 'kue';

const queue = createQueue();

function sendNotification (phoneNumber, message, job, done) {
  job.progress(0, 100);
  if (phoneNumber in ['4153518780', '4153518781']) {
    done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    return;
  }
  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  done();
}

queue.process('push_notification_code_2', 2, function (job, done) {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
