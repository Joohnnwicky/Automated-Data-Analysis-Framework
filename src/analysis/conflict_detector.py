"""Conflict detection module for multi-expert analysis.

Detects contradictory conclusions between expert analyses.
Implements EXPT-08 requirement.
"""

import logging
from typing import List, Dict, Optional
from pathlib import Path
import re

logger = logging.getLogger(__name__)


def detect_numerical_conflicts(expert_outputs: List[Dict]) -> List[Dict]:
    """EXPT-08: Detect numerical conflicts between expert outputs.

    Args:
        expert_outputs: List of expert output dicts with 'expert_id' and 'metrics' keys

    Returns:
        List of conflict dicts with type, metric, values, experts, threshold

    Note:
        Threshold: 10% difference for numerical conflicts.
        Similar to anomaly detection threshold in insights.py.
    """
    conflicts = []
    metrics = {}

    for output in expert_outputs:
        expert_id = output.get('expert_id', 'unknown')
        for metric, value in output.get('metrics', {}).items():
            if metric in metrics:
                existing = metrics[metric]
                # Check if difference exceeds 10% threshold
                if abs(existing['value'] - value) > 0.1 * max(existing['value'], value):
                    conflicts.append({
                        'type': 'numerical',
                        'metric': metric,
                        'values': [existing['value'], value],
                        'experts': [existing['expert'], expert_id],
                        'threshold': '10%'
                    })
                    logger.info(f'Numerical conflict: {metric} differs by >10%')
            metrics[metric] = {'value': value, 'expert': expert_id}

    return conflicts