import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsSearch

api_id = 6067591
api_hash = "94e17044c2393f43fda31d3afe77b26b"
bot_token = "7756558480:AAF-vp2SWzdeUOq2sl_V-w48VphfJ-sP5Pk"
OWNER_ID = 8075557596


client = TelegramClient("banall_bot", api_id, api_hash).start(bot_token=bot_token)

ban_rights = ChatBannedRights(
    until_date=None,
    view_messages=True
)

@client.on(events.NewMessage(pattern='/banall'))
async def ban_all_handler(event):
    sender = await event.get_sender()
    chat = await event.get_chat()

    if sender.id != OWNER_ID or not event.is_group:
        return

    progress = await client.send_message(chat.id, "🚫 Banning all members... Please wait.")
    count = 0

    try:
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
                count += 1
                await asyncio.sleep(0.4)
            except Exception as e:
                print(f"❌ Failed to ban {user.id}: {e}")
                continue

        await client.send_message(chat.id, f"✅ Finished banning {count} members.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

print("Bot is running...")
client.run_until_disconnected()
