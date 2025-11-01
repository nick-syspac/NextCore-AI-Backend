"""
Rules Engine for funding eligibility evaluation.
Supports JSONLogic format with extensible adapter pattern.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, date
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class EvaluationContext:
    """Context data for rule evaluation"""

    # Input data
    input_data: Dict[str, Any]

    # External lookup results
    lookups: Dict[str, Any]

    # Reference tables
    reference_data: Dict[str, Any]

    # Metadata
    jurisdiction_code: str
    evaluation_date: datetime

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get value from context using dot notation path.

        Example: get('student.age') -> input_data['student']['age']
        """
        parts = path.split(".")
        data = self.input_data

        for part in parts:
            if isinstance(data, dict) and part in data:
                data = data[part]
            else:
                return default

        return data

    def get_lookup(self, provider: str, key: str, default: Any = None) -> Any:
        """Get external lookup result"""
        return self.lookups.get(provider, {}).get(key, default)

    def get_reference(self, namespace: str, key: str, default: Any = None) -> Any:
        """Get reference table data"""
        return self.reference_data.get(namespace, {}).get(key, default)


@dataclass
class EvaluationResult:
    """Result from rule evaluation"""

    # Outcome
    passed: bool
    outcome: str  # 'eligible', 'ineligible', 'review'

    # Reasons
    reasons: List[Dict[str, Any]]

    # Clauses referenced
    clause_refs: List[str]

    # Explanation
    explanation: str

    # Detailed output
    details: Dict[str, Any]

    # Metadata
    ruleset_version: str
    evaluated_at: datetime


class JSONLogicEvaluator:
    """
    Simplified JSONLogic evaluator for eligibility rules.
    Supports common operations needed for funding eligibility.
    """

    def __init__(self):
        self.operators = {
            "==": self._op_equals,
            "!=": self._op_not_equals,
            ">": self._op_greater,
            ">=": self._op_greater_equal,
            "<": self._op_less,
            "<=": self._op_less_equal,
            "and": self._op_and,
            "or": self._op_or,
            "not": self._op_not,
            "in": self._op_in,
            "var": self._op_var,
            "if": self._op_if,
            "between": self._op_between,
            "date_diff": self._op_date_diff,
            "lookup": self._op_lookup,
            "reference": self._op_reference,
        }

    def evaluate(self, logic: Dict[str, Any], context: EvaluationContext) -> Any:
        """Evaluate JSONLogic expression"""
        if not isinstance(logic, dict):
            return logic

        # Get operator
        op = list(logic.keys())[0]
        args = logic[op]

        if op not in self.operators:
            logger.warning(f"Unknown operator: {op}")
            return False

        # Evaluate operator
        return self.operators[op](args, context)

    def _op_equals(self, args: List, context: EvaluationContext) -> bool:
        """Equality check"""
        left = self.evaluate(args[0], context)
        right = self.evaluate(args[1], context)
        return left == right

    def _op_not_equals(self, args: List, context: EvaluationContext) -> bool:
        """Inequality check"""
        return not self._op_equals(args, context)

    def _op_greater(self, args: List, context: EvaluationContext) -> bool:
        """Greater than"""
        left = self.evaluate(args[0], context)
        right = self.evaluate(args[1], context)
        return left > right

    def _op_greater_equal(self, args: List, context: EvaluationContext) -> bool:
        """Greater than or equal"""
        left = self.evaluate(args[0], context)
        right = self.evaluate(args[1], context)
        return left >= right

    def _op_less(self, args: List, context: EvaluationContext) -> bool:
        """Less than"""
        left = self.evaluate(args[0], context)
        right = self.evaluate(args[1], context)
        return left < right

    def _op_less_equal(self, args: List, context: EvaluationContext) -> bool:
        """Less than or equal"""
        left = self.evaluate(args[0], context)
        right = self.evaluate(args[1], context)
        return left <= right

    def _op_and(self, args: List, context: EvaluationContext) -> bool:
        """Logical AND"""
        return all(self.evaluate(arg, context) for arg in args)

    def _op_or(self, args: List, context: EvaluationContext) -> bool:
        """Logical OR"""
        return any(self.evaluate(arg, context) for arg in args)

    def _op_not(self, args: Any, context: EvaluationContext) -> bool:
        """Logical NOT"""
        return not self.evaluate(args, context)

    def _op_in(self, args: List, context: EvaluationContext) -> bool:
        """Check if value in list"""
        value = self.evaluate(args[0], context)
        lst = self.evaluate(args[1], context)
        return value in lst

    def _op_var(self, args: Any, context: EvaluationContext) -> Any:
        """Get variable from context"""
        if isinstance(args, list):
            path = args[0]
            default = args[1] if len(args) > 1 else None
        else:
            path = args
            default = None

        return context.get(path, default)

    def _op_if(self, args: List, context: EvaluationContext) -> Any:
        """Conditional expression"""
        # args = [condition, then_value, else_value]
        condition = self.evaluate(args[0], context)

        if condition:
            return self.evaluate(args[1], context)
        else:
            return self.evaluate(args[2], context) if len(args) > 2 else None

    def _op_between(self, args: List, context: EvaluationContext) -> bool:
        """Check if value between min and max (inclusive)"""
        value = self.evaluate(args[0], context)
        min_val = self.evaluate(args[1], context)
        max_val = self.evaluate(args[2], context)

        return min_val <= value <= max_val

    def _op_date_diff(self, args: List, context: EvaluationContext) -> int:
        """Calculate date difference in days"""
        date1 = self.evaluate(args[0], context)
        date2 = self.evaluate(args[1], context)

        # Parse dates if strings
        if isinstance(date1, str):
            date1 = datetime.fromisoformat(date1).date()
        if isinstance(date2, str):
            date2 = datetime.fromisoformat(date2).date()

        delta = date2 - date1
        return delta.days

    def _op_lookup(self, args: List, context: EvaluationContext) -> Any:
        """Get external lookup result"""
        provider = self.evaluate(args[0], context)
        key = self.evaluate(args[1], context)
        default = self.evaluate(args[2], context) if len(args) > 2 else None

        return context.get_lookup(provider, key, default)

    def _op_reference(self, args: List, context: EvaluationContext) -> Any:
        """Get reference table data"""
        namespace = self.evaluate(args[0], context)
        key = self.evaluate(args[1], context)
        default = self.evaluate(args[2], context) if len(args) > 2 else None

        return context.get_reference(namespace, key, default)


class RulesEngine:
    """
    Main rules engine for funding eligibility evaluation.
    """

    def __init__(self):
        self.evaluator = JSONLogicEvaluator()

    def evaluate(
        self,
        ruleset_artifacts: List[Dict[str, Any]],
        context: EvaluationContext,
        ruleset_version: str,
    ) -> EvaluationResult:
        """
        Evaluate eligibility using ruleset artifacts.

        Args:
            ruleset_artifacts: List of {type, name, blob} dicts
            context: Evaluation context with input and lookup data
            ruleset_version: Version string for reproducibility

        Returns:
            EvaluationResult with outcome and reasons
        """
        reasons = []
        clause_refs = []
        details = {}

        # Track all rule results
        rule_results = []

        for artifact in ruleset_artifacts:
            artifact_type = artifact["type"]
            artifact_name = artifact["name"]
            blob = artifact["blob"]

            if artifact_type == "jsonlogic":
                # Parse and evaluate JSONLogic
                try:
                    logic = json.loads(blob)
                    result = self.evaluator.evaluate(logic, context)

                    rule_results.append(
                        {
                            "artifact": artifact_name,
                            "passed": bool(result),
                            "result": result,
                        }
                    )

                    details[artifact_name] = result

                except Exception as e:
                    logger.error(f"Error evaluating {artifact_name}: {e}")
                    rule_results.append({"artifact": artifact_name, "error": str(e)})

            elif artifact_type == "rego":
                # TODO: Implement OPA/Rego evaluation
                logger.warning(f"Rego not yet supported: {artifact_name}")

            elif artifact_type == "python":
                # TODO: Implement safe Python evaluation
                logger.warning(f"Python not yet supported: {artifact_name}")

        # Determine overall outcome
        passed = all(r.get("passed", False) for r in rule_results if "passed" in r)

        if passed:
            outcome = "eligible"
            explanation = "All eligibility criteria met."
        else:
            # Check if manual review needed
            failed_rules = [
                r["artifact"] for r in rule_results if not r.get("passed", True)
            ]

            # Heuristic: if certain rules fail, require manual review
            review_triggers = [
                "income_verification",
                "qualification_assessment",
                "special_case",
            ]
            needs_review = any(
                trigger in " ".join(failed_rules) for trigger in review_triggers
            )

            if needs_review:
                outcome = "review"
                explanation = f"Manual review required for: {', '.join(failed_rules)}"
                reasons.append(
                    {
                        "code": "MANUAL_REVIEW",
                        "message": "One or more criteria require manual verification",
                    }
                )
            else:
                outcome = "ineligible"
                explanation = f"Eligibility criteria not met: {', '.join(failed_rules)}"
                reasons.append({"code": "CRITERIA_NOT_MET", "message": explanation})

        # Extract clause references from context
        # TODO: Implement clause reference extraction from rule metadata
        clause_refs = self._extract_clause_refs(rule_results, context)

        return EvaluationResult(
            passed=passed,
            outcome=outcome,
            reasons=reasons,
            clause_refs=clause_refs,
            explanation=explanation,
            details=details,
            ruleset_version=ruleset_version,
            evaluated_at=datetime.now(),
        )

    def _extract_clause_refs(
        self, rule_results: List[Dict[str, Any]], context: EvaluationContext
    ) -> List[str]:
        """Extract relevant clause references from rule results"""
        # TODO: Implement based on rule metadata
        # For now, return jurisdiction-specific base clauses

        jurisdiction = context.jurisdiction_code

        base_clauses = {
            "VIC": ["SRF-2024-1.1", "SRF-2024-1.2"],
            "NSW": ["NSI-2024-3.1"],
            "QLD": ["QTR-2024-2.3"],
        }

        return base_clauses.get(jurisdiction, [])

    def explain_decision(
        self, result: EvaluationResult, context: EvaluationContext
    ) -> str:
        """
        Generate human-readable explanation of decision.

        Args:
            result: Evaluation result
            context: Evaluation context

        Returns:
            Formatted explanation string
        """
        lines = []

        lines.append(f"Eligibility Decision: {result.outcome.upper()}")
        lines.append(f"Jurisdiction: {context.jurisdiction_code}")
        lines.append(f"Ruleset Version: {result.ruleset_version}")
        lines.append(f"Evaluated: {result.evaluated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        if result.passed:
            lines.append("✓ All eligibility criteria have been met.")
        else:
            lines.append("✗ Eligibility criteria not met:")
            for reason in result.reasons:
                lines.append(f"  • {reason['message']}")

        if result.clause_refs:
            lines.append("")
            lines.append("Relevant Policy Clauses:")
            for ref in result.clause_refs:
                lines.append(f"  • {ref}")

        if result.details:
            lines.append("")
            lines.append("Rule Details:")
            for rule_name, rule_result in result.details.items():
                status = "✓" if rule_result else "✗"
                lines.append(f"  {status} {rule_name}: {rule_result}")

        return "\n".join(lines)
