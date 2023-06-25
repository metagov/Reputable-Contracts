const gateway = artifacts.require("GatewayInterface");

module.exports = function (deployer) {
  deployer.deploy(gateway);
};
