import asyncio
import os
import sys



if len(sys.argv) < 2:
    print("Usage: python main.py [api_name]")
    sys.exit(1)

api_name = sys.argv[1]

if api_name == "rest":
    from api.rest.api import app as rest_app
    app = rest_app
# elif api_name == "graphql":
#     from api.graphql.api import app as graphql_app
#     app = graphql_app
# elif api_name == "grpc":
#     from api.grpc.api import start_grpc_server
#     start_grpc_server()
else:
    print(f"Invalid API name. Available options: rest, graphql, grpc")
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
