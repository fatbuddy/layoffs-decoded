const athenaHandler = require("./athena-handler");

async function find_all(db, query) {

    let myQuery = {
        sql : query,
        db : db
    };

    console.log(myQuery.sql)

    await athenaHandler
	.query(myQuery)
	.then(results => {
        output = {success: true, payload: results.Items };
        console.log(output);
	})
	.catch(error => {
        output = {success: false, payload: error };
		console.log(error);
	});   

    return output;
}

module.exports = {
    find_all
};
