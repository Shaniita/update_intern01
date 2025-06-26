const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');

const DB_CONFIG = {
  host: 'xxxxxxxxx',
  user: 'xxxxxxxxx',
  password: 'xxxxxxxxx',
  database: 'xxxxxxxxx'
};

const p_dept_abbr = 'null';
const p_divisi_abbr = 'null';

const today = new Date();
const startDate = new Date(today);
startDate.setDate(today.getDate() - 2);
const endDate = today;

const logFilePath = path.join(__dirname, 'rotasi_log.txt');

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

async function runRotasi() {
  let connection;
  const startTime = Date.now();

  try {
    connection = await mysql.createConnection(DB_CONFIG);

    const procedureQuery = 'CALL generate_rotasi01(?, ?, ?, ?)';
    await connection.execute(procedureQuery, [
      startDate.toISOString().split('T')[0],
      endDate.toISOString().split('T')[0],
      p_dept_abbr,
      p_divisi_abbr
    ]);

    const durationMs = Date.now() - startTime;
    log(`SUKSES generate rotasi dari ${startDate.toISOString().split('T')[0]} sampai ${endDate.toISOString().split('T')[0]} (waktu proses: ${formatDuration(durationMs)})`);
  } catch (err) {
    const durationMs = Date.now() - startTime;
    log(`GAGAL! Error: ${err.message} (waktu proses: ${formatDuration(durationMs)})`);
  } finally {
    if (connection) await connection.end();
  }
}

runRotasi();
