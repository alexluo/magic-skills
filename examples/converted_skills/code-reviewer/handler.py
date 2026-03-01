"""
Converted from Anthropic Skills: code-reviewer
Enhanced with Magic Skills capabilities
"""

from typing import Dict, Any
from src.core.base_skill import BaseSkill
import re


class CodeReviewerSkill(BaseSkill):
    """
    Enhanced code reviewer with Magic Skills features:
    - Multi-LLM support
    - Cost tracking
    - Feedback collection
    - Self-optimization
    """
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        code = params["code"]
        language = params.get("language", "python")
        
        # Load the original Anthropic prompt
        prompt_template = self.load_prompt()
        
        # Enhance with Magic Skills context
        enhanced_prompt = f"""{prompt_template}

## Additional Context
- Language: {language}
- Code Length: {len(code)} characters
- Lines: {len(code.split(chr(10)))}

## Code to Review
```{language}
{code}
```

Please provide your review now.
"""
        
        # Generate review using configured LLM
        review = self.llm.generate(enhanced_prompt)
        
        # Extract structured data
        issues = self._extract_issues(review)
        score = self._calculate_score(review, len(issues))
        
        # Record execution for optimization
        self._record_execution(params, review)
        
        return {
            "review": review,
            "issues": issues,
            "score": score,
            "language": language,
            "metrics": {
                "code_length": len(code),
                "issues_found": len(issues)
            }
        }
    
    def _extract_issues(self, review: str) -> list:
        """Extract issues from review text."""
        # Look for patterns like "- [High]" or "### Bug"
        issues = []
        lines = review.split("\n")
        for line in lines:
            if any(marker in line for marker in ["- [", "### ", "**Issue"]):
                issues.append(line.strip())
        return issues
    
    def _calculate_score(self, review: str, issue_count: int) -> float:
        """Calculate code quality score."""
        base_score = 10.0
        
        # Deduct points for issues
        deductions = min(issue_count * 0.5, 5.0)
        
        # Check for positive indicators
        if "excellent" in review.lower() or "great" in review.lower():
            base_score += 0.5
        
        score = max(1.0, min(10.0, base_score - deductions))
        return round(score, 1)
    
    def _record_execution(self, params: Dict[str, Any], result: str):
        """Record execution for future optimization."""
        # This enables self-optimization features
        execution_data = {
            "skill": self.name,
            "params_keys": list(params.keys()),
            "result_length": len(result),
        }
        # Would be saved to feedback system
        self.logger.debug(f"Recorded execution: {execution_data}")


# Backward compatibility - can also be used as a simple function
def review_code(code: str, language: str = "python") -> str:
    """Simple function interface for backward compatibility."""
    skill = CodeReviewerSkill()
    result = skill.execute({"code": code, "language": language})
    return result["review"]
