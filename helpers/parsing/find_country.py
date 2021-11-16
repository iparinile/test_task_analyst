import aiohttp
import asyncio
import os

import ipinfo
from dotenv import load_dotenv


async def get_ip_info(session, url):
    async with session.get(url) as resp:
        ip_info = await resp.json(content_type='text/html')
        return ip_info


async def async_main(ips: list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ip in ips:
            url = f'https://geolocation-db.com/json/{ip}'
            tasks.append(asyncio.ensure_future(get_ip_info(session, url)))

        ip_info_list = await asyncio.gather(*tasks)
        return ip_info_list


def get_country_name_for_ips(ips: list) -> list:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    res = asyncio.run(async_main(ips))
    return res


def insert_country_into_users(users: dict) -> dict:
    load_dotenv()
    access_token = os.getenv('ipinfo_token')
    handler = ipinfo.getHandler(access_token)
    users_ips = [ip for ip in users.keys()]
    users_info_response = handler.getBatchDetails(users_ips)
    for user_ip in users_info_response.keys():
        users[user_ip]['country'] = users_info_response[user_ip]['country_name']
    return users


if __name__ == '__main__':
    list_ip = ['217.89.121.82', '121.165.118.201']
    get_country_name_for_ips(list_ip)
