"""Model selection module."""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ModelPerformance:
    """Model performance metrics."""
    provider: str
    model: str
    avg_latency: float
    avg_quality: float
    cost_per_1k_tokens: float
    success_rate: float


class ModelSelector:
    """Selects optimal model based on task requirements."""

    def __init__(self):
        self.performance_data: Dict[str, List[ModelPerformance]] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        """Initialize with default performance data."""
        # Default performance estimates (will be updated with real data)
        self.performance_data = {
            "code-generation": [
                ModelPerformance("openai", "gpt-4o", 1.5, 4.5, 0.005, 0.98),
                ModelPerformance("openai", "gpt-4o-mini", 0.8, 4.0, 0.0006, 0.97),
                ModelPerformance("anthropic", "claude-3-opus", 2.0, 4.7, 0.015, 0.97),
                ModelPerformance("anthropic", "claude-3-sonnet", 1.2, 4.3, 0.003, 0.96),
                ModelPerformance("deepseek", "deepseek-coder", 1.0, 4.2, 0.002, 0.95),
            ],
            "code-analysis": [
                ModelPerformance("openai", "gpt-4o", 1.5, 4.6, 0.005, 0.98),
                ModelPerformance("anthropic", "claude-3-opus", 2.0, 4.8, 0.015, 0.97),
                ModelPerformance("deepseek", "deepseek-coder", 1.0, 4.3, 0.002, 0.95),
            ],
            "documentation": [
                ModelPerformance("openai", "gpt-4o-mini", 0.8, 4.0, 0.0006, 0.97),
                ModelPerformance("anthropic", "claude-3-haiku", 0.6, 3.8, 0.0008, 0.96),
            ],
        }

    def select_model(
        self,
        task_type: str,
        priority: str = "balanced",  # "speed", "quality", "cost", "balanced"
        constraints: Optional[Dict] = None
    ) -> Dict:
        """Select optimal model for task."""
        constraints = constraints or {}
        max_latency = constraints.get("max_latency")
        max_cost = constraints.get("max_cost")
        min_quality = constraints.get("min_quality")

        candidates = self.performance_data.get(task_type, [])

        # Filter by constraints
        filtered = candidates
        if max_latency:
            filtered = [m for m in filtered if m.avg_latency <= max_latency]
        if max_cost:
            filtered = [m for m in filtered if m.cost_per_1k_tokens <= max_cost]
        if min_quality:
            filtered = [m for m in filtered if m.avg_quality >= min_quality]

        if not filtered:
            # Return default if no candidates match
            return {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "reason": "No candidates match constraints, using default"
            }

        # Score candidates based on priority
        if priority == "speed":
            best = min(filtered, key=lambda m: m.avg_latency)
        elif priority == "quality":
            best = max(filtered, key=lambda m: m.avg_quality)
        elif priority == "cost":
            best = min(filtered, key=lambda m: m.cost_per_1k_tokens)
        else:  # balanced
            # Combined score: quality / (latency * cost)
            def score(m):
                return m.avg_quality / (m.avg_latency * m.cost_per_1k_tokens * 1000 + 0.001)
            best = max(filtered, key=score)

        return {
            "provider": best.provider,
            "model": best.model,
            "expected_latency": best.avg_latency,
            "expected_quality": best.avg_quality,
            "expected_cost": best.cost_per_1k_tokens,
            "reason": f"Selected based on {priority} priority"
        }

    def update_performance(
        self,
        provider: str,
        model: str,
        task_type: str,
        latency: float,
        quality: float,
        success: bool
    ):
        """Update performance data with new metrics."""
        if task_type not in self.performance_data:
            self.performance_data[task_type] = []

        # Find existing entry
        for perf in self.performance_data[task_type]:
            if perf.provider == provider and perf.model == model:
                # Update with exponential moving average
                alpha = 0.3
                perf.avg_latency = alpha * latency + (1 - alpha) * perf.avg_latency
                perf.avg_quality = alpha * quality + (1 - alpha) * perf.avg_quality
                perf.success_rate = alpha * (1 if success else 0) + (1 - alpha) * perf.success_rate
                return

        # Add new entry
        self.performance_data[task_type].append(
            ModelPerformance(
                provider=provider,
                model=model,
                avg_latency=latency,
                avg_quality=quality,
                cost_per_1k_tokens=0.001,  # Default estimate
                success_rate=1.0 if success else 0.0
            )
        )

    def get_recommendations(self, task_type: str) -> List[Dict]:
        """Get model recommendations for a task type."""
        candidates = self.performance_data.get(task_type, [])

        return [
            {
                "provider": m.provider,
                "model": m.model,
                "latency": m.avg_latency,
                "quality": m.avg_quality,
                "cost": m.cost_per_1k_tokens,
                "success_rate": m.success_rate
            }
            for m in sorted(candidates, key=lambda x: x.avg_quality, reverse=True)
        ]
