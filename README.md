# Bulk-Send-TX-with-you-Data-V2
This Python script enables users to send transactions with function data to any smart contract on Ethereum Virtual Machine (EVM) compatible networks. It accepts a list of private keys or mnemonic phrases from a file and sends transactions concurrently using multithreading. The script supports deriving private keys from mnemonic phrases, signing transactions, checking account balances, and handling transaction receipts to determine success or failure. Users can input the network's RPC URL, contract address, function data, gas limit, and the number of threads for execution. The script is adaptable to various EVM networks and outputs the number of completed and failed transactions.

# To run the send.js script, you can follow these steps:
1. Save you private keys/seed phrases in private_keys.txt line by line
2. Pip install re/web3/hexbytes/eth-utils/eth-keys/mnemonic/bip32utils (or simply use "pip install -r requirements.txt")
3. Run script typing "python send.py" in terminal
4. Input contract address/TX data/gas limit and number of threads you need (ctrl + shift + v to paste in visual studio code terminal)
