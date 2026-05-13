pragma solidity ^0.8.0;

contract ProductTraceability {

    mapping(string => string) public productHashes;

    function storeProduct(string memory batch, string memory hash) public {
        productHashes[batch] = hash;
    }

    function getProduct(string memory batch) public view returns(string memory) {
        return productHashes[batch];
    }
}