// SPDX-License-Identifier: MIT

// Oracle smart contract which will interact with 'Gateway' contract

pragma solidity ^0.8.0;

import "./Gateway.sol";

contract OracleInterface {
    
    // Event stored on blockchain whicn oracle backend would poll for
    // Parameters are taken from event to be parsed by the oracle 
    event RequestValueEvent(uint sellerId, uint[] userId, string[] array);
    event RequestScoreEvent(uint sellerId, uint token_val, uint user_id, uint indi_score);
    // event ReturnToClientEvent(uint id, address client_address, uint result);
    
    // mapping(uint => bool) public requests_pending; 
    
    // Gateway contract will interact with this function to use the oracle
    function requestValue(uint _sellerId, uint[] memory _userId, string[] memory _array) public {
        // address nonceValue = 0x179288a02eE8a939668DDbb0Ac21b4Fc2A9606A7;
        // uint id = uint(keccak256(abi.encodePacked(block.timestamp, nonceValue))) % 1000000000000;
        
        // requests_pending[id] = true;
        emit RequestValueEvent(_sellerId, _userId, _array);
    }
    
    function requestScore(uint _sellerId, uint token_val, uint user_id, uint _indi_score) public {
        emit RequestScoreEvent(_sellerId, token_val, user_id, _indi_score);
    }
    
    // Aggregate score will be returned back to the Gateway contract using this function
    function returnToGateway(address _gateway_address, string memory _aggr_score, string memory _off_chain) public {
        // require(requests_pending[_id]);
        // delete requests_pending[_id];
        
        GatewayInterface gatewayContract;
        gatewayContract = GatewayInterface(_gateway_address);
        gatewayContract.callback(_aggr_score, _off_chain);
        // emit ReturnToClientEvent(_id, _client_address, _aggr_score);
    }

}