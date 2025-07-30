from fastapi import FastAPI
from index.api.routers import invest, qa_pdf, budget, chat, general, user

app = FastAPI()

app.include_router(user.router)
app.include_router(general.router)
app.include_router(invest.router)
app.include_router(qa_pdf.router)
app.include_router(budget.router)
app.include_router(chat.router)
