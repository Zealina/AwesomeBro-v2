"""Quiz pool"""

from telegram import Update, Document
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
import json
import time
import os

# Placeholder function for parsing TXT to JSON
def parse_txt_to_json(file_path):
    # TODO: Implement this later
    return []

# Function to store questions
def store_questions(group_id, topic, questions):
    folder = f"quiz_data/{group_id}"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/{topic}.json"

    # Load existing questions if the topic file exists
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_questions = json.load(f)
    else:
        existing_questions = []

    # Add new questions
    existing_questions.extend(questions)

    # Save back to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_questions, f, indent=4)

# Function to process uploaded files
def handle_file_upload(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.message.chat_id
    file = update.message.document

    # Ensure user has a selected group
    selected_group = context.user_data.get("selected_group")
    if not selected_group:
        update.message.reply_text("⚠️ Please select a group first using /select_group")
        return

    # Download file
    file_path = f"temp/{file.file_id}"
    file.get_file().download(file_path)

    # Determine file type
    if file.file_name.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                update.message.reply_text("⚠️ Invalid JSON file!")
                return
    elif file.file_name.endswith(".txt"):
        data = parse_txt_to_json(file_path)
    else:
        update.message.reply_text("⚠️ Unsupported file type! Use .txt or .json")
        return

    # Process the uploaded questions
    for topic, questions in data.items():
        store_questions(selected_group, topic, questions)

        # Delay between questions
        for question in questions:
            time.sleep(5)

    update.message.reply_text("✅ Questions added successfully!")

# Register handler
file_handler = MessageHandler(Filters.document, handle_file_upload)


