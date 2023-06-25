const web_int = artifacts.require("WebInterface");

module.exports = function (deployer) {
  deployer.deploy(web_int);
};
