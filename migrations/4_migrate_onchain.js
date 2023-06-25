const onchain = artifacts.require("OnChainReputationData");

module.exports = function (deployer) {
  deployer.deploy(onchain);
};
