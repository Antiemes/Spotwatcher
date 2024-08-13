#!/usr/bin/env python3

import secret
import requests
import time
import os
from importlib import util
import asyncio
from nio import AsyncClient, SyncResponse, RoomMessageText
from datetime import datetime, timezone

async_client = AsyncClient(
    "https://matrix.org", secret.nick
)

def beep():
    pass
    #os.system('play -nq -t alsa synth 2 sine 500')

async def main():
    response = await async_client.login(secret.password)
    print(response)
    lastId = 1

    while True:
        try:
            response = requests.get("https://api2.sota.org.uk/api/spots/50/all%7Call?client=sotawatch&user=anon", timeout = 5)
        #except ConnectionError:
        except Exception as e:
            print("Error in getting spots.")
            time.sleep(30)
            continue
        try:
            json = response.json()
        except RequestsJSONDecodeError:
            continue

        timestampnow = time.time()

        for record in sorted(json, key=lambda d: d['id']):
            id = int(record["id"])
            callsign = record["activatorCallsign"].upper()
            mode = record["mode"].upper()
            frequency = record["frequency"]
            timestampstr = record["timeStamp"] + "Z"
            timestampobj = datetime.fromisoformat(timestampstr)
            timestamp = timestampobj.timestamp()
            foo = timestampobj.astimezone().strftime('%H:%M') #.astimezone(timezone.utc))
            age = timestampnow - timestamp
            if age > 15*60:
                continue
            ha = callsign.startswith("HA") or callsign.startswith("HG")
            if id > lastId and (mode == "SSB" or ha):
                #if record["callsign"] == "RBNHOLE":
                #	print(record)
                content = {
                   "body": "",
                   "msgtype": "m.text"
                }
                content["body"] += f"{callsign} / {frequency} / {mode} (@{foo})"
                if ha:
                    content["body"] += "     !!!"
                    beep()
                print(content["body"])
                await async_client.room_send(secret.roomid, 'm.room.message', content)
                
                lastId = id
        time.sleep(30)

asyncio.run(main())

while True:
    print(x)
    time.sleep(1)
