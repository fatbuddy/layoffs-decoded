const AthenaExpress = require("athena-express");
var config = require("../config.js");
//Importing the AWS SDK
const AWS = require("aws-sdk");

// Configuring the region and credentials to make connection to AWS Athena
console.log(config["awsCredentials"])
 AWS.config.update(config["awsCredentials"]);
//configuring athena-express with aws sdk object
 const athenaExpressConfig = { aws: AWS,
	getStats: true }; 
 // Creating Athena Express service object
 const athenaExpress = new AthenaExpress(athenaExpressConfig);

 module.exports = athenaExpress;
