"""Prompt optimization module."""

import json
from typing import Dict, List, Optional
from pathlib import Path


class PromptOptimizer:
    """Optimizes prompts based on feedback."""

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.optimization_history: List[Dict] = []

    def optimize_prompt(
        self,
        skill_name: str,
        current_prompt: str,
        feedback: List[Dict],
        strategy: str = "auto"
    ) -> str:
        """Optimize a prompt based on feedback."""
        if not feedback:
            return current_prompt

        # Analyze feedback patterns
        issues = self._analyze_feedback(feedback)

        # Apply optimization strategies
        optimized_prompt = current_prompt

        if strategy == "auto" or strategy == "clarity":
            optimized_prompt = self._improve_clarity(optimized_prompt, issues)

        if strategy == "auto" or strategy == "examples":
            optimized_prompt = self._add_examples(optimized_prompt, feedback)

        if strategy == "auto" or strategy == "structure":
            optimized_prompt = self._improve_structure(optimized_prompt)

        # Record optimization
        self.optimization_history.append({
            "skill_name": skill_name,
            "strategy": strategy,
            "issues_addressed": issues,
            "timestamp": self._get_timestamp(),
        })

        return optimized_prompt

    def _analyze_feedback(self, feedback: List[Dict]) -> Dict:
        """Analyze feedback to identify issues."""
        issues = {
            "unclear": 0,
            "incomplete": 0,
            "incorrect": 0,
            "slow": 0,
        }

        for item in feedback:
            rating = item.get("rating", 3)
            comment = item.get("comment", "").lower()

            if rating < 3:
                if "unclear" in comment or "confusing" in comment:
                    issues["unclear"] += 1
                if "incomplete" in comment or "missing" in comment:
                    issues["incomplete"] += 1
                if "wrong" in comment or "incorrect" in comment:
                    issues["incorrect"] += 1
                if "slow" in comment or "timeout" in comment:
                    issues["slow"] += 1

        return issues

    def _improve_clarity(self, prompt: str, issues: Dict) -> str:
        """Improve prompt clarity."""
        if issues["unclear"] > 0:
            # Add clearer instructions
            if "Instructions:" not in prompt:
                prompt = "Instructions:\n" + prompt

            # Add formatting guidance
            if "Format your response" not in prompt:
                prompt += "\n\nFormat your response clearly with appropriate sections."

        return prompt

    def _add_examples(self, prompt: str, feedback: List[Dict]) -> str:
        """Add examples based on good feedback."""
        good_examples = [
            item for item in feedback
            if item.get("rating", 3) >= 4 and item.get("output")
        ]

        if good_examples and "Example:" not in prompt:
            example = good_examples[0]["output"][:500]  # Limit example length
            prompt += f"\n\nExample output:\n{example}"

        return prompt

    def _improve_structure(self, prompt: str) -> str:
        """Improve prompt structure."""
        # Ensure prompt has clear sections
        sections = ["Context:", "Task:", "Requirements:", "Output:"]

        for section in sections:
            if section not in prompt:
                prompt += f"\n\n{section}\n[To be filled]"

        return prompt

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_optimization_history(self, skill_name: Optional[str] = None) -> List[Dict]:
        """Get optimization history."""
        if skill_name:
            return [h for h in self.optimization_history if h["skill_name"] == skill_name]
        return self.optimization_history
