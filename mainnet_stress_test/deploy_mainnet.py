import os
import base64
import time
from dotenv import load_dotenv
from algosdk import account, mnemonic, transaction, logic
from algosdk.v2client import algod
import auction_contract
from pyteal import compileTeal, Mode

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

def deploy():
    # Load .env variables
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    m = os.getenv("MAINNET_MNEMONIC")
    address = os.getenv("ALGOD_ADDRESS")
    token = os.getenv("ALGOD_TOKEN")

    if not m or not address:
        print("ERROR: Environment variables missing.")
        return

    # Setup Account
    private_key = mnemonic.to_private_key(m)
    sender = account.address_from_private_key(private_key)
    
    # Initialize Algod Client
    client = algod.AlgodClient(token, address)
    
    print("Compiling PyTeal programs...")
    approval_teal = compileTeal(auction_contract.approval_program(), mode=Mode.Application, version=6)
    clear_teal = compileTeal(auction_contract.clear_state_program(), mode=Mode.Application, version=6)
    
    approval_bytes = compile_program(client, approval_teal)
    clear_bytes = compile_program(client, clear_teal)
    
    print("Fetching suggested parameters...")
    sp = client.suggested_params()
    
    # Global state schema: 1 integer (highest_bid) and 1 byte slice (highest_bidder)
    global_schema = transaction.StateSchema(num_uints=2, num_byte_slices=1)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)
    
    print("Creating ApplicationCreateTxn...")
    txn = transaction.ApplicationCreateTxn(
        sender=sender,
        sp=sp,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_bytes,
        clear_program=clear_bytes,
        global_schema=global_schema,
        local_schema=local_schema
    )
    
    # Sign transaction
    print("Signing transaction...")
    signed_txn = txn.sign(private_key)
    
    # Send transaction
    print("Sending transaction to MainNet...")
    try:
        tx_id = client.send_transaction(signed_txn)
        print(f"Transaction ID: {tx_id}")
    except Exception as e:
        print(f"ERROR submitting transaction: {e}")
        return
    
    # Wait for confirmation
    print("Waiting for confirmation (this may take a few seconds)...")
    try:
        result = transaction.wait_for_confirmation(client, tx_id, 4)
        app_id = result['application-index']
        app_address = logic.get_application_address(app_id)
        
        print(f"\n--- DEPLOYMENT SUCCESSFUL ---")
        print(f"App ID: {app_id}")
        print(f"App Address: {app_address}")
        
        # Update .env file
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        with open(env_path, 'r') as f:
            lines = f.readlines()
        with open(env_path, 'w') as f:
            for line in lines:
                if line.startswith("APP_ID="):
                    f.write(f"APP_ID=\"{app_id}\"\n")
                else:
                    f.write(line)
        print("Updated APP_ID in .env file.")
        
    except Exception as e:
        print(f"ERROR waiting for confirmation: {e}")

if __name__ == "__main__":
    deploy()
