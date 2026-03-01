"""A/B testing module for prompt and model optimization."""

import random
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from enum import Enum


class TestStatus(Enum):
    """Test status."""
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ABTester:
    """Manages A/B tests for skills."""

    def __init__(self, tests_dir: str = "ab_tests"):
        self.tests_dir = Path(tests_dir)
        self.tests_dir.mkdir(exist_ok=True)
        self.active_tests: Dict[str, Dict] = {}

    def create_test(
        self,
        skill_name: str,
        variant_a: Dict,  # Control
        variant_b: Dict,  # Treatment
        test_name: Optional[str] = None,
        sample_size: int = 100
    ) -> str:
        """Create a new A/B test."""
        test_id = f"{skill_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        test = {
            "id": test_id,
            "name": test_name or f"A/B Test for {skill_name}",
            "skill_name": skill_name,
            "created_at": datetime.now().isoformat(),
            "status": TestStatus.RUNNING.value,
            "sample_size": sample_size,
            "variants": {
                "A": {
                    "name": "Control",
                    "config": variant_a,
                    "assignments": 0,
                    "ratings": [],
                    "avg_rating": 0
                },
                "B": {
                    "name": "Treatment",
                    "config": variant_b,
                    "assignments": 0,
                    "ratings": [],
                    "avg_rating": 0
                }
            }
        }

        # Save test
        test_file = self.tests_dir / f"{test_id}.json"
        with open(test_file, "w") as f:
            json.dump(test, f, indent=2)

        self.active_tests[test_id] = test

        return test_id

    def assign_variant(self, test_id: str) -> str:
        """Assign a variant for testing (A or B)."""
        if test_id not in self.active_tests:
            # Load from file
            test_file = self.tests_dir / f"{test_id}.json"
            if not test_file.exists():
                raise ValueError(f"Test {test_id} not found")
            with open(test_file, "r") as f:
                self.active_tests[test_id] = json.load(f)

        test = self.active_tests[test_id]

        if test["status"] != TestStatus.RUNNING.value:
            # Return control if test is not running
            return "A"

        variants = test["variants"]

        # Check if we've reached sample size
        total = variants["A"]["assignments"] + variants["B"]["assignments"]
        if total >= test["sample_size"]:
            self._complete_test(test_id)
            return "A"

        # Random assignment with balancing
        if variants["A"]["assignments"] < variants["B"]["assignments"]:
            variant = "A"
        elif variants["B"]["assignments"] < variants["A"]["assignments"]:
            variant = "B"
        else:
            variant = random.choice(["A", "B"])

        variants[variant]["assignments"] += 1
        self._save_test(test_id)

        return variant

    def record_result(
        self,
        test_id: str,
        variant: str,
        rating: int,
        metadata: Optional[Dict] = None
    ):
        """Record a test result."""
        if test_id not in self.active_tests:
            raise ValueError(f"Test {test_id} not found")

        test = self.active_tests[test_id]
        variant_data = test["variants"][variant]

        variant_data["ratings"].append({
            "rating": rating,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })

        # Update average
        ratings = [r["rating"] for r in variant_data["ratings"]]
        variant_data["avg_rating"] = sum(ratings) / len(ratings)

        self._save_test(test_id)

        # Check if test should complete
        total_ratings = sum(len(v["ratings"]) for v in test["variants"].values())
        if total_ratings >= test["sample_size"]:
            self._complete_test(test_id)

    def get_test_results(self, test_id: str) -> Dict:
        """Get test results."""
        if test_id not in self.active_tests:
            test_file = self.tests_dir / f"{test_id}.json"
            if not test_file.exists():
                raise ValueError(f"Test {test_id} not found")
            with open(test_file, "r") as f:
                test = json.load(f)
        else:
            test = self.active_tests[test_id]

        variants = test["variants"]

        # Calculate statistics
        results = {
            "test_id": test_id,
            "name": test["name"],
            "status": test["status"],
            "skill_name": test["skill_name"],
            "created_at": test["created_at"],
            "completed_at": test.get("completed_at"),
            "variants": {}
        }

        for variant_name, variant_data in variants.items():
            ratings = [r["rating"] for r in variant_data["ratings"]]
            results["variants"][variant_name] = {
                "name": variant_data["name"],
                "assignments": variant_data["assignments"],
                "ratings_count": len(ratings),
                "avg_rating": round(variant_data["avg_rating"], 2) if ratings else 0,
                "config": variant_data["config"]
            }

        # Determine winner if test is complete
        if test["status"] == TestStatus.COMPLETED.value:
            avg_a = results["variants"]["A"]["avg_rating"]
            avg_b = results["variants"]["B"]["avg_rating"]

            if avg_b > avg_a:
                results["winner"] = "B"
                results["improvement"] = round(((avg_b - avg_a) / avg_a * 100) if avg_a > 0 else 0, 2)
            elif avg_a > avg_b:
                results["winner"] = "A"
                results["improvement"] = 0
            else:
                results["winner"] = "tie"
                results["improvement"] = 0

        return results

    def list_tests(self, skill_name: Optional[str] = None) -> List[Dict]:
        """List all tests."""
        tests = []

        for test_file in self.tests_dir.glob("*.json"):
            with open(test_file, "r") as f:
                test = json.load(f)

            if skill_name is None or test["skill_name"] == skill_name:
                tests.append({
                    "id": test["id"],
                    "name": test["name"],
                    "skill_name": test["skill_name"],
                    "status": test["status"],
                    "created_at": test["created_at"]
                })

        return sorted(tests, key=lambda x: x["created_at"], reverse=True)

    def _save_test(self, test_id: str):
        """Save test to file."""
        test_file = self.tests_dir / f"{test_id}.json"
        with open(test_file, "w") as f:
            json.dump(self.active_tests[test_id], f, indent=2)

    def _complete_test(self, test_id: str):
        """Mark test as complete."""
        if test_id in self.active_tests:
            self.active_tests[test_id]["status"] = TestStatus.COMPLETED.value
            self.active_tests[test_id]["completed_at"] = datetime.now().isoformat()
            self._save_test(test_id)
