import requests
from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
from db import User
from utils import beautiful_output
from time import sleep

async def last_txns(user, txid, owner='dimees.near'):
    page = 1
    res = []
    flag = True
    while flag:
        url = f'https://api.nearblocks.io/v1/account/{user.account}/txns?page={page}&per_page=25&order=desc'
        try:
            r = requests.get(url)
            txns = json.loads(r.text)['txns']
        except:
            print('Too many requests')
            sleep(1)
            continue
        if len(txns) == 0:
            print('Account or transaction not found!')
            return 0
        for i, tx in enumerate(txns):
            if tx['transaction_hash'] == txid or tx['receiver_account_id'] == owner:
                user.time = int(txns[i - 1]['block_timestamp'][:10])
                flag = False
                break
            if tx['predecessor_account_id'] == 'app.nearcrowd.near':
                res.append(tx['transaction_hash'])
            if i==0:
                print(tx['transaction_hash'])
        page += 1
        if page > 35:
            print('Error. Pls check your transaction ID')
            return 0
    return res


# async def last_txns(user, txid, owner='dimees.near'):
#     res = []
#     url = 'https://near.getblock.io/explorer/tx/list/account'
#     data = {
#         "account": user.account,
#         "count": 80,
#         "offset": 0,
#     }
#     headers = {
#         "x-api-key": "5fad30f1-3305-40f8-a193-5302f9595c3f",
#         "accept": "application/json"
#     }
#     try:
#         r = requests.post(url,headers=headers, json=data)
#         txns = json.loads(r.text)
#     except Exception as e:
#         print(f'Error! {e.args}')
#         return 0
#     if txns == None:
#         print('Account or transaction not found!')
#         return 0
#     for i, tx in enumerate(txns):
#         if tx['receiver_id'] == owner:
#             user.time = int(str(txns[i - 1]['created_at'])[:10])
#             break
#         if tx['signer_id'] == 'app.nearcrowd.near':
#             res.append(tx['hash'])
#     return res




async def get_data(session, user, hsh):
    url = f'https://explorer.near.org/transactions/{hsh}'
    while True:
        async with session.get(url) as resp:
            assert resp.status == 200
            resp_text = await resp.text()
            soup = BeautifulSoup(resp_text, 'html.parser')
            try:
                user.all_data.append(json.loads(soup.find("div", {"class": "c-CodePreviewWrapper-gJFGlx"}).text))
                break
            except:
                continue



async def check(user, txid):
    act_txns = await last_txns(user, txid)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for tx in act_txns:
            task = asyncio.create_task(get_data(session, user, tx))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def get_result(data):
    if len(data) > 1:
        user = User(data[0])
        await check(user, data[1])
    else:
        user = User(data[0])
        await check(user)
    return await beautiful_output(user)


async def get_balance(session,acc):
    url = f'https://nearblocks.io/api/account/balance?address={acc}'
    async with session.get(url) as resp:
        assert resp.status == 200
        resp_text = await resp.text()
        balance = round(float(json.loads(resp_text)['balance']),2)
        sl.update({acc:balance})
    return resp_text


async def get_acc(accounts):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for acc in accounts:
            task = asyncio.create_task(get_balance(session,acc))
            tasks.append(task)
        await asyncio.gather(*tasks)