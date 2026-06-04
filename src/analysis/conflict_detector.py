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


def detect_recommendation_conflicts(expert_outputs: List[Dict]) -> List[Dict]:
    """EXPT-08: Detect recommendation direction conflicts.

    Args:
        expert_outputs: List of expert output dicts with 'recommendation' key

    Returns:
        List of conflict dicts for opposing recommendations

    Note:
        Detects 'increase' vs 'decrease' direction conflicts.
    """
    recommendations = []

    for output in expert_outputs:
        rec = output.get('recommendation', '')
        expert_id = output.get('expert_id', 'unknown')

        # Detect direction keywords (similar to keyword detection in classifier.py)
        if '增加' in rec or '提高' in rec or '上升' in rec:
            recommendations.append(('increase', expert_id))
        elif '减少' in rec or '降低' in rec or '下降' in rec:
            recommendations.append(('decrease', expert_id))

    # Check for opposing directions
    directions = [r[0] for r in recommendations]
    if 'increase' in directions and 'decrease' in directions:
        logger.info('Recommendation conflict detected: opposing directions')
        return [{
            'type': 'recommendation',
            'direction': 'opposite',
            'experts': [r[1] for r in recommendations]
        }]

    return []