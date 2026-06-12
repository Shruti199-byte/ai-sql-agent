import asyncio
import os
from typing import Type

import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, inspect, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise EnvironmentError(
        "DATABASE_URL is not set. "
        "Create a .env file with DATABASE_URL=postgresql+psycopg2://..."
    )

engine = create_engine(DATABASE_URL)



class ListTablesInput(BaseModel):
    pass


class ListTablesTool(BaseTool):
    name: str = "list_tables"

    description: str = (
        "Lists all table names available in the database. "
        "Always call this first before writing any SQL, "
        "so you know which tables exist."
    )

    args_schema: Type[BaseModel] = ListTablesInput

    def _run(self) -> str:
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if not tables:
            return "No tables found in the database."

        result = ", ".join(tables)
        print(f"[list_tables] Found tables: {result}")
        return result

    async def _arun(self) -> str:
        return await asyncio.to_thread(self._run)


class GetSchemaInput(BaseModel):
    table_name: str = Field(
        description="The exact name of the table whose schema you want to inspect."
    )


class GetSchemaTool(BaseTool):
    name: str = "get_schema"

    description: str = (
        "Returns all column names and their data types for a given table. "
        "Use this to understand the table structure before writing SQL."
    )

    args_schema: Type[BaseModel] = GetSchemaInput

    def _run(self, table_name: str) -> str:
        inspector = inspect(engine)

        available_tables = inspector.get_table_names()

        if table_name not in available_tables:
            return (
                f"Error: Table '{table_name}' does not exist. "
                f"Available tables: {', '.join(available_tables)}"
            )

        columns = inspector.get_columns(table_name)

        lines = [f"Schema for table '{table_name}':"]

        for col in columns:
            lines.append(f"  - {col['name']}  ({col['type']})")

        result = "\n".join(lines)

        print(f"[get_schema] {result}")

        return result

    async def _arun(self, table_name: str) -> str:
        return await asyncio.to_thread(self._run, table_name)


class ValidateQueryInput(BaseModel):
    query: str = Field(
        description="The SQL query string to validate before executing."
    )


class ValidateQueryTool(BaseTool):
    name: str = "validate_query"

    description: str = (
        "Validates a SQL query by running EXPLAIN on PostgreSQL. "
        "No data is read or changed. Use this before execute_query "
        "to catch syntax errors early."
    )

    args_schema: Type[BaseModel] = ValidateQueryInput

    def _run(self, query: str) -> str:
        with engine.connect() as conn:
            try:
                conn.execute(text(f"EXPLAIN {query}"))
                print("[validate_query] Query is valid.")
                return "Valid: The query is syntactically correct and can be executed."

            except Exception as e:
                error_msg = f"Invalid query: {str(e)}"
                print(f"[validate_query] {error_msg}")
                return error_msg

    async def _arun(self, query: str) -> str:
        return await asyncio.to_thread(self._run, query)


class ExecuteQueryInput(BaseModel):
    query: str = Field(
        description="A valid SQL SELECT query to execute against the database."
    )


class ExecuteQueryTool(BaseTool):
    name: str = "execute_query"

    description: str = (
        "Executes a SQL SELECT query against the database and returns the results. "
        "Only SELECT queries are permitted. "
        "Validate the query with validate_query before calling this."
    )

    args_schema: Type[BaseModel] = ExecuteQueryInput


    response_format: str = "content_and_artifact"   

    def _run(self, query: str) -> tuple[str, pd.DataFrame | None]:
        first_word = query.strip().split()[0].upper()
        if first_word != "SELECT":
            return (
                f"Error: Only SELECT queries are allowed. "
                f"Received a '{first_word}' statement.",
                None,                                # ← no artifact on error
            )
        
        with engine.connect() as conn:
            try:
                result = conn.execute(text(query))
                rows = result.fetchall()
                column_names = list(result.keys())

                if not rows:
                    print("[execute_query] Query returned no rows.")
                    return ("The query executed successfully but returned no rows.", None)
                
                df = pd.DataFrame(rows, columns=column_names)
                output = df.to_string(index=False)

                print(f"[execute_query] Returned {len(rows)} row(s).")
                return (output, df)          
                    
            except Exception as e:
                error_msg = f"Error executing query: {str(e)}"
                print(f"[execute_query] {error_msg}")
                return (error_msg, None)
            
    async def _arun(self, query: str) -> tuple[str, pd.DataFrame | None]:
        return await asyncio.to_thread(self._run, query)