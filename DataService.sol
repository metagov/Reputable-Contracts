pragma solidity ^0.8.0;
// SPDX-License-Identifier: MIT

import "./Oracle.sol";


contract WebInterface {
    // Aggregator contract
    address public oracle_address;
    OracleInterface private oracleContract;
    //string user_rating;
    //address user_addr;
    uint seller_id = 3;
    // store aggr in variable
    
    // 5 values instead
    struct Tokens {
        uint [] token_val;
        bool [] used;
        uint [] scores;
        uint [] camps;
        //can store the campaign id and user id.
        //address [] user_addr;
        
    }
    
    constructor() {
        
        for (uint i=0; i<12; i++) {
            addData(11, 1234, true, 1, 1);
        }
        
    }
    //local variable for user_addr and 
    
    //Tokens [] tokensArr;
    uint [] tokensArr;
    //mappin of seller addrs to seller_ids
    //mapping of seller ids to the arrays
    //with the arrays we can loop to find the info
    
    mapping(uint => Tokens) seller_tokens;
    
    function addToToken(uint tok_val, bool use) public {
        //seller
        //make a new struct 
        //popoulate the mapping with the struct
        //add the mapping value in an array
        seller_id = 4;
        
    }
    
    function setOracleAddress(address _oracle_address) public {
        oracle_address = _oracle_address;
        oracleContract = OracleInterface(_oracle_address);
    }
    
    // seller_id, camapaign_id, inside aggr function
    // remove campaign id 
    function aggr(uint _campaign_id, uint _seller_id, uint _user_id) public {
        
        uint[] memory scores = seller_tokens[_seller_id].scores;
        oracleContract.requestValue(_campaign_id, _seller_id, _user_id, scores);
        
        //connect to proprietary oracle
        //look at example looking at chainlink

    }

    //emit event for aggregation to be parsed to oracle

    function getSellerId() public view returns (uint) {
        return seller_id;
    }


    function addData(uint _seller_id, uint _token_val, bool _used, uint _score, uint _campaign_id) public {
        
        //uint [] memory tok;
        //bool [] memory use;
        //value already set to 12 so it's only changing the last value.
        //can later check if the seller exists before putting calling the
        //function to create one.
        
        //need to push the values
        seller_tokens[_seller_id].token_val.push(_token_val);
        seller_tokens[_seller_id].used.push(_used);
        seller_tokens[_seller_id].scores.push(_score);
        seller_tokens[_seller_id].camps.push(_campaign_id);
        tokensArr.push(_seller_id);
        //emit feedback submitted event
        //event will contain user id campaing and seller id.
        //event feedback_submitted(uint _seller_id, uint _campId, uint _user_id);
        //emit feedback_submitted(seller_id, camp_id, user_id);
        
        //I am making a new array every time the function is called
        //change it to a var if needed
        //Make the memory already initiated
        //We just add data to it.
        
         
        
        //token.token_val.push(_token_val);
        //token.used.push(_used);
        //var seller_tokens = seller_tokens[_seller_id];
        //seller_tokens.token_val.push(_token_val);
        //seller_tokens.used.push(_used);
    }

    function getTokenArr() view public returns (uint[] memory) {
        return tokensArr;
    }

    function getData(uint _seller_id) view public returns (uint[] memory, bool[] memory, uint[] memory, uint[] memory){
        return(seller_tokens[_seller_id].token_val, seller_tokens[_seller_id].used, seller_tokens[_seller_id].scores, seller_tokens[_seller_id].camps);
    }

    function newSeller(uint _seller_id) public {
        uint [] memory tok;
        bool [] memory use;
        uint [] memory score;
        uint [] memory camp;
        //seller_tokens[_seller_id] = Tokens(new uint[] (12), new bool [] (12));
        seller_tokens[_seller_id] = Tokens(tok, use, score, camp);
    }
    function countScoresForSeller(uint _seller_id) view public returns (uint) {
        //later implemented to count the array of a specific seller
        
    }

    function isValid(uint _seller_id, uint _token_val) public view returns (bool) {
        uint [] memory token_arrays =  seller_tokens[_seller_id].token_val;
        //if (seller_tokens[_seller_id].token_val == _token_val){
        bool action = false;
        
        for(uint i=0; i<=token_arrays.length; i++){
            if (token_arrays[i] ==_token_val){
                //seller_tokens instead of token_arrays
                action = true;
            }
            
        }
        
        return action;
        //return seller_tokens[_seller_id].token_val == _token_val;
    }



}