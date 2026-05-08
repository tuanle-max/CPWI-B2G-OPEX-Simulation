import os
from dotenv import load_dotenv
from algosdk import mnemonic, account
from algosdk.v2client import algod

def check_account_status():
    """
    Check the balance and status of the Algorand account configured in .env
    """
    # Load environment variables from the root .env file
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    m = os.getenv("MAINNET_MNEMONIC")
    address = os.getenv("ALGOD_ADDRESS")
    token = os.getenv("ALGOD_TOKEN")
    
    if not m or "[Dán 25 từ mnemonic" in m:
        print("ERROR: MAINNET_MNEMONIC is not set in .env file.")
        print("Please paste your 25-word mnemonic into the .env file before running this.")
        return

    try:
        # Decode mnemonic
        private_key = mnemonic.to_private_key(m)
        my_address = account.address_from_private_key(private_key)
        print(f"--- MainNet Account Info ---")
        print(f"Address: {my_address}")

        # Initialize AlgodClient
        client = algod.AlgodClient(token, address)
        
        # Query account info
        account_info = client.account_info(my_address)
        micro_algos = account_info.get('amount', 0)
        algo_balance = micro_algos / 1_000_000
        
        print(f"Current Balance: {algo_balance} ALGO")
        print(f"---------------------------")
        
        if algo_balance >= 15:
            print("Status: READY. You have enough ALGO for deployment and tests.")
        elif algo_balance > 0:
            print(f"Status: WARNING. Low balance ({algo_balance} ALGO). Recommend 15-20 ALGO.")
        else:
            print("Status: ERROR. Zero balance. Please fund the account with 15-20 ALGO.")
            
    except Exception as e:
        print(f"ERROR checking account status: {e}")

if __name__ == "__main__":
    check_account_status()
