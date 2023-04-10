const base = require('./base.js')

// PEARSON
async function find_model_metrics(db, limit) {
    var query = "SELECT * FROM q2_metrics_1 limit " + limit
    return await base.find_all(db, query)
}

module.exports = {
    find_model_metrics
};
