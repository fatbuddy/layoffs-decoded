const base = require('./base.js')

// PEARSON
async function find_all_precovid_pearson(db, limit) {
    var query = "SELECT name, value FROM precovid_pearson limit " + limit
    return await base.find_all(db, query)
}

async function find_all_covid_pearson(db, limit) {
    var query = "SELECT name, value FROM covid_pearson limit " + limit
    return await base.find_all(db, query)
}

async function find_all_postcovid_pearson(db, limit) {
    var query = "SELECT name, value FROM postcovid_pearson limit " + limit
    return await base.find_all(db, query)
}

// SPEARMAN
async function find_all_precovid_spearman(db, limit) {
    var query = "SELECT name, value FROM precovid_spearman limit " + limit
    return await base.find_all(db, query)
}

async function find_all_covid_spearman(db, limit) {
    var query = "SELECT name, value FROM covid_spearman limit " + limit
    return await base.find_all(db, query)
}

async function find_all_postcovid_spearman(db, limit) {
    var query = "SELECT name, value FROM postcovid_spearman limit " + limit
    return await base.find_all(db, query)
}

// LASSO
async function find_all_precovid_lasso(db, limit) {
    var query = "SELECT name, value FROM precovid_lasso limit " + limit
    return await base.find_all(db, query)
}

async function find_all_covid_lasso(db, limit) {
    var query = "SELECT name, value FROM covid_lasso limit " + limit
    return await base.find_all(db, query)
}

async function find_all_postcovid_lasso(db, limit) {
    var query = "SELECT name, value FROM postcovid_lasso limit " + limit
    return await base.find_all(db, query)
}

// RIDGE
async function find_all_precovid_ridge(db, limit) {
    var query = "SELECT name, value FROM precovid_ridge limit " + limit
    return await base.find_all(db, query)
}

async function find_all_covid_ridge(db, limit) {
    var query = "SELECT name, value FROM covid_ridge limit " + limit
    return await base.find_all(db, query)
}

async function find_all_postcovid_ridge(db, limit) {
    var query = "SELECT name, value FROM postcovid_ridge limit " + limit
    return await base.find_all(db, query)
}

// ELASTICNET
async function find_all_precovid_elasticnet(db, limit) {
    var query = "SELECT name, value FROM precovid_elasticnet limit " + limit
    return await base.find_all(db, query)
}

async function find_all_covid_elasticnet(db, limit) {
    var query = "SELECT name, value FROM covid_elasticnet limit " + limit
    return await base.find_all(db, query)
}

async function find_all_postcovid_elasticnet(db, limit) {
    var query = "SELECT name, value FROM postcovid_elasticnet limit " + limit
    return await base.find_all(db, query)
}

// DECISION TREE
async function find_all_precovid_decisiontree(db, limit) {
    var query = "SELECT name, value FROM precovid_decisiontree limit " + limit
    return await base.find_all(db, query)
}

async function find_all_covid_decisiontree(db, limit) {
    var query = "SELECT name, value FROM covid_decisiontree limit " + limit
    return await base.find_all(db, query)
}

async function find_all_postcovid_decisiontree(db, limit) {
    var query = "SELECT name, value FROM postcovid_decisiontree limit " + limit
    return await base.find_all(db, query)
}

// RANDOMFOREST 
async function find_all_precovid_randomforest(db, limit) {
    var query = "SELECT name, value FROM precovid_randomforest limit " + limit
    return await base.find_all(db, query)
}

async function find_all_covid_randomforest(db, limit) {
    var query = "SELECT name, value FROM covid_randomforest limit " + limit
    return await base.find_all(db, query)
}

async function find_all_postcovid_randomforest(db, limit) {
    var query = "SELECT name, value FROM postcovid_randomforest limit " + limit
    return await base.find_all(db, query)
}

module.exports = {
    find_all_precovid_pearson,
    find_all_covid_pearson,
    find_all_postcovid_pearson,
    find_all_precovid_spearman,
    find_all_covid_spearman,
    find_all_postcovid_spearman,
    find_all_precovid_lasso,
    find_all_covid_lasso,
    find_all_postcovid_lasso,
    find_all_precovid_ridge,
    find_all_covid_ridge,
    find_all_postcovid_ridge,
    find_all_precovid_elasticnet,
    find_all_covid_elasticnet,
    find_all_postcovid_elasticnet,
    find_all_precovid_decisiontree,
    find_all_covid_decisiontree,
    find_all_postcovid_decisiontree,
    find_all_precovid_randomforest,
    find_all_covid_randomforest,
    find_all_postcovid_randomforest
  };
