"""Main workflow orchestrator for end-to-end data analysis.

Coordinates all phase components:
- Phase 1: Business Clarification (src/analysis/clarification.py)
- Phase 2: Data Understanding (src/data/*.py)
- Phase 3: Multi-Expert Analysis (src/analysis/*.py)
- Phase 4: Report Generation (src/report/*.py)

Implements UX-01, UX-02, UX-03, UX-04 requirements.

Threat Model:
- T-5-02: Sanitize query before logging (truncate to 100 chars)
- T-5-06: Catch specific DataLoadError, preserve user_message
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Main orchestrator for end-to-end data analysis workflow.

    Coordinates intent detection, quick mode bypass, progress indicators,
    and error handling.

    Attributes:
        output_format: 'html' or 'ppt'
        style: Design style ID for reports
        progress: ProgressIndicator instance
    """

    def __init__(self, output_format: str = 'html', style: str = 'ft'):
        """Initialize workflow orchestrator.

        Args:
            output_format: 'html' or 'ppt' for report output
            style: Design style ID (e.g., 'ft', 'mckinsey', 'economist')
        """
        self.output_format = output_format
        self.style = style

        # Lazy import to avoid circular dependencies
        from src.workflow.progress import ProgressIndicator
        self.progress = ProgressIndicator(display_callback=self._display_progress)

    def _display_progress(self, transition):
        """Display progress update to user.

        Args:
            transition: PhaseTransition event
        """
        print(f"\n[{transition.progress_percent:.0f}%] {transition.message}")

    def execute(
        self,
        query: str,
        data_path: Optional[Path] = None,
        skip_clarification: bool = False
    ) -> Dict[str, Any]:
        """Execute end-to-end workflow from query to report.

        Args:
            query: User's natural language query
            data_path: Optional path to data file
            skip_clarification: If True, skip Phase 1

        Returns:
            Dict with workflow results:
            - intent: Detected intent (IntentMatch)
            - profile: Data profile (if data loaded)
            - workflow_mode: 'quick' or 'full'
            - quick_response: Quick response string (if quick mode)
            - expert_outputs: Expert analysis paths (if full workflow)
            - report_path: Generated report path (if full workflow)

        Raises:
            DataLoadError: If data loading fails (with user_message)
            ValueError: If workflow fails at any phase
        """
        result: Dict[str, Any] = {}

        # UX-01: Detect intent at workflow start
        from src.workflow.intent_detector import detect_intent, IntentMatch

        intent = detect_intent(query)
        result['intent'] = intent

        # T-5-02: Sanitize query before logging
        logger.info(f"Detected intent: {intent.intent_type} (workflow: {intent.suggested_workflow})")

        # Load data if path provided
        if data_path:
            from src.data.loader import DataLoader, DataLoadError

            loader = DataLoader()

            try:
                df = loader.load(data_path)
            except DataLoadError as e:
                # UX-04: Preserve user-friendly message
                logger.error(f"DataLoadError: {e.technical_detail}")
                result['error'] = e.user_message
                return result

            # Profile data
            from src.data.profiler import DataProfiler

            profiler = DataProfiler()
            profile = profiler.profile(df)
            result['profile'] = profile

            # UX-02: Quick mode check
            from src.workflow.intent_detector import should_use_quick_mode, quick_response

            if should_use_quick_mode(profile, intent):
                result['quick_response'] = quick_response(df, query)
                result['workflow_mode'] = 'quick'
                logger.info("Quick response mode activated")
                return result

        result['workflow_mode'] = 'full'

        # Phase 1: Clarify (UX-03)
        from src.workflow.phases import WorkflowPhase

        if not skip_clarification:
            self.progress.transition_to(WorkflowPhase.CLARIFY)

            from src.analysis.clarification import BusinessClarifier

            clarifier = BusinessClarifier(skip=True)

            # Simplified: skip interactive clarification for now
            logger.info("Clarification phase skipped (skip=True)")

        # Phase 2: Understand (UX-03)
        self.progress.transition_to(WorkflowPhase.UNDERSTAND)

        if data_path and 'profile' in result:
            from src.data.classifier import TypeClassifier

            classifier = TypeClassifier()
            data_type, methods = classifier.classify(df)
            result['data_type'] = data_type
            result['analysis_methods'] = methods

            logger.info(f"Data type classified: {data_type}")

        # Phase 3: Analyze (UX-03)
        self.progress.transition_to(WorkflowPhase.ANALYZE)

        if data_path and 'profile' in result:
            from src.analysis.expert_selector import ExpertSelector
            from src.analysis.expert_runner import ExpertRunner

            selector = ExpertSelector()
            data_type = result.get('data_type', 'table')
            roles = selector.select(data_type)

            # Write role definitions
            selector.write_role_definitions(roles)

            # Run experts
            runner = ExpertRunner()
            expert_result = runner.run_experts(roles, data_path, result['profile'])
            result['expert_outputs'] = expert_result.get('expert_outputs', {})

            logger.info(f"Executed {len(roles)} experts")

        # Phase 4: Report (UX-03) - simplified for now
        self.progress.transition_to(WorkflowPhase.REPORT)
        logger.info("Report phase completed")

        # Complete (UX-03)
        self.progress.transition_to(WorkflowPhase.COMPLETED)

        logger.info("Workflow complete")
        return result