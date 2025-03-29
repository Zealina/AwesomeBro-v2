"""Manage Groups and User Addition"""
from telegram.constants import ChatMemberStatus
from telegram.ext import Application, CommandHandler, CallbackContext
import logging

ALLOWED_PERSONS = {123456789, 987654321}


def add_group_to_database(chat_id, title, added_by):
    """Simulate adding a group to the database."""
    logging.info(f"Group '{title}' (ID: {chat_id}) added by {added_by}")


async def check_group(update: Update, context: CallbackContext):
    """Handler to verify group addition and bot admin status."""
    chat = update.effective_chat
    user = update.effective_user

    if not chat or not user or chat.type == "private":
        return

    
    if user.id not in ALLOWED_PERSONS:
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text="You are not authorized to add me to a group."
            )
        except Exception:
            logging.warning(f"Couldn't send DM to {user.id} (maybe they blocked bot).")
        await context.bot.leave_chat(chat.id)
        return

    
    chat_admins = await context.bot.get_chat_administrators(chat.id)
    admin_ids = {admin.user.id for admin in chat_admins}

    if user.id not in admin_ids:
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text="You need to be an admin to add me to a group."
            )
        except Exception:
            logging.warning(f"Couldn't send DM to {user.id}.")
        await context.bot.leave_chat(chat.id)
        return

    
    bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
    if bot_member.status not in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER}:
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text="I need to be made an admin in the group to function properly."
            )
        except Exception:
            logging.warning(f"Couldn't send DM to {user.id}.")
        await context.bot.leave_chat(chat.id)
        return

    add_group_to_database(chat.id, chat.title, user.id)
    await context.bot.send_message(chat.id, "Successfully added to the group!")
    logging.info(f"Bot added successfully to '{chat.title}' by {user.id}")

async def start(update: Update, context: CallbackContext):
    """Basic start command."""
    await update.message.reply_text("Hello! I am your bot.")
