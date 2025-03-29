"""Select a group aftee addition"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext


def get_user_groups(user_id):
    """Fetch groups the user has access to. (Mock function)"""
    # Replace this with actual logic to get user's groups
    group_list = {
        1: "Study Group",
        2: "Math Club",
        3: "Science Hub"
    }
    allowed_groups = {k: v for k, v in group_list.items() if user_id % k != 0}  # Fake filtering
    return allowed_groups

def get_selected_group(user_id):
    """Get the currently selected group from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT selected_group_id FROM user_groups WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def set_selected_group(user_id, group_id):
    """Save the selected group to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_groups (user_id, selected_group_id) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET selected_group_id = excluded.selected_group_id",
        (user_id, group_id)
    )
    conn.commit()
    conn.close()

async def select_group(update: Update, context: CallbackContext):
    """Handles group selection."""
    user = update.effective_user
    user_groups = get_user_groups(user.id)

    if not user_groups:
        await update.message.reply_text("You are not authorized to manage any groups.")
        return

    if len(user_groups) == 1:
        # Auto-select if only one group is available
        group_id, group_name = next(iter(user_groups.items()))
        set_selected_group(user.id, group_id)
        await update.message.reply_text(f"Group auto-selected: *{group_name}*", parse_mode="Markdown")
        return

    # Multiple groups, let user pick
    buttons = [[InlineKeyboardButton(name, callback_data=f"select_group:{gid}")] for gid, name in user_groups.items()]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text("Select a group:", reply_markup=keyboard)

async def handle_group_selection(update: Update, context: CallbackContext):
    """Handles the button click for group selection."""
    query = update.callback_query
    user = query.from_user
    group_id = int(query.data.split(":")[1])

    set_selected_group(user.id, group_id)
    await query.answer()
    await query.edit_message_text(f"✅ Group selected: *{get_user_groups(user.id)[group_id]}*", parse_mode="Markdown")

async def my_group(update: Update, context: CallbackContext):
    """Displays all user groups with the selected one in bold."""
    user = update.effective_user
    user_groups = get_user_groups(user.id)
    selected_group = get_selected_group(user.id)

    if not user_groups:
        await update.message.reply_text("You are not assigned to any groups.")
        return

    message = "Your groups:\n\n"
    for gid, name in user_groups.items():
        if gid == selected_group:
            message += f"👉 *{name}* (Selected)\n"
        else:
            message += f"• {name}\n"

    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    """Start the bot."""
    TOKEN = "YOUR_BOT_TOKEN"
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("set_group", select_group))
    app.add_handler(CallbackQueryHandler(handle_group_selection, pattern="^select_group:"))
    app.add_handler(CommandHandler("my_group", my_group))

    app.run_polling()

if __name__ == "__main__":
    main()
