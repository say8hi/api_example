from fastapi import FastAPI
from ariadne.asgi import GraphQL

from api.graphql.schema import schema

app = FastAPI()

graphql_app = GraphQL(schema, debug=True)

app.mount("/graphql", graphql_app)