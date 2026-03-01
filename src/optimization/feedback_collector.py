"""Feedback collection system."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel


class Feedback(BaseModel):
    """Feedback model."""
    skill_name: str
    execution_id: str
    rating: int  # 1 or -1
    comment: Optional[str] = None
    context: Optional[Dict] = None
    created_at: str = ""

    def __init__(self, **data):
        if not data.get("created_at"):
            data["created_at"] = datetime.now().isoformat()
        super().__init__(**data)


class FeedbackCollector:
    """Collects and manages user feedback."""

    def __init__(self, db_path: str = "feedback.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    execution_id TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    comment TEXT,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_skill_name ON feedback(skill_name)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_execution_id ON feedback(execution_id)
            """)

    def submit_feedback(self, feedback: Feedback) -> int:
        """Submit feedback to database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO feedback (skill_name, execution_id, rating, comment, context, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    feedback.skill_name,
                    feedback.execution_id,
                    feedback.rating,
                    feedback.comment,
                    json.dumps(feedback.context) if feedback.context else None,
                    feedback.created_at,
                ),
            )
            return cursor.lastrowid

    def get_feedback_for_skill(self, skill_name: str) -> List[Feedback]:
        """Get all feedback for a skill."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM feedback WHERE skill_name = ? ORDER BY created_at DESC",
                (skill_name,),
            )
            rows = cursor.fetchall()

        feedback_list = []
        for row in rows:
            feedback_list.append(
                Feedback(
                    skill_name=row[1],
                    execution_id=row[2],
                    rating=row[3],
                    comment=row[4],
                    context=json.loads(row[5]) if row[5] else None,
                    created_at=row[6],
                )
            )
        return feedback_list

    def get_feedback_stats(self, skill_name: Optional[str] = None) -> Dict:
        """Get feedback statistics."""
        with sqlite3.connect(self.db_path) as conn:
            if skill_name:
                cursor = conn.execute(
                    """
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as positive,
                        SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as negative,
                        AVG(rating) as avg_rating
                    FROM feedback
                    WHERE skill_name = ?
                    """,
                    (skill_name,),
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as positive,
                        SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as negative,
                        AVG(rating) as avg_rating
                    FROM feedback
                    """
                )

            row = cursor.fetchone()
            return {
                "total": row[0] or 0,
                "positive": row[1] or 0,
                "negative": row[2] or 0,
                "average_rating": round(row[3], 2) if row[3] else 0,
            }
