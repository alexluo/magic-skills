"""Tests for optimization modules."""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.optimization import (
    PromptOptimizer,
    ModelSelector,
    FeedbackProcessor,
    ABTester
)


class TestPromptOptimizer:
    """Tests for PromptOptimizer."""

    def test_optimize_prompt_no_feedback(self):
        """Test optimization with no feedback."""
        optimizer = PromptOptimizer()
        prompt = "Original prompt"

        result = optimizer.optimize_prompt("test", prompt, [], "auto")

        assert result == prompt

    def test_optimize_prompt_with_feedback(self):
        """Test optimization with feedback."""
        optimizer = PromptOptimizer()
        prompt = "Original prompt"
        feedback = [
            {"rating": 2, "comment": "unclear instructions"},
            {"rating": 2, "comment": "confusing output"},
        ]

        result = optimizer.optimize_prompt("test", prompt, feedback, "clarity")

        assert "Instructions:" in result

    def test_get_optimization_history(self):
        """Test getting optimization history."""
        optimizer = PromptOptimizer()

        # Add some history
        optimizer.optimize_prompt("skill1", "prompt", [{"rating": 3, "comment": "ok"}], "auto")
        optimizer.optimize_prompt("skill2", "prompt", [{"rating": 4, "comment": "good"}], "auto")

        history = optimizer.get_optimization_history()

        assert len(history) == 2


class TestModelSelector:
    """Tests for ModelSelector."""

    def test_select_model_balanced(self):
        """Test balanced model selection."""
        selector = ModelSelector()

        result = selector.select_model("code-generation", "balanced")

        assert "provider" in result
        assert "model" in result
        assert "reason" in result

    def test_select_model_quality_priority(self):
        """Test quality-priority selection."""
        selector = ModelSelector()

        result = selector.select_model("code-generation", "quality")

        assert result["provider"] in ["openai", "anthropic"]

    def test_select_model_with_constraints(self):
        """Test selection with constraints."""
        selector = ModelSelector()

        result = selector.select_model(
            "code-generation",
            "balanced",
            constraints={"max_cost": 0.001}
        )

        assert result["expected_cost"] <= 0.001

    def test_update_performance(self):
        """Test performance update."""
        selector = ModelSelector()

        selector.update_performance(
            "openai",
            "gpt-4o",
            "code-generation",
            latency=1.0,
            quality=4.5,
            success=True
        )

        recommendations = selector.get_recommendations("code-generation")
        assert len(recommendations) > 0


class TestFeedbackProcessor:
    """Tests for FeedbackProcessor."""

    @pytest.fixture
    def temp_feedback_dir(self):
        """Create temporary feedback directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_record_feedback(self, temp_feedback_dir):
        """Test recording feedback."""
        processor = FeedbackProcessor(feedback_dir=temp_feedback_dir)

        feedback = processor.record_feedback(
            skill_name="test-skill",
            rating=5,
            comment="Great!"
        )

        assert feedback["skill_name"] == "test-skill"
        assert feedback["rating"] == 5
        assert "timestamp" in feedback

    def test_get_feedback(self, temp_feedback_dir):
        """Test getting feedback."""
        processor = FeedbackProcessor(feedback_dir=temp_feedback_dir)

        processor.record_feedback("skill1", 5)
        processor.record_feedback("skill1", 4)
        processor.record_feedback("skill2", 3)

        feedback = processor.get_feedback(skill_name="skill1")

        assert len(feedback) == 2

    def test_analyze_feedback(self, temp_feedback_dir):
        """Test feedback analysis."""
        processor = FeedbackProcessor(feedback_dir=temp_feedback_dir)

        processor.record_feedback("test", 5, comment="good")
        processor.record_feedback("test", 4, comment="nice")
        processor.record_feedback("test", 2, comment="unclear")

        analysis = processor.analyze_feedback("test")

        assert analysis["total_feedback"] == 3
        assert analysis["average_rating"] > 3
        assert "issues" in analysis

    def test_get_improvement_suggestions(self, temp_feedback_dir):
        """Test getting improvement suggestions."""
        processor = FeedbackProcessor(feedback_dir=temp_feedback_dir)

        # Add low-rated feedback
        for _ in range(3):
            processor.record_feedback("test", 2, comment="unclear and confusing")

        suggestions = processor.get_improvement_suggestions("test")

        assert len(suggestions) > 0
        assert any("unclear" in s.lower() for s in suggestions)


class TestABTester:
    """Tests for ABTester."""

    @pytest.fixture
    def temp_tests_dir(self):
        """Create temporary tests directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_create_test(self, temp_tests_dir):
        """Test creating A/B test."""
        tester = ABTester(tests_dir=temp_tests_dir)

        test_id = tester.create_test(
            skill_name="test-skill",
            variant_a={"prompt": "Control prompt"},
            variant_b={"prompt": "Treatment prompt"},
            sample_size=10
        )

        assert test_id.startswith("test-skill_")
        assert test_id in tester.active_tests

    def test_assign_variant(self, temp_tests_dir):
        """Test variant assignment."""
        tester = ABTester(tests_dir=temp_tests_dir)

        test_id = tester.create_test(
            skill_name="test",
            variant_a={"model": "gpt-3.5"},
            variant_b={"model": "gpt-4"},
            sample_size=10
        )

        variant = tester.assign_variant(test_id)

        assert variant in ["A", "B"]

    def test_record_result(self, temp_tests_dir):
        """Test recording test result."""
        tester = ABTester(tests_dir=temp_tests_dir)

        test_id = tester.create_test(
            skill_name="test",
            variant_a={},
            variant_b={},
            sample_size=10
        )

        tester.record_result(test_id, "A", 5)
        tester.record_result(test_id, "A", 4)

        results = tester.get_test_results(test_id)

        assert results["variants"]["A"]["ratings_count"] == 2
        assert results["variants"]["A"]["avg_rating"] == 4.5

    def test_get_test_results(self, temp_tests_dir):
        """Test getting test results."""
        tester = ABTester(tests_dir=temp_tests_dir)

        test_id = tester.create_test(
            skill_name="test",
            variant_a={},
            variant_b={},
            sample_size=2
        )

        tester.record_result(test_id, "A", 4)
        tester.record_result(test_id, "B", 5)

        results = tester.get_test_results(test_id)

        assert "variants" in results
        assert "A" in results["variants"]
        assert "B" in results["variants"]
