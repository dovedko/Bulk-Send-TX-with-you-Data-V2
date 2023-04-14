# Import required libraries
import binascii
import web3
from hexbytes import HexBytes
import concurrent.futures
from eth_account import Account
from eth_utils import to_bytes
from eth_keys import keys
from mnemonic import Mnemonic
from bip32utils import BIP32Key, BIP32_HARDEN
import re

# Function to send transaction
def send_transaction(credential):
    # Check if the input is a mnemonic phrase or private key
    is_mnemonic = len(credential.split()) >= 12

    if is_mnemonic:
        # Derive the private key from the mnemonic phrase
        mnemonic = Mnemonic("english")
        seed = mnemonic.to_seed(credential.strip())
        master_key = BIP32Key.fromEntropy(seed)
        child_key = master_key.ChildKey(44 + BIP32_HARDEN).ChildKey(60 + BIP32_HARDEN).ChildKey(0 + BIP32_HARDEN).ChildKey(0).ChildKey(0)
        private_key_hex = child_key.PrivateKey().hex()
        private_key_bytes = to_bytes(hexstr=private_key_hex)
    else:
        # Remove the '0x' prefix if it exists
        if credential.startswith('0x'):
            credential = credential[2:]

        # Convert the private key to bytes
        private_key_bytes = binascii.unhexlify(credential.strip())

    # Get the account address associated with the private key
    address = Account.privateKeyToAccount(private_key_bytes).address

    # Get the nonce for the account
    nonce = w3.eth.getTransactionCount(address)

    # Set the transaction parameters
    chain_id = 56
    tx_params = {
        "nonce": nonce,
        "gasPrice": gas_price,
        "gas": gas_limit,
        "to": contract_address,
        "value": 0,
        "data": data,
        "chainId": chain_id,
    }

    # Check if the account balance is sufficient to cover the gas fees
    balance = w3.eth.getBalance(address)
    required_balance = gas_price * gas_limit
    if balance < required_balance:
        print(f"Insufficient balance for address: {address}")
        return False

    # Sign the transaction
    signed_tx = w3.eth.account.signTransaction(tx_params, private_key_bytes)

    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=transaction_wait_time)

    # Check the transaction status
    if tx_receipt["status"] == 1:
        # Transaction was successful
        print(f"Completed: {tx_hash.hex()}")
        return True
    else:
        # Transaction failed
        print(f"Failed: {tx_hash.hex()}")
        return False

# Set the Binance Smart Chain endpoint URL (I recommend to use custom ankr RPC)
w3 = web3.Web3(web3.Web3.HTTPProvider("https://rpc.ankr.com/bsc"))

# Get the contract address, data, and gas limit from user input
contract_address_input = input("Enter the contract address (Interacted With (To) - address from bscscan): ")
contract_address = HexBytes(contract_address_input)
data_input = input("Enter the function data (Input Data - from bscscan): ")
data = HexBytes(data_input)
gas_limit = int(input("Enter the gas limit (50000 - send transaction, 500000 - contract interaction): "))

gas_price_gwei = float(input("Enter the gas price in gwei (e.g., 1.2): "))
gas_price = int(gas_price_gwei * 1e9)

transaction_wait_time = int(input("Enter the transaction wait time in seconds (e.g., 300): "))

# Load the credentials from a file
with open("private_keys.txt", "r") as f:
    credentials = f.readlines()

# Initialize the counter variables
completed_count = 0
failed_count = 0

# Get the number of threads from user input
num_threads = int(input("Enter the number of threads (number of your wallets): "))

# Iterate over the credentials and send a transaction for each one using multithreading
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = list(executor.map(send_transaction, credentials))

# Count the completed and failed transactions
completed_count = results.count(True)
failed_count = results.count(False)

# Print the results
print(f"Total transactions: {len(credentials)}")
print(f"Completed: {completed_count}")
print(f"Failed: {failed_count}")
