const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');
const schedule = require('node-schedule');

const DB_CONFIG = {
  host: 'xxxxxxxxx',
  user: 'xxxxxxxxx',
  password: 'xxxxxxxxx',
  database: 'xxxxxxxxx'
};

const logFilePath = path.join(__dirname, 'restan_log.txt');

function log(message) {
  const timestamp = new Date().toISOString();
  fs.appendFileSync(logFilePath, `${timestamp}: ${message}\n`);
}

function formatDuration(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes} menit ${seconds} detik`;
}

async function updateRestan() {
  let connection;
  const startTime = Date.now();

  try {
    connection = await mysql.createConnection(DB_CONFIG);

    await connection.execute('CALL updateRestan01(NULL, NULL);');

    const durationMs = Date.now() - startTime;
    log(`SUKSES menjalankan prosedur updateRestan01 (waktu proses: ${formatDuration(durationMs)})`);
  } catch (err) {
    const durationMs = Date.now() - startTime;
    log(`GAGAL! Error: ${err.message} (waktu proses: ${formatDuration(durationMs)})`);
  } finally {
    if (connection) await connection.end();
  }
}

schedule.scheduleJob('*/10 * * * *', updateRestan);

updateRestan();
