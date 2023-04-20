function createPushNotificationsJobs (jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw Error('Jobs is not an array');
  }

  jobs.forEach((newJob) => {
    const job = queue.create('push_notification_code_3', newJob)
      .save((error) => {
        if (error) throw err;
        console.log(`Notification job created: ${job.id}`);
      })
      .on('complete', () => {
        console.log(`Notification job ${job.id} completed`);
      })
      .on('failed', (error) => {
        console.log(`Notification job ${job.id} failed: ${error}`);
      })
      .on('progress', (progress, data) => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      });
  });
}

module.exports = createPushNotificationsJobs;
