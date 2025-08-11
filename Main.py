import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantsSearch, ChannelParticipantsKicked

api_id = 6067591
api_hash = "94e17044c2393f43fda31d3afe77b26b"
bot_token = "7282536736:AAH8VWBWU9F5ZAIATg5pDu1l1ouzke2s6dg"

client = TelegramClient("banall_bot", api_id, api_hash).start(bot_token=bot_token)

ban_rights = ChatBannedRights(until_date=None, view_messages=True)
unban_rights = ChatBannedRights(until_date=None, view_messages=False)

@client.on(events.NewMessage(pattern='/banall'))
async def ban_all_handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    if not event.is_group:
        await event.reply("❌ This command only works in groups.")
        return

    msg = await client.send_message(event.chat_id, "🚫 Banning all non-admins (including bots)... Please wait.")
    await asyncio.sleep(1)
    await msg.delete()

    total_banned = 0

    async for user in client.iter_participants(chat.id, filter=ChannelParticipantsSearch("")):
        try:
            if user.id == sender.id or user.id == (await client.get_me()).id:
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
            await asyncio.sleep(0.2)

        except Exception as e:
            print(f"❌ Failed to ban {user.id}: {e}")
            continue

    await client.send_message(chat.id, f"✅ Finished banning {total_banned} non-admin members (including bots).")

@client.on(events.NewMessage(pattern='/unbanall'))
async def unban_all_handler(event):
    chat = await event.get_chat()

    if not event.is_group:
        await event.reply("❌ This command only works in groups.")
        return

    msg = await client.send_message(event.chat_id, "🔄 Unbanning all previously banned users...")
    await asyncio.sleep(1)
    await msg.delete()

    total_unbanned = 0

    async for banned_user in client.iter_participants(chat.id, filter=ChannelParticipantsKicked):
        try:
            await client(EditBannedRequest(
                channel=chat.id,
                participant=banned_user.id,
                banned_rights=unban_rights
            ))
            total_unbanned += 1
            await asyncio.sleep(0.2)

        except Exception as e:
            print(f"❌ Failed to unban {banned_user.id}: {e}")
            continue

    await client.send_message(chat.id, f"✅ Unbanned total {total_unbanned} users.")

print("Bot is running...")
client.run_until_disconnected()
