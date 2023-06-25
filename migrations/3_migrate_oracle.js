const oracle = artifacts.require("OracleInterface");

module.exports = function (deployer) {
  deployer.deploy(oracle);
};
