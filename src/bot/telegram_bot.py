import asyncio
import traceback
from concurrent.futures import ThreadPoolExecutor

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from src.config import Config
from src.agent.agent import get_agent_for_user

_executor = ThreadPoolExecutor(max_workers=4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Bienvenido a ReProyecta*\n\n"
        "Soy un asistente de gestión de recursos.\n\n"
        "*Comandos disponibles:*\n"
        "📝 *Registrar*: \"Guardar 10 motores DC\"\n"
        "🔍 *Consultar*: \"¿Cuántos motores tenemos?\"\n"
        "📋 *Inventario*: \"Muéstrame todo el inventario\"\n"
        "🏗️ *Planificar*: \"Quiero construir un brazo robótico\"\n"
        "📁 *Proyectos*: \"Ver proyectos anteriores\"",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*Ayuda de ReProyecta*\n\n"
        "Puedes interactuar con lenguaje natural.\n\n"
        "*Ejemplos:*\n"
        "- \"Registrar 20 sensores ultrasónicos\"\n"
        "- \"¿Hay motores disponibles?\"\n"
        "- \"Agregar 5 baterías LiPo al inventario\"\n"
        "- \"¿Qué proyectos tenemos?\"\n"
        "- \"Necesito desarrollar un rover\"",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_message = update.message.text.strip()

    if not user_message:
        return

    await update.message.chat.send_action("typing")

    try:
        agent = get_agent_for_user(user_id)
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(_executor, agent.run, user_message)
        await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        print(f"\n❌ ERROR en handle_message (user={user_id}):")
        traceback.print_exc()
        error_msg = (
            "Ocurrió un error al procesar tu solicitud. "
            "Por favor intenta nuevamente."
        )
        await update.message.reply_text(error_msg)


def run_bot():
    Config.validate()

    application = (
        Application.builder()
        .token(Config.TELEGRAM_BOT_TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Bot ReProyecta en ejecución...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
