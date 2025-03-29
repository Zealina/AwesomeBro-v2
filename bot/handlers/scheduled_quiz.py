from telegram import Update, Poll
from telegram.ext import CallbackContext, CommandHandler
import asyncio

# Simulated database for storing scheduled quizzes
SCHEDULED_QUIZZES = {}  # {group_id: {"time": timestamp, "questions": [list]}}

async def send_quiz(update: Update, context: CallbackContext):
    """Send the scheduled quiz as Telegram Polls with quiz mode enabled."""
    group_id = update.effective_chat.id
    
    # Check if the group has a scheduled quiz
    if group_id not in SCHEDULED_QUIZZES or not SCHEDULED_QUIZZES[group_id]["questions"]:
        await update.message.reply_text("No scheduled quiz found for this group.")
        return

    questions = SCHEDULED_QUIZZES[group_id]["questions"]
    
    for question in questions:
        # Extract question details
        q_text = question["question"]
        options = question["options"]
        correct_index = question["correct_index"]
        
        # Send as a quiz (correct answer is revealed after selection)
        await update.message.chat.send_poll(
            question=q_text,
            options=options,
            type=Poll.QUIZ,
            correct_option_id=correct_index,
            explanation="Answer will be shown after you select.",
            is_anonymous=False
        )

        await asyncio.sleep(5)  # Prevent flood restrictions

async def schedule_quiz(update: Update, context: CallbackContext):
    """Schedule a quiz for a group (admins only)."""
    group_id = update.effective_chat.id

    # Load preset quiz or generate from the pool
    quiz_questions = load_preset_quiz(group_id) or generate_quiz_from_pool(group_id)
    
    if not quiz_questions:
        await update.message.reply_text("No questions available to schedule.")
        return
    
    # Store in the scheduled quizzes database
    SCHEDULED_QUIZZES[group_id] = {
        "time": "Every 1 week",  # Default scheduling (can be modified)
        "questions": quiz_questions
    }
    
    await update.message.reply_text("Quiz has been scheduled successfully!")

async def cancel_quiz(update: Update, context: CallbackContext):
    """Cancel a scheduled quiz (admins only)."""
    group_id = update.effective_chat.id
    
    if group_id in SCHEDULED_QUIZZES:
        del SCHEDULED_QUIZZES[group_id]
        await update.message.reply_text("Scheduled quiz has been canceled.")
    else:
        await update.message.reply_text("No quiz was scheduled for this group.")

def load_preset_quiz(group_id):
    """Simulated function to load preset quiz (replace with actual file loading)."""
    return None  # Placeholder: Load from file in real implementation

def generate_quiz_from_pool(group_id):
    """Simulated function to generate quiz questions from the pool."""
    return [
        {
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "correct_index": 2
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "correct_index": 1
        }
    ]  # Placeholder data

# Handlers
schedule_quiz_handler = CommandHandler("schedule_quiz", schedule_quiz)
send_quiz_handler = CommandHandler("start_quiz", send_quiz)
cancel_quiz_handler = CommandHandler("cancel_quiz", cancel_quiz)
