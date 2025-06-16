import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsSearch

api_id = 6067591
api_hash = "94e17044c2393f43fda31d3afe77b26b"
bot_token = "7756558480:AAF-vp2SWzdeUOq2sl_V-w48VphfJ-sP5Pk"
OWNER_ID = 8075557596

# ✅ Replace this with your group ID (negative number)
CHAT_ID = -1001428862998

client = TelegramClient("banall_bot", api_id, api_hash).start(bot_token=bot_token)

ban_rights = ChatBannedRights(
    until_date=None,
    view_messages=True
)

async def auto_ban_chat_members():
    chat = await client.get_entity(CHAT_ID)
    total_banned = 0

    print(f"🚫 Starting ban process in: {chat.title}")

    while True:
        banned_this_round = 0

        async for user in client.iter_participants(chat.id, filter=ChannelParticipantsSearch("")):
            try:
                if user.id == OWNER_ID or user.bot:
                    continue

                perms = await client.get_permissions(chat.id, user.id)
                if perms.is_admin or perms.is_creator:
                    continue

                await client(EditBannedRequest(
                    channel=chat.id,
                    participant=user.id,
                    banned_rights=ban_rights
                ))

                total_banned += 1
                banned_this_round += 1
                print(f"Banned: {user.id}")
                await asyncio.sleep(0.4)

            except Exception as e:
                print(f"❌ Failed to ban {user.id}: {e}")
                continue

        if banned_this_round == 0:
            break

    print(f"✅ Finished banning total {total_banned} members in '{chat.title}'.")

async def main():
    await auto_ban_chat_members()

print("Bot is running...")
with client:
    client.loop.run_until_complete(main())
