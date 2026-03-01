"""Feedback processing module."""

import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class FeedbackProcessor:
    """Processes and analyzes feedback."""

    def __init__(self, feedback_dir: str = "feedback"):
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(exist_ok=True)
        self.feedback_cache: Dict[str, List[Dict]] = {}

    def record_feedback(
        self,
        skill_name: str,
        rating: int,
        comment: Optional[str] = None,
        output: Optional[str] = None,
        execution_time: Optional[float] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Record user feedback."""
        feedback = {
            "skill_name": skill_name,
            "rating": rating,
            "comment": comment,
            "output": output,
            "execution_time": execution_time,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }

        # Save to file
        feedback_file = self.feedback_dir / f"{skill_name}.json"
        existing = []
        if feedback_file.exists():
            with open(feedback_file, "r") as f:
                existing = json.load(f)

        existing.append(feedback)

        with open(feedback_file, "w") as f:
            json.dump(existing, f, indent=2)

        # Update cache
        if skill_name not in self.feedback_cache:
            self.feedback_cache[skill_name] = []
        self.feedback_cache[skill_name].append(feedback)

        return feedback

    def get_feedback(
        self,
        skill_name: Optional[str] = None,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get feedback with optional filters."""
        if skill_name:
            feedback_list = self._load_feedback(skill_name)
        else:
            feedback_list = []
            for file in self.feedback_dir.glob("*.json"):
                feedback_list.extend(self._load_feedback(file.stem))

        # Apply filters
        if min_rating is not None:
            feedback_list = [f for f in feedback_list if f["rating"] >= min_rating]
        if max_rating is not None:
            feedback_list = [f for f in feedback_list if f["rating"] <= max_rating]

        # Sort by timestamp (newest first)
        feedback_list.sort(key=lambda x: x["timestamp"], reverse=True)

        return feedback_list[:limit]

    def _load_feedback(self, skill_name: str) -> List[Dict]:
        """Load feedback from file."""
        if skill_name in self.feedback_cache:
            return self.feedback_cache[skill_name]

        feedback_file = self.feedback_dir / f"{skill_name}.json"
        if not feedback_file.exists():
            return []

        with open(feedback_file, "r") as f:
            feedback = json.load(f)

        self.feedback_cache[skill_name] = feedback
        return feedback

    def analyze_feedback(self, skill_name: str) -> Dict:
        """Analyze feedback for a skill."""
        feedback_list = self._load_feedback(skill_name)

        if not feedback_list:
            return {
                "skill_name": skill_name,
                "total_feedback": 0,
                "average_rating": 0,
                "improvement_needed": False
            }

        ratings = [f["rating"] for f in feedback_list]
        avg_rating = sum(ratings) / len(ratings)

        # Count issues
        issues = {"unclear": 0, "incomplete": 0, "incorrect": 0, "slow": 0}
        for f in feedback_list:
            comment = f.get("comment", "").lower()
            if "unclear" in comment or "confusing" in comment:
                issues["unclear"] += 1
            if "incomplete" in comment or "missing" in comment:
                issues["incomplete"] += 1
            if "wrong" in comment or "incorrect" in comment:
                issues["incorrect"] += 1
            if "slow" in comment or "timeout" in comment:
                issues["slow"] += 1

        return {
            "skill_name": skill_name,
            "total_feedback": len(feedback_list),
            "average_rating": round(avg_rating, 2),
            "rating_distribution": {
                "5": ratings.count(5),
                "4": ratings.count(4),
                "3": ratings.count(3),
                "2": ratings.count(2),
                "1": ratings.count(1),
            },
            "issues": issues,
            "improvement_needed": avg_rating < 3.5 or any(c > 2 for c in issues.values())
        }

    def get_improvement_suggestions(self, skill_name: str) -> List[str]:
        """Get improvement suggestions based on feedback."""
        analysis = self.analyze_feedback(skill_name)
        suggestions = []

        if analysis["average_rating"] < 3.5:
            suggestions.append("Overall quality needs improvement. Consider reviewing the prompt and examples.")

        issues = analysis.get("issues", {})
        if issues.get("unclear", 0) > 2:
            suggestions.append("Users report the skill is unclear. Add more specific instructions and examples.")
        if issues.get("incomplete", 0) > 2:
            suggestions.append("Output is often incomplete. Consider increasing max_tokens or improving prompt structure.")
        if issues.get("incorrect", 0) > 2:
            suggestions.append("Results are sometimes incorrect. Review the prompt for accuracy requirements.")
        if issues.get("slow", 0) > 2:
            suggestions.append("Execution is too slow. Consider using a faster model or optimizing the prompt.")

        return suggestions
