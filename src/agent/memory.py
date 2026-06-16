from langchain.memory import ConversationBufferWindowMemory


class PostgresConversationMemory(ConversationBufferWindowMemory):
    def __init__(self, user_id: str, supabase, k: int = 10):
        self.user_id = user_id
        self.supabase = supabase
        super().__init__(memory_key="chat_history", k=k, return_messages=True)
        self._load_history()

    def _load_history(self):
        result = (
            self.supabase.table("conversaciones")
            .select("*")
            .eq("telegram_user_id", self.user_id)
            .order("fecha", desc=True)
            .limit(self.k)
            .execute()
        )
        for row in reversed(result.data):
            self.chat_memory.add_user_message(row["mensaje_usuario"])
            respuesta = row.get("respuesta_sistema") or ""
            if respuesta:
                self.chat_memory.add_ai_message(respuesta)

    def save_context(self, inputs: dict, outputs: dict) -> None:
        super().save_context(inputs, outputs)
        user_msg = inputs.get("input", "")
        ai_msg = outputs.get("output", "")
        data = {
            "telegram_user_id": self.user_id,
            "mensaje_usuario": user_msg,
            "respuesta_sistema": ai_msg,
            "tipo_entrada": "texto",
        }
        self.supabase.table("conversaciones").insert(data).execute()
