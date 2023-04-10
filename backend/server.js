const express = require('express')
var config = require("./config.js");
const fs = require("fs");
const https = require("https");
const app = express()
const port = 4000

const DB_NAME = "layoffs_decoded_result";

//load model
const q1 = require("./models/q1.js");
const q2 = require("./models/q2.js");
const q3 = require("./models/q3.js");

app.use(express.json());

//Q1
//BINS
app.get("/q1_bin_layoffs", async (req, res) => {
  const result = await q1.find_all_bin_layoffs(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//PEARSON
app.get("/q1_precovid_pearson", async (req, res) => {
  const result = await q1.find_all_precovid_pearson(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_pearson", async (req, res) => {
  const result = await q1.find_all_covid_pearson(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_pearson", async (req, res) => {
  const result = await q1.find_all_postcovid_pearson(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//SPEARMAN
app.get("/q1_precovid_spearman", async (req, res) => {
  const result = await q1.find_all_precovid_spearman(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_spearman", async (req, res) => {
  const result = await q1.find_all_covid_spearman(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_spearman", async (req, res) => {
  const result = await q1.find_all_postcovid_spearman(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//lasso
app.get("/q1_precovid_lasso", async (req, res) => {
  const result = await q1.find_all_precovid_lasso(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_lasso", async (req, res) => {
  const result = await q1.find_all_covid_lasso(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_lasso", async (req, res) => {
  const result = await q1.find_all_postcovid_lasso(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//ridge
app.get("/q1_precovid_ridge", async (req, res) => {
  const result = await q1.find_all_precovid_ridge(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_ridge", async (req, res) => {
  const result = await q1.find_all_covid_ridge(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_ridge", async (req, res) => {
  const result = await q1.find_all_postcovid_ridge(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//elasticnet
app.get("/q1_precovid_elasticnet", async (req, res) => {
  const result = await q1.find_all_precovid_elasticnet(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_elasticnet", async (req, res) => {
  const result = await q1.find_all_covid_elasticnet(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_elasticnet", async (req, res) => {
  const result = await q1.find_all_postcovid_elasticnet(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//decisiontree
app.get("/q1_precovid_decisiontree", async (req, res) => {
  const result = await q1.find_all_precovid_decisiontree(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_decisiontree", async (req, res) => {
  const result = await q1.find_all_covid_decisiontree(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_decisiontree", async (req, res) => {
  const result = await q1.find_all_postcovid_decisiontree(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//randomforest
app.get("/q1_precovid_randomforest", async (req, res) => {
  const result = await q1.find_all_precovid_randomforest(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_randomforest", async (req, res) => {
  const result = await q1.find_all_covid_randomforest(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_randomforest", async (req, res) => {
  const result = await q1.find_all_postcovid_randomforest(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//forward-elimination
app.get("/q1_precovid_forward_elimination", async (req, res) => {
  const result = await q1.find_all_precovid_forward_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_forward_elimination", async (req, res) => {
  const result = await q1.find_all_covid_forward_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_forward_elimination", async (req, res) => {
  const result = await q1.find_all_postcovid_forward_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//stepwise-elimination
app.get("/q1_precovid_stepwise_elimination", async (req, res) => {
  const result = await q1.find_all_precovid_stepwise_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_stepwise_elimination", async (req, res) => {
  const result = await q1.find_all_covid_stepwise_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_stepwise_elimination", async (req, res) => {
  const result = await q1.find_all_postcovid_stepwise_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q1
//backward-elimination
app.get("/q1_precovid_backward_elimination", async (req, res) => {
  const result = await q1.find_all_precovid_backward_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_covid_backward_elimination", async (req, res) => {
  const result = await q1.find_all_covid_backward_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q1_postcovid_backward_elimination", async (req, res) => {
  const result = await q1.find_all_postcovid_backward_elimination(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q2
app.get("/q2_model_metrics", async (req, res) => {
  const result = await q2.find_model_metrics(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

//Q3
app.get("/q3_titles", async (req, res) => {
  const result = await q3.find_all_titles(DB_NAME, req.query.includeUnknown, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q3_departments", async (req, res) => {
  const result = await q3.find_all_departments(DB_NAME, req.query.includeOthers, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
});

app.get("/q3_locations", async (req, res) => {
  const result = await q3.find_all_locations(DB_NAME, req.query.limit);
  res.header("Access-Control-Allow-Origin","*")
  res.send(result);
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
