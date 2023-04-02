const Title = function(Title) {
};

Title.findAll = (db, includeUnknown, limit = 100, result) => {
    var query = "SELECT title_name, count FROM titles where title_name <> 'Unknown' limit ?"
    if (parseInt(includeUnknown)) {
        query = "SELECT title_name, count FROM titles limit ?"
    }
    db.execute(query, [limit], (err, res) => {
        if (err) {
            console.log("error: ", err);
            result(err, null);
            return;
        }
        result(null, res);
    });
  }


  module.exports = Title;