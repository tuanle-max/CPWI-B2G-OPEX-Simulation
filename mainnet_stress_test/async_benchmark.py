import os
import time
import asyncio
import aiohttp
import sys
import base64
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from algosdk import account, mnemonic, transaction, logic
from algosdk.v2client import algod

TOTAL_TXNS = 2500
TARGET_RPS = 50
CONCURRENCY_LIMIT = 500

async def fetch_highest_bid(url, token, app_id):
    client = algod.AlgodClient(token, url)
    try:
        app_info = client.application_info(app_id)
        global_state = app_info.get('params', {}).get('global-state', [])
        for kv in global_state:
            key = base64.b64decode(kv['key']).decode('utf-8')
            if key == 'highest_bid':
                return kv['value']['uint']
    except Exception as e:
        print(f"Error fetching state: {e}")
    return 0

def prepare_transactions(client, sender, private_key, app_id, app_address, start_bid):
    print(f"Preparing {TOTAL_TXNS} transaction groups offline...")
    sp = client.suggested_params()
    # Mở rộng cửa sổ hiệu lực (validity window) lên 1000 block để đảm bảo giao dịch không bị hết hạn khi chạy queue
    sp.last = sp.first + 1000 
    
    txns = []
    current_bid = start_bid + 1
    
    for i in range(TOTAL_TXNS):
        # Yêu cầu: Giao dịch nhóm (Group Txn) gồm 1 PaymentTxn + 1 AppCallTxn.
        # Hợp đồng thực thi thêm 1 Inner Txn. Do đó tổng phí tối thiểu cho cả bộ là 3 * 1000 = 3000 microALGO.
        # Ta gán 2000 cho PaymentTxn và 1000 cho AppCallTxn.
        sp_pay = transaction.SuggestedParams(
            fee=2000, flat_fee=True, first=sp.first, last=sp.last, gh=sp.gh, gen=sp.gen
        )
        pay_txn = transaction.PaymentTxn(
            sender=sender, sp=sp_pay, receiver=app_address, amt=current_bid
        )
        
        sp_app = transaction.SuggestedParams(
            fee=1000, flat_fee=True, first=sp.first, last=sp.last, gh=sp.gh, gen=sp.gen
        )
        app_txn = transaction.ApplicationCallTxn(
            sender=sender, sp=sp_app, index=app_id, on_complete=transaction.OnComplete.NoOpOC
        )
        
        gid = transaction.calculate_group_id([pay_txn, app_txn])
        pay_txn.group = gid
        app_txn.group = gid
        
        signed_pay = pay_txn.sign(private_key)
        signed_app = app_txn.sign(private_key)
        
        # Định dạng bytecode chuẩn cho endpoint POST /v2/transactions
        from algosdk import encoding
        signed_group_bytes = base64.b64decode(encoding.msgpack_encode(signed_pay)) + base64.b64decode(encoding.msgpack_encode(signed_app))
        
        txns.append((pay_txn.get_txid(), signed_group_bytes, 3000))
        current_bid += 1
        
    return txns

async def send_and_wait(session, url, token, txid, raw_bytes, expected_fee, semaphore, results):
    headers = {
        'Content-Type': 'application/x-binary',
        'X-Algo-API-Token': token
    }
    
    async with semaphore:
        start_time = time.time()
        
        # 1. Bắn tải giao dịch (POST)
        try:
            async with session.post(f"{url}/v2/transactions", data=raw_bytes, headers=headers) as resp:
                if resp.status != 200:
                    err = await resp.text()
                    results.append({"txid": txid, "ttf": None, "fee": expected_fee, "status": "failed", "error": err})
                    return
        except Exception as e:
            results.append({"txid": txid, "ttf": None, "fee": expected_fee, "status": "failed", "error": str(e)})
            return
            
        # 2. Đợi xác nhận (Polling TTF)
        await asyncio.sleep(2.0) # Đợi 2s trước khi bắt đầu poll
        while True:
            try:
                async with session.get(f"{url}/v2/transactions/pending/{txid}", headers={'X-Algo-API-Token': token}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("confirmed-round", 0) > 0:
                            ttf = time.time() - start_time
                            actual_fee = data.get("txn", {}).get("txn", {}).get("fee", expected_fee)
                            results.append({"txid": txid, "ttf": ttf, "fee": actual_fee, "status": "success", "error": None})
                            
                            # CIRCUIT BREAKER: Kiểm tra phí
                            algo_fee = actual_fee / 1_000_000
                            # Lưu ý: Vì có 1 Inner Txn, fee tối thiểu cho Group này là 0.003 ALGO.
                            if algo_fee > 0.003: 
                                print(f"\n[CIRCUIT BREAKER] CẢNH BÁO: Phí giao dịch vượt quá giới hạn ({algo_fee} ALGO) cho TXID {txid}. Dừng hệ thống khẩn cấp!")
                                os._exit(1)
                            return
                            
                        if data.get("pool-error"):
                            results.append({"txid": txid, "ttf": None, "fee": expected_fee, "status": "failed", "error": data.get("pool-error")})
                            return
            except Exception:
                pass # Bỏ qua lỗi kết nối tạm thời và thử lại ở vòng lặp sau
                
            await asyncio.sleep(1.0)

async def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    m = os.getenv("MAINNET_MNEMONIC")
    url = os.getenv("ALGOD_ADDRESS", "https://mainnet-api.algonode.cloud")
    token = os.getenv("ALGOD_TOKEN", "")
    app_id = int(os.getenv("APP_ID", 0))
    
    if not m or not app_id:
        print("ERROR: Không tìm thấy Mnemonic hoặc APP_ID trong .env.")
        return

    private_key = mnemonic.to_private_key(m)
    sender = account.address_from_private_key(private_key)
    app_address = logic.get_application_address(app_id)
    
    print(f"Address: {sender}")
    print(f"App ID: {app_id} | App Address: {app_address}")
    
    client = algod.AlgodClient(token, url)
    start_bid = await fetch_highest_bid(url, token, app_id)
    print(f"Current highest bid is: {start_bid} microALGO.")
    
    txns = prepare_transactions(client, sender, private_key, app_id, app_address, start_bid)
    
    results = []
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    print(f"STARTING ASYNC BENCHMARK: Sending {TOTAL_TXNS} txns at {TARGET_RPS} RPS...")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for idx, (txid, raw_bytes, fee) in enumerate(txns):
            task = asyncio.create_task(send_and_wait(session, url, token, txid, raw_bytes, fee, semaphore, results))
            tasks.append(task)
            
            await asyncio.sleep(1.0 / TARGET_RPS)
            
            if (idx + 1) % 500 == 0:
                print(f"Dispatched {idx + 1}/{TOTAL_TXNS} txns...")
                
        print("All transactions dispatched. Waiting for confirmations...")
        await asyncio.gather(*tasks)
        
    df = pd.DataFrame(results)
    df.to_csv("mainnet_results.csv", index=False)
    
    success_df = df[df['status'] == 'success']
    failed_count = len(df) - len(success_df)
    
    print("\n" + "="*40)
    print(" MAINNET STRESS-TEST REPORT")
    print("="*40)
    print(f"Total Sent : {TOTAL_TXNS}")
    print(f"Success    : {len(success_df)}")
    print(f"Failed     : {failed_count}")
    
    if len(success_df) > 0:
        median_ttf = np.median(success_df['ttf'])
        p95_ttf = np.percentile(success_df['ttf'], 95)
        max_fee = np.max(success_df['fee']) / 1_000_000
        
        print(f"\n[PERFORMANCE]")
        print(f"Median TTF : {median_ttf:.2f} seconds")
        print(f"p95 TTF    : {p95_ttf:.2f} seconds")
        print(f"Max Fee    : {max_fee} ALGO")
    
    print(f"\n=> Results saved to mainnet_results.csv")

if __name__ == "__main__":
    asyncio.run(main())
