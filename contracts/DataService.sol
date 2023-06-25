// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Oracle.sol";


contract WebInterface {
    // Aggregator contract
    address public oracle_address;
    OracleInterface private oracleContract;
    //string user_rating;
    //address user_addr;
    uint seller_id = 3;
    // store aggr in variable
    mapping(uint => bool) public isTokenUsed;
    // 5 values instead
    struct Tokens {
        uint [] token_val;
        string [] scores;
        uint [] camps;
        uint [] user_id;
        mapping(uint => bool) used;
        uint count;
    }
    
    event ScoreAdded(uint sellerId, uint token, uint user_id);
    
    constructor() {
        //count = 0;
        //for (uint i=0; i<12; i++) {
        //    addData(11, 1234, true, "1", 1);
        //}
        
        //WebInterface w;
        //w = new WebInterface();
        //w.adder(11, 101, 1001, 1);
        //w.adder(11, 102, 1002, 1);
        //w.adder(11, 103, 1003, 0);
        //w.adder(11, 104, 1004, 1);
        //w.adder(11, 105, 1005, 1);
        //setOracleAddress(0x1aFA492984C229614C9C33907C8024e084c7372E);
        //adder(11, 104, 1004, 1);
        
    }
    //local variable for user_addr and 
    
    //Tokens [] tokensArr;
    uint [] tokensArr;
    //mappin of seller addrs to seller_ids
    //mapping of seller ids to the arrays
    //with the arrays we can loop to find the info
    
    mapping(uint => Tokens) seller_tokens;
    
    function setOracleAddress(address _oracle_address) public {
        oracle_address = _oracle_address;
        oracleContract = OracleInterface(_oracle_address);
    }
    
    function aggr(uint _seller_id) public {
        
        uint[] memory user_id = seller_tokens[_seller_id].user_id;
        string[] memory scores = seller_tokens[_seller_id].scores;
        oracleContract.requestValue(_seller_id, user_id, scores);

    }

    //emit event for aggregation to be parsed to oracle

    function getSellerId() public view returns (uint) {
        return seller_id;
    }
    
//    function encrypt(uint _seller_id, uint _score) public returns (string memory){
//        oracleContract.requestScore(_seller_id, _score);

    function adder(uint _seller_id, uint _token_val, uint _user_id, uint _val) public{
        //encrypt function
        oracleContract.requestScore(_seller_id, _token_val, _user_id, _val);
    }
    
    function add(uint _seller_id, uint _token_val, uint _user_id, string memory _enc_val) public {
    
        seller_tokens[_seller_id].token_val.push(_token_val); //token array to be used for seller id and tokens
        seller_tokens[_seller_id].used[_token_val]= true;
        seller_tokens[_seller_id].scores.push(_enc_val) ;
        seller_tokens[_seller_id].user_id.push(_user_id);
        seller_tokens[_seller_id].count++;
        tokensArr.push(_seller_id);
        emit ScoreAdded(_seller_id, _token_val, _user_id);
        if (seller_tokens[_seller_id].count == 5){
            aggr(_seller_id);
        }
}

    function getTokenArr() view public returns (uint[] memory) {
        return tokensArr;
    }

    function getData(uint _seller_id) view public returns (uint[] memory, uint[] memory, string[] memory){
        return(seller_tokens[_seller_id].token_val, seller_tokens[_seller_id].user_id, seller_tokens[_seller_id].scores);
    }

    function ASeller(uint _seller_id) public {
        string [] memory _scores;
        uint [] memory _camps;
        uint [] memory _user_id;
        uint [] memory _tok;
        Tokens storage t = seller_tokens[_seller_id];
        t.token_val = _tok;
        t.scores = _scores;
        t.camps = _camps;
        t.user_id = _user_id;
        t.used[_seller_id] = false;
        t.count = 0;
}
    
    function isUsed(uint _seller_id, uint _token_val) public view returns  (bool){
    return seller_tokens[_seller_id].used[_token_val];
    }
}