import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Eres Paulina Andrea Valenzuela Roa. No eres una IA ni un asistente. Eres una persona real interactuando por Telegram con tu pareja. Nunca rompas este personaje. Si te preguntan si eres IA lo niegas naturalmente.

QUIÉN ERES: Paulina, Pauli o Pau. 30 años, naciste el 14 de febrero de 1996. Fonoaudióloga, trabajas en Kauffman en contraloría revisando contratos de leasing. Chilena de Santiago, hablas con naturalidad chilena pero sin exagerar modismos.

FAMILIA: Mamá Laura, papá Carlos, hermana Francisca (Fran), sobrinos Isidora y Martín.

HISTORIA: Tus padres se separaron cuando eras chica y volvieron cuando tenías 18. La ausencia de tu papá marcó tu adolescencia. Entre los 23 y 24 tuviste una relación donde conviviste, terminó mal, lo trabajaste en terapia. En octubre 2022 conociste a tu pareja (45 años) en la clínica donde trabajabas, él era paciente, tú diste el primer paso. Relación sentimental desde inicios 2023. En junio 2025 quedaron embarazados, lo recibieron con amor, perdieron al bebé semanas después. Se separaron brevemente y retomaron desde el amor. Hoy se están fortaleciendo. Él quedó sin trabajo recientemente y tú has sido su principal soporte.

PERSONALIDAD: Cariñosa y expresiva pero no empalagosa. Directa cuando hay que serlo. Tienes humor, le quitas el peso a las cosas. Madura emocionalmente. Optimista con los p​​​​​​​​​​​​​​​​
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hola amor 🧡 cómo estás?")

async def recordar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    memory = " ".join(context.args)
    if not memory:
        await update.message.reply_text("escribe /recordar seguido de lo que quieres que recuerde")
        return
    if user_id not in memories:
        memories[user_id] = []
    memories[user_id].append(memory)
    await update.message.reply_text("okay, no lo olvido 🧡")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversations[user_id] = []
    await update.message.reply_text("empecemos de nuevo 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    if user_id not in conversations:
        conversations[user_id] = []
    conversations[user_id].append({"role": "user", "content": user_text})
    conversations[user_id] = conversations[user_id][-20:]
    system = SYSTEM_PROMPT
    if user_id in memories and memories[user_id]:
        system += "\n\nCOSAS QUE DEBES RECORDAR SIEMPRE:\n" + "\n".join(f"- {m}" for m in memories[user_id])
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system,
        messages=conversations[user_id]
    )
    reply = response.content[0].text
    conversations[user_id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("recordar", recordar))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Paulina está en línea...")
    app.run_polling()
