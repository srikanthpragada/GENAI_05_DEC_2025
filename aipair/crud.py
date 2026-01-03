import sqlite3
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_connection(db_path: str = "courses.sqlite") -> sqlite3.Connection:
	"""Return a sqlite3 connection and ensure the `COURSES` table exists.

	Args:
		db_path: Path to the SQLite database file.

	Returns:
		sqlite3.Connection: open connection to the database.

	Raises:
		RuntimeError: if the database cannot be opened or table cannot be created.
	"""
	try:
		conn = sqlite3.connect(db_path)
		conn.row_factory = sqlite3.Row
		_ensure_table_exists(conn)
		return conn
	except sqlite3.Error as e:
		logger.exception("Failed to open database or ensure table exists")
		raise RuntimeError(f"Database error: {e}")


def _ensure_table_exists(conn: sqlite3.Connection) -> None:
	"""Create the `COURSES` table if it does not already exist.

	The expected schema: id (INTEGER PRIMARY KEY), title (TEXT), duration (INTEGER), fee (REAL)
	"""
	try:
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS COURSES (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT NOT NULL,
				duration INTEGER NOT NULL,
				fee REAL NOT NULL
			)
			"""
		)
		conn.commit()
	except sqlite3.Error:
		logger.exception("Failed to create COURSES table")
		raise


def create_course(title: str, duration: int, fee: float, db_path: str = "courses.sqlite") -> int:
	"""Insert a new course into the `COURSES` table.

	Args:
		title: Course title (non-empty string).
		duration: Course duration (integer, e.g., hours or weeks).
		fee: Course fee (float).
		db_path: Path to the SQLite database file.

	Returns:
		The newly created course `id`.

	Raises:
		ValueError: if input validation fails.
		RuntimeError: if a database error occurs.
	"""
	if not title or not isinstance(title, str):
		raise ValueError("title must be a non-empty string")
	if not isinstance(duration, int) or duration < 0:
		raise ValueError("duration must be a non-negative integer")
	if not isinstance(fee, (int, float)) or fee < 0:
		raise ValueError("fee must be a non-negative number")

	try:
		conn = _get_connection(db_path)
		with conn:
			cur = conn.execute(
				"INSERT INTO COURSES (title, duration, fee) VALUES (?, ?, ?)",
				(title, duration, float(fee)),
			)
			new_id = cur.lastrowid
			logger.info("Created course id=%s title=%s", new_id, title)
			return new_id
	except sqlite3.Error as e:
		logger.exception("Failed to create course")
		raise RuntimeError(f"Failed to create course: {e}")


def get_course(course_id: int, db_path: str = "courses.sqlite") -> Optional[Dict[str, Any]]:
	"""Retrieve a course by `id`.

	Args:
		course_id: The id of the course to fetch.
		db_path: Path to the SQLite database file.

	Returns:
		A dict with keys `id`, `title`, `duration`, `fee` or None if not found.

	Raises:
		ValueError: if `course_id` is invalid.
		RuntimeError: if a database error occurs.
	"""
	if not isinstance(course_id, int) or course_id < 1:
		raise ValueError("course_id must be a positive integer")
	try:
		conn = _get_connection(db_path)
		cur = conn.execute("SELECT id, title, duration, fee FROM COURSES WHERE id = ?", (course_id,))
		row = cur.fetchone()
		if row is None:
			return None
		return dict(row)
	except sqlite3.Error as e:
		logger.exception("Failed to get course id=%s", course_id)
		raise RuntimeError(f"Failed to get course: {e}")


def update_course(course_id: int, title: Optional[str] = None, duration: Optional[int] = None, fee: Optional[float] = None, db_path: str = "courses.sqlite") -> bool:
	"""Update fields of an existing course.

	Args:
		course_id: ID of the course to update.
		title: New title (optional).
		duration: New duration (optional).
		fee: New fee (optional).
		db_path: Path to the SQLite database file.

	Returns:
		True if a row was updated, False if no row matched `course_id`.

	Raises:
		ValueError: if inputs are invalid or no fields provided.
		RuntimeError: if a database error occurs.
	"""
	if not isinstance(course_id, int) or course_id < 1:
		raise ValueError("course_id must be a positive integer")

	fields = []
	params: List[Any] = []
	if title is not None:
		if not title:
			raise ValueError("title must be a non-empty string")
		fields.append("title = ?")
		params.append(title)
	if duration is not None:
		if not isinstance(duration, int) or duration < 0:
			raise ValueError("duration must be a non-negative integer")
		fields.append("duration = ?")
		params.append(duration)
	if fee is not None:
		if not isinstance(fee, (int, float)) or fee < 0:
			raise ValueError("fee must be a non-negative number")
		fields.append("fee = ?")
		params.append(float(fee))

	if not fields:
		raise ValueError("At least one field (title, duration, fee) must be provided to update")

	params.append(course_id)
	sql = f"UPDATE COURSES SET {', '.join(fields)} WHERE id = ?"
	try:
		conn = _get_connection(db_path)
		with conn:
			cur = conn.execute(sql, tuple(params))
			updated = cur.rowcount > 0
			logger.info("Update course id=%s updated=%s", course_id, updated)
			return updated
	except sqlite3.Error as e:
		logger.exception("Failed to update course id=%s", course_id)
		raise RuntimeError(f"Failed to update course: {e}")


def delete_course(course_id: int, db_path: str = "courses.sqlite") -> bool:
	"""Delete a course by `id`.

	Args:
		course_id: ID of the course to delete.
		db_path: Path to the SQLite database file.

	Returns:
		True if a row was deleted, False if no row matched `course_id`.

	Raises:
		ValueError: if `course_id` is invalid.
		RuntimeError: if a database error occurs.
	"""
	if not isinstance(course_id, int) or course_id < 1:
		raise ValueError("course_id must be a positive integer")
	try:
		conn = _get_connection(db_path)
		with conn:
			cur = conn.execute("DELETE FROM COURSES WHERE id = ?", (course_id,))
			deleted = cur.rowcount > 0
			logger.info("Delete course id=%s deleted=%s", course_id, deleted)
			return deleted
	except sqlite3.Error as e:
		logger.exception("Failed to delete course id=%s", course_id)
		raise RuntimeError(f"Failed to delete course: {e}")


def list_courses(db_path: str = "courses.sqlite") -> List[Dict[str, Any]]:
	"""Return all courses ordered by `id`.

	Args:
		db_path: Path to the SQLite database file.

	Returns:
		A list of dicts, each containing `id`, `title`, `duration`, `fee`.

	Raises:
		RuntimeError: if a database error occurs.
	"""
	try:
		conn = _get_connection(db_path)
		cur = conn.execute("SELECT id, title, duration, fee FROM COURSES ORDER BY id")
		rows = cur.fetchall()
		return [dict(r) for r in rows]
	except sqlite3.Error as e:
		logger.exception("Failed to list courses")
		raise RuntimeError(f"Failed to list courses: {e}")


if __name__ == "__main__":
	# Simple demonstration when run as a script
	try:
		print("Creating sample course...")
		cid = create_course("Intro to AI", 10, 199.99)
		print("Created id:", cid)
		print("All courses:")
		for c in list_courses():
			print(c)
	except Exception as exc:
		print("Error during demo:", exc)
