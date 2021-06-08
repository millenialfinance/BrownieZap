#!/usr/bin/env python3

from brownie import *

WMATIC = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"

WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"

SPIRIT = "0x5cc61a78f164885776aa610fb0fe1257df78e59b"
WFTM = "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83"

ICE_FTM = "0xf16e81dce15B08F326220742020379B855B87DF9"

SPIRIT_ROUTER = "0x16327e3fbdaca3bcf7e38f5af2599d2ddc33ae52"

DAI_SPIRIT_LP = "0xfFbfc0446cA725b21256461e214E9D472f9be390"

DAI_SPIRIT_VAULT = "0xd0CA2E5A8c12F56a130A7d609DcAC0f820743056"

matic_tokens = {}
matic_tokens['dai'] = '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'
matic_tokens['usdc'] = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
matic_tokens['usdt'] = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'

ftm_tokens = {}
ftm_tokens['dai'] = '0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e'
ftm_tokens['usdc'] = '0x04068da6c83afcfa0e13ba15a6696662335d5b75'
ftm_tokens['usdt'] = '0x049d68029688eabf473097a2fc38ef61633a3c7a'
ftm_tokens['busd'] = '0xc931f61b1534eb21d8c11b24f3f5ab2471d4ab50'

bsc_tokens = {}
bsc_tokens['dai'] = '0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3'
bsc_tokens['usdc'] = '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d'
bsc_tokens['usdt'] = '0x55d398326f99059fF775485246999027B3197955'

def deployLPHelperMatic(zapperAddress):
    addr = accounts[-1].address
    print("Deploying with", addr)
    lpHelper = LPVaultWithdrawHelper.deploy({'from': accounts[-1]})
    lpHelper.setGasAmount(matic_tokens['dai'], 50000000000000000)
    lpHelper.setGasAmount(matic_tokens['usdc'], 50000)
    lpHelper.setGasAmount(matic_tokens['usdt'], 50000)
    return lpHelper

def deploySSHelperMatic(zapperAddress):
    addr = accounts[-1].address
    print("Deploying with", addr)
    lpHelper = SSVaultWithdrawHelper.deploy({'from': accounts[-1]})
    lpHelper.setGasAmount(matic_tokens['dai'], 50000000000000000)
    lpHelper.setGasAmount(matic_tokens['usdc'], 50000)
    lpHelper.setGasAmount(matic_tokens['usdt'], 50000)
    return lpHelper


def deployZapper(WNATIVE):
    zap = Zap.deploy(WNATIVE, {'from': accounts[-1]})
    if WNATIVE == WFTM:
        zap.setTokenBridgeForRouter(ftm_tokens['dai'], SPIRIT_ROUTER, SPIRIT);
        zap.setTokenBridgeForRouter(ftm_tokens['busd'], SPIRIT_ROUTER, ftm_tokens['busd'])
    return zap

def deployLPHelper(zapperAddress, tokens):
    addr = accounts[-1].address
    print("Deploying with", addr)
    lpHelper = LPVaultWithdrawHelper.deploy({'from': accounts[-1]})
    lpHelper.setGasAmount(tokens['dai'], 50000000000000000)
    lpHelper.setGasAmount(tokens['usdc'], 50000)
    lpHelper.setGasAmount(tokens['usdt'], 50000)
    return lpHelper

def deploySSHelper(zapperAddress, tokens):
    addr = accounts[-1].address
    print("Deploying with", addr)
    ssHelper = SSVaultWithdrawHelper.deploy({'from': accounts[-1]})
    ssHelper.setGasAmount(tokens['dai'], 50000000000000000)
    ssHelper.setGasAmount(tokens['usdc'], 50000)
    ssHelper.setGasAmount(tokens['usdt'], 50000)
    return ssHelper

def maticDeploy():
    accounts.load('m')
    print("Zapping with ", accounts[-1].address)
    zap = deployZapper(WMATIC)
    LPhelper = deployLPHelperMatic(zap.address, matic_tokens)
    SShelper = deploySSHelperMatic(zap.address, matic_tokens)
    print("Zapper address: ", zap.address)
    print("LP Helper address: ", LPhelper.address)
    print("SS Helper address: ", SShelper.address)

def bscDeploy():
    accounts.load('m')
    print("Zapping with ", accounts[-1].address)
    zap = deployZapper(BSC)
    LPhelper = deployLPHelperMatic(zap.address, bsc_tokens)
    SShelper = deploySSHelperMatic(zap.address, bsc_tokens)
    print("Zapper address: ", zap.address)
    print("LP Helper address: ", LPhelper.address)
    print("SS Helper address: ", SShelper.address)



def fantomDeploy():
    # accounts.at("0x8800528f6b9480dbbffd65fe6d8cc075bac7c1a8", force=True)
    #accounts.at("0xC6C68811E75EfD86d012587849F1A1D30427361d", force=True)
    accounts.load('m')
    print("Zapping with ", accounts[-1].address)
    zap = deployZapper(WFTM)
    LPhelper = deployLPHelper(zap.address, ftm_tokens)
    SShelper = deploySSHelper(zap.address, ftm_tokens)
    print("Zapper address: ", zap.address)
    print("LP Helper address: ", LPhelper.address)
    print("SS Helper address: ", SShelper.address)

def main():
    fantomDeploy()
