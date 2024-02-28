from ariadne import gql, make_executable_schema
from .resolvers import query, mutation

type_defs = gql("""
                
    input CreateUserInput {
        username: String!
        full_name: String!
    }
                
    input UpdateUserInput {
        username: String
        full_name: String
    }
                
    type Query {
        getUser(user_id: Int!): User
        getAllUsers: [User!]!
    }

    type Mutation {
        createUser(user_data: CreateUserInput): User
        updateUser(user_id: Int!, user_data: UpdateUserInput): User
        deleteUser(user_id: Int!): StatusResponse
    }

    type User {
        id: Int!
        username: String!
        full_name: String!
        registered_at: String!
    }

    type StatusResponse {
        status: String!
        data: String
    }
""")


schema = make_executable_schema(type_defs, query, mutation)
