// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

interface IZap {
    function swapToken(address _from, uint amount, address _to, address routerAddr, address _recipient) external;
    function swapToNative(address _from, uint amount, address routerAddr, address _recipient) external;
    function zapIn(address _to, address routerAddr, address _recipient) external payable;
    function zapInToLPVault(address _to, address routerAddr, address _vault, address _recipient) external payable;
    function zapInToSSVault(address _to, address routerAddr, address _vault, address _recipient) external payable;
    function zapInToken(address _from, uint amount, address _to, address routerAddr, address _recipient) external;
    function zapInTokenToLPVault(address _from, uint amount, address _to, address routerAddr, address _vault, address _recipient) external;
    function zapInTokenToSSVault(address _from, uint amount, address _to, address routerAddr, address _vault, address _recipient) external;
    function zapAcross(address _from, uint amount, address _toRouter, address _recipient) external;
    function zapOut(address _from, uint amount, address routerAddr, address _recipient) external;
    function zapOutToken(address _from, uint amount, address _to, address routerAddr, address _recipient) external;
}
