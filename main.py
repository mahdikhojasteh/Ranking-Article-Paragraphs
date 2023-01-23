from fastapi import FastAPI
from api import articles


app = FastAPI(
    title="TL;DR",
	description="Prioritize News Article paragraphs",
	version="0.0.1",
	contact={
		"name":"mahdi khojasteh",
		"email":"s.mahdikhojasteh@gmail.com",
	},
	license_info={
		"name":"MIT",
	},
)

app.include_router(articles.router)

