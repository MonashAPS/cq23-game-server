const ftp = require("basic-ftp")

async function upload() {
  const client = new ftp.Client();
  client.ftp.verbose = true;
  try {
    await client.access({
      host: process.argv[2],
      user: process.argv[3],
      password: process.argv[4],
      port: 21,
      secure: true,
      secureOptions: {
        rejectUnauthorized: false,
      },
    });
    await client.ensureDir(process.argv[5]);
    await client.uploadFromDir(process.argv[6]);
  } catch (err) {
    console.log(err);
  }
  client.close();
}

upload();
