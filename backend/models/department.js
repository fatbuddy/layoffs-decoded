const Department = function(Department) {
};

Department.findAll = (db, includeOthers, limit = 100, result) => {
    var query = "SELECT department, count FROM departments where department <> 'Others' limit ?"
    if (parseInt(includeOthers)) {
        query = "SELECT department, count FROM departments limit ?"
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


  module.exports = Department;