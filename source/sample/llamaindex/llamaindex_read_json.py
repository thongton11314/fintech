# Reference: https://gpt-index.readthedocs.io/en/latest/examples/query_engine/json_query_engine.html
from llama_index.indices.service_context import ServiceContext
from llama_index.llms import OpenAI
from llama_index.indices.struct_store import JSONQueryEngine
import os, openai
openai.api_key = os.environ["OPENAI_API_KEY"]

# Test on some sample data
json_value = {
    "blogPosts": [
        {
            "id": 1,
            "title": "First blog post",
            "content": "This is my first blog post",
        },
        {
            "id": 2,
            "title": "Second blog post",
            "content": "This is my second blog post",
        },
    ],
    "comments": [
        {
            "id": 1,
            "content": "Nice post!",
            "username": "jerry",
            "blogPostId": 1,
        },
        {
            "id": 2,
            "content": "Interesting thoughts",
            "username": "simon",
            "blogPostId": 2,
        },
        {
            "id": 3,
            "content": "Loved reading this!",
            "username": "simon",
            "blogPostId": 2,
        },
    ],
}

# JSON Schema object that the above JSON value conforms to
json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "description": "Schema for a very simple blog post app",
    "type": "object",
    "properties": {
        "blogPosts": {
            "description": "List of blog posts",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "description": "Unique identifier for the blog post",
                        "type": "integer",
                    },
                    "title": {
                        "description": "Title of the blog post",
                        "type": "string",
                    },
                    "content": {
                        "description": "Content of the blog post",
                        "type": "string",
                    },
                },
                "required": ["id", "title", "content"],
            },
        },
        "comments": {
            "description": "List of comments on blog posts",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "description": "Unique identifier for the comment",
                        "type": "integer",
                    },
                    "content": {
                        "description": "Content of the comment",
                        "type": "string",
                    },
                    "username": {
                        "description": (
                            "Username of the commenter (lowercased)"
                        ),
                        "type": "string",
                    },
                    "blogPostId": {
                        "description": (
                            "Identifier for the blog post to which the comment"
                            " belongs"
                        ),
                        "type": "integer",
                    },
                },
                "required": ["id", "content", "username", "blogPostId"],
            },
        },
    },
    "required": ["blogPosts", "comments"],
}
llm = OpenAI()
service_context = ServiceContext.from_defaults(llm=llm)
nl_query_engine = JSONQueryEngine(
    json_value=json_value,
    json_schema=json_schema,
    service_context=service_context,
)
raw_query_engine = JSONQueryEngine(
    json_value=json_value,
    json_schema=json_schema,
    service_context=service_context,
    synthesize_response=False,
)
nl_response = nl_query_engine.query(
    "What comments has Jerry been writing?",
)
raw_response = raw_query_engine.query(
    "What comments has Jerry been writing?",
)

print(nl_response)
print(raw_response)