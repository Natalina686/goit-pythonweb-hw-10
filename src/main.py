from fastapi import FastAPI
from .routes import contacts

app =  FastAPI(title="Contacts API")
app.include_router(contacts.router)
