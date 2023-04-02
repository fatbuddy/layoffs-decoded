const express = require('express')
var config = require("./config.js");
const mysql = require("mysql2");
const fs = require("fs");
const https = require("https");
const app = express()
const port = 3000

const pool = mysql.createPool({
  host: config.MYSQL.HOST,
  user: config.MYSQL.USER,
  password: config.MYSQL.PASSWORD,
  database: config.MYSQL.DATABASE,
  waitForConnections: true,
});

//load model
const title = require("./models/title");
const department = require("./models/department");

app.use(express.json());

app.get("/titles", (req, res) => {
  title.findAll(pool, req.query.includeUnknown, req.query.limit, (err, result) => {
    if (err) {
      res.send({ success: false, payload: err });
    } else {
      res.send({ success: true, payload: result });
    }
  });
});

app.get("/departments", (req, res) => {
  department.findAll(pool, req.query.includeOthers, req.query.limit, (err, result) => {
    if (err) {
      res.send({ success: false, payload: err });
    } else {
      res.send({ success: true, payload: result });
    }
  });
});


if (config.SSL.ENABLED) {
  var privateKey = fs.readFileSync(config.SSL.KEYPATH);
  var certificate = fs.readFileSync(config.SSL.CERTPATH);
  https
    .createServer(
      {
        key: privateKey,
        cert: certificate,
      },
      app
    )
    .listen(443);
} else {
  app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
  })
}
