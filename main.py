import asyncio
import os
import traceback

import aiohttp
import discord
import twikit
from twikit.streaming import Topic

client = twikit.Client(language="ja-JP", proxy=os.getenv("proxy"))


async def main():
    httpSession = aiohttp.ClientSession()
    webhook1 = discord.Webhook.from_url(os.getenv("webhook1"), session=httpSession)
    webhook2 = discord.Webhook.from_url(os.getenv("webhook2"), session=httpSession)
    webhook3 = discord.Webhook.from_url(os.getenv("webhook3"), session=httpSession)

    try:
        await client.login(
            auth_info_1=os.getenv("username"),
            auth_info_2=os.getenv("email"),
            password=os.getenv("password"),
            cookies_file="cookies.json",
        )

        user = await client.user()
        print(f"Logined as {user.name} (@{user.screen_name})")
        topics = {
            Topic.dm_update("1894362909465350511"),  # 無名のプロセカ雑談グループ
            Topic.dm_update("1895631561472819265"),  # 名言botを許さない会審査室
            Topic.dm_update("1895834188533940600"),  # 名言botを許さない会【ホロ支部】
        }
        session = await client.get_streaming_session(topics)
        async for topic, payload in session:
            if payload.dm_update:
                match (payload.dm_update.conversation_id):
                    # 無名のプロセカ雑談グループ
                    case "1894362909465350511":
                        messages = await client.get_group_dm_history(
                            "1894362909465350511"
                        )
                        message = messages[0]
                        user = await client.get_user_by_id(message.sender_id)
                        await webhook1.send(
                            content=message.text,
                            username=f"{user.name} (@{user.screen_name})",
                            avatar_url=user.profile_image_url,
                        )
                    # 名言botを許さない会審査室
                    case "1895631561472819265":
                        messages = await client.get_group_dm_history(
                            "1895631561472819265"
                        )
                        message = messages[0]
                        user = await client.get_user_by_id(message.sender_id)
                        await webhook2.send(
                            content=message.text,
                            username=f"{user.name} (@{user.screen_name})",
                            avatar_url=user.profile_image_url,
                        )
                    # 名言botを許さない会【ホロ支部】
                    case "1895834188533940600":
                        messages = await client.get_group_dm_history(
                            "1895834188533940600"
                        )
                        message = messages[0]
                        user = await client.get_user_by_id(message.sender_id)
                        await webhook3.send(
                            content=message.text,
                            username=f"{user.name} (@{user.screen_name})",
                            avatar_url=user.profile_image_url,
                        )
    except:
        traceback.print_exc()
        await httpSession.close()


asyncio.run(main())
