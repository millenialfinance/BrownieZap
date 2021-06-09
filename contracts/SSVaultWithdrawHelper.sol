//
// SPDX-License-Identifier: UNLICENSED
//
pragma solidity ^0.8.4;
pragma experimental ABIEncoderV2;


import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.1.0/contracts/utils/math/SafeMath.sol";
import "../interfaces/IWithdrawHelper.sol";
import "../interfaces/IZap.sol";

contract SSVaultWithdrawHelper is IWithdrawHelper, Ownable {

  using SafeMath for uint;

  mapping (address => uint256) gasAmount;

  event VaultZap(address vault, address recipient, uint256 amt);
  event ZapError(address vault, address recipient, uint256 amt);

  struct VaultZapData {
    address zapper;
    address from;
    address to;
    address router;
    address vault;
    address recipient;
  }

  function getCallData(
    VaultZapData calldata vaultZapData
  ) public pure returns (bytes memory) {
    return abi.encode(vaultZapData);
  }

  function setGasAmount(address token, uint256 amt) external onlyOwner {
    gasAmount[token] = amt;
  }

  function execute(WithdrawData calldata wd, uint256 actualAmount) override external {
    VaultZapData memory vaultZapData = abi.decode(wd.callData, (VaultZapData));
    uint amt = actualAmount;

    if (vaultZapData.from != address(0)) {
      require(ERC20(vaultZapData.from).approve(vaultZapData.zapper, actualAmount), "UniswapWithdrawHelper: tokenA approve failed.");
    }

    if (address(vaultZapData.recipient).balance == 0) {
      require(actualAmount > gasAmount[wd.assetId]);
      try IZap(vaultZapData.zapper).swapToNative(
          wd.assetId,
          gasAmount[wd.assetId],
          vaultZapData.router,
          vaultZapData.recipient
      ) {
        amt = actualAmount.sub(gasAmount[wd.assetId]);
      } catch {
        ERC20(wd.assetId).transfer(vaultZapData.recipient, ERC20(wd.assetId).balanceOf(address(this)));
        emit ZapError(vaultZapData.vault, vaultZapData.recipient, amt);
        return;
      }
    }

    try IZap(vaultZapData.zapper).zapInTokenToSSVault(
        vaultZapData.from,
        amt,
        vaultZapData.to,
        vaultZapData.router,
        vaultZapData.vault,
        vaultZapData.recipient
      ) {
      emit VaultZap(vaultZapData.vault, vaultZapData.recipient, actualAmount);
    } catch {
      ERC20(wd.assetId).transfer(vaultZapData.recipient, ERC20(wd.assetId).balanceOf(address(this)));
      emit ZapError(vaultZapData.vault, vaultZapData.recipient, amt);
      return;
    }
  }
    /* ========== RESTRICTED FUNCTIONS ========== */

    function withdraw(address token) external onlyOwner {
        if (token == address(0)) {
            payable(owner()).transfer(address(this).balance);
            return;
        }

        ERC20(token).transfer(owner(), ERC20(token).balanceOf(address(this)));
    }
}
