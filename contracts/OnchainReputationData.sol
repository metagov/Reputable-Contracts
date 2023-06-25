pragma solidity ^0.8.0;

contract OnChainReputationData{

    //struct to store the aggr score with seller id and 
    //mapping of seller id to uint score

    //function to add aggr score (passes seller id and aggr score)

    //function get_rep_score(seller_id) returns the aggr score (uint)
    mapping(uint => string) public seller_score;
    uint [] scoreArr;
    string score = "empty";

    function add_rep_data(uint _seller_id, string memory _score) public{
        seller_score[_seller_id] = _score;
        scoreArr.push(_seller_id);
        score = _score;
    }

    function get_rep_data(uint _seller_id) public view returns (string memory) {
        return seller_score[_seller_id];
    }

}