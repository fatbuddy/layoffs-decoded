const base = require('./base.js')

async function find_all_titles(db, includeUnknown, limit = 100) {
    var query = "SELECT name, value FROM q3_titles_counts where name <> 'Unknown' limit " + limit
    if (parseInt(includeUnknown)) {
        query = "SELECT name, value FROM q3_titles_counts limit " + limit
    }

    return await base.find_all(db, query);
}

async function find_all_departments(db, includeOthers, limit = 100) {
    var query = "SELECT name, value FROM q3_departments_counts where name <> 'Others' limit " + limit 
    if (parseInt(includeOthers)) {
        query = "SELECT name, value FROM q3_departments_counts limit " + limit
    }

    return await base.find_all(db, query);
}

async function find_all_locations(db, limit = 100) {
    var query = "SELECT name, value FROM q3_location limit " + limit;
    return await base.find_all(db, query);
}

  module.exports = {
    find_all_titles,
    find_all_departments,
    find_all_locations
  };
  