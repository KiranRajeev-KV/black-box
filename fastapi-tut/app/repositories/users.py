import sqlite3

from app.database import db_connection
from app.dependencies import DbConnectionDep
from app.models import UserCreate, UserPatch, UserUpdate

class UserRepository:
    def row_to_user_public(self, row: sqlite3.Row) -> dict:
        return {
            "id": row["id"],
            "name": row["name"],
            "age": row["age"],
        }


    def create_user(self, user: UserCreate) -> dict:
        with db_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (name, age, password)
                VALUES (?, ?, ?)
                """,
                (user.name, user.age, user.password),
            )

            user_id = cursor.lastrowid

            row = connection.execute(
                """
                SELECT id, name, age
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()

            if row is None:
                raise RuntimeError("User was inserted but could not be fetched")

            return self.row_to_user_public(row)


    def list_users(self, connection: DbConnectionDep) -> list[dict]:
        rows = connection.execute(
            """
            SELECT id, name, age
            FROM users
            ORDER BY id
            """
        ).fetchall()

        return [self.row_to_user_public(row) for row in rows]


    def get_user_by_id(self,user_id: int) -> dict | None:
        with db_connection() as connection:
            row = connection.execute(
                """
                SELECT id, name, age
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()

            if row is None:
                return None

            return self.row_to_user_public(row)


    def update_user(self,user_id: int, user: UserUpdate) -> dict | None:
        with db_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE users
                SET name = ?, age = ?
                WHERE id = ?
                """,
                (user.name, user.age, user_id),
            )

            if cursor.rowcount == 0:
                return None

            row = connection.execute(
                """
                SELECT id, name, age
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()

            if row is None:
                return None

            return self.row_to_user_public(row)


    def patch_user(self,user_id: int, user_patch: UserPatch) -> dict | None:
        update_data = user_patch.model_dump(exclude_unset=True)

        if not update_data:
            return self.get_user_by_id(user_id)

        allowed_fields = {"name", "age"}
        invalid_fields = set(update_data) - allowed_fields

        if invalid_fields:
            raise ValueError(f"Invalid update fields: {invalid_fields}")

        set_clause = ", ".join(f"{field} = ?" for field in update_data)
        values = list(update_data.values())
        values.append(user_id)

        with db_connection() as connection:
            cursor = connection.execute(
                f"""
                UPDATE users
                SET {set_clause}
                WHERE id = ?
                """,
                values,
            )

            if cursor.rowcount == 0:
                return None

            row = connection.execute(
                """
                SELECT id, name, age
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()

            if row is None:
                return None

            return self.row_to_user_public(row)


    def delete_user(self,user_id: int) -> dict | None:
        with db_connection() as connection:
            row = connection.execute(
                """
                SELECT id, name, age
                FROM users
                WHERE id = ?
                """,
                (user_id,),
            ).fetchone()

            if row is None:
                return None

            connection.execute(
                """
                DELETE FROM users
                WHERE id = ?
                """,
                (user_id,),
            )

            return self.row_to_user_public(row)