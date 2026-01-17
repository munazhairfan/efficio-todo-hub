import re
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum


class ActionType(Enum):
    SAFE = "safe"
    CAUTION = "caution"
    CRITICAL = "critical"
    DESTRUCTIVE = "destructive"
    CREATIVE = "creative"
    INFORMATIONAL = "informational"


class ActionClassifier:
    def __init__(self):
        # Patterns for destructive/critical actions
        self.destructive_patterns = [
            # Deletion patterns
            r'\bdelete\b',
            r'\berase\b',
            r'\bremove\b',
            r'\bdestroy\b',
            r'\bnuke\b',
            r'\beliminate\b',
            r'\bwipe\b',
            r'\bpurge\b',
            r'\bobliterate\b',
            r'\bannihilate\b',
            r'\beradicate\b',
            r'\braze\b',
            r'\bextinguish\b',
            r'\bvaporize\b',
            r'\banhilate\b',

            # Bulk operations that could be destructive
            r'\bdelete all\b',
            r'\berase everything\b',
            r'\bremove all\b',
            r'\bclear all\b',
            r'\breset all\b',
            r'\bwipe out\b',
            r'\bnuke all\b',
            r'\bdestroy all\b',

            # Modification patterns that could be problematic
            r'\boverwrite\b',
            r'\breplace all\b',
            r'\bforce update\b',
            r'\bpermanent change\b',
            r'\birreversible\b',
            r'\bundo not possible\b',
            r'\bcannot be reverted\b',
        ]

        # Patterns for cautionary actions
        self.caution_patterns = [
            # Potentially risky operations
            r'\bmodify\b',
            r'\bchange\b',
            r'\bupdate\b',
            r'\bedit\b',
            r'\badjust\b',
            r'\balter\b',
            r'\btweak\b',
            r'\bconfigure\b',
            r'\bset\b',
            r'\bassign\b',
            r'\bgrant\b',
            r'\brevoke\b',
            r'\bdisable\b',
            r'\benable\b',
            r'\bactivate\b',
            r'\bdeactivate\b',

            # Administrative actions
            r'\badmin\b',
            r'\badministrator\b',
            r'\bpermission\b',
            r'\bprivilege\b',
            r'\baccess\b',
            r'\brole\b',
            r'\brights\b',
            r'\bauthority\b',
        ]

        # Patterns for safe/common actions
        self.safe_patterns = [
            # Informational/read-only actions
            r'\bview\b',
            r'\bsee\b',
            r'\bshow\b',
            r'\bdisplay\b',
            r'\blist\b',
            r'\bget\b',
            r'\bread\b',
            r'\bfind\b',
            r'\bsearch\b',
            r'\blook up\b',
            r'\bquery\b',
            r'\bfetch\b',
            r'\bretrieve\b',

            # Creation patterns
            r'\bcreate\b',
            r'\badd\b',
            r'\bnew\b',
            r'\bmake\b',
            r'\bgenerate\b',
            r'\bbuild\b',
            r'\bconstruct\b',
            r'\bproduce\b',
            r'\bform\b',
            r'\bestablish\b',
        ]

        # Patterns that indicate urgency or risk
        self.risk_indicators = [
            r'\bimmediate\b',
            r'\burgent\b',
            r'\bnow\b',
            r'\binstant\b',
            r'\bquick\b',
            r'\bfast\b',
            r'\bexpedite\b',
            r'\bhurry\b',
            r'\brush\b',
            r'\bforce\b',
            r'\bemergency\b',
            r'\bcritical\b',
            r'\bemergency\b',
            r'\bcrucial\b',
        ]

        # Compile patterns for performance
        self.compiled_destructive = [re.compile(p, re.IGNORECASE) for p in self.destructive_patterns]
        self.compiled_caution = [re.compile(p, re.IGNORECASE) for p in self.caution_patterns]
        self.compiled_safe = [re.compile(p, re.IGNORECASE) for p in self.safe_patterns]
        self.compiled_risk = [re.compile(p, re.IGNORECASE) for p in self.risk_indicators]

    def classify_action(self, action_text: str) -> Dict[str, Any]:
        """
        Classify an action based on its potential risk level
        """
        action_lower = action_text.lower()

        # Initialize result
        result = {
            'action_text': action_text,
            'primary_classification': ActionType.SAFE.value,
            'confidence': 0.0,
            'matched_patterns': {
                'destructive': [],
                'caution': [],
                'safe': [],
                'risk_indicators': []
            },
            'risk_score': 0.0,
            'requires_confirmation': False,
            'explanation': []
        }

        # Check for destructive patterns
        destructive_matches = []
        for pattern in self.compiled_destructive:
            matches = pattern.finditer(action_lower)
            for match in matches:
                destructive_matches.append({
                    'pattern': pattern.pattern,
                    'matched_text': match.group(0),
                    'position': (match.start(), match.end())
                })

        # Check for caution patterns
        caution_matches = []
        for pattern in self.compiled_caution:
            matches = pattern.finditer(action_lower)
            for match in matches:
                caution_matches.append({
                    'pattern': pattern.pattern,
                    'matched_text': match.group(0),
                    'position': (match.start(), match.end())
                })

        # Check for safe patterns
        safe_matches = []
        for pattern in self.compiled_safe:
            matches = pattern.finditer(action_lower)
            for match in matches:
                safe_matches.append({
                    'pattern': pattern.pattern,
                    'matched_text': match.group(0),
                    'position': (match.start(), match.end())
                })

        # Check for risk indicators
        risk_matches = []
        for pattern in self.compiled_risk:
            matches = pattern.finditer(action_lower)
            for match in matches:
                risk_matches.append({
                    'pattern': pattern.pattern,
                    'matched_text': match.group(0),
                    'position': (match.start(), match.end())
                })

        # Store matches
        result['matched_patterns']['destructive'] = destructive_matches
        result['matched_patterns']['caution'] = caution_matches
        result['matched_patterns']['safe'] = safe_matches
        result['matched_patterns']['risk_indicators'] = risk_matches

        # Calculate risk score and determine classification
        destructive_count = len(destructive_matches)
        caution_count = len(caution_matches)
        safe_count = len(safe_matches)
        risk_indicator_count = len(risk_matches)

        # Base risk score calculation
        risk_score = (
            (destructive_count * 0.8) +
            (caution_count * 0.3) +
            (risk_indicator_count * 0.2) -
            (safe_count * 0.1)  # Safe actions slightly reduce risk
        )

        # Cap the risk score between 0 and 1
        risk_score = max(0.0, min(1.0, risk_score))
        result['risk_score'] = risk_score

        # Determine primary classification based on risk score and match types
        if destructive_count > 0:
            result['primary_classification'] = ActionType.DESTRUCTIVE.value
            result['confidence'] = min(0.7 + (destructive_count * 0.1), 0.95)
            result['requires_confirmation'] = True
            result['explanation'].append("Contains destructive action keywords")
        elif caution_count > 0 and destructive_count == 0:
            result['primary_classification'] = ActionType.CAUTION.value
            result['confidence'] = min(0.5 + (caution_count * 0.1), 0.8)
            result['requires_confirmation'] = risk_indicator_count > 0
            if risk_indicator_count > 0:
                result['explanation'].append("Contains cautionary keywords and risk indicators")
            else:
                result['explanation'].append("Contains cautionary keywords")
        elif safe_count > 0 and caution_count == 0 and destructive_count == 0:
            result['primary_classification'] = ActionType.SAFE.value
            result['confidence'] = min(0.6 + (safe_count * 0.05), 0.8)
            result['explanation'].append("Contains safe/informational keywords")
        else:
            # Mixed or neutral classification
            if risk_score > 0.5:
                result['primary_classification'] = ActionType.CAUTION.value
                result['confidence'] = risk_score
                result['requires_confirmation'] = True
                result['explanation'].append("Mixed keywords with higher risk score")
            else:
                result['primary_classification'] = ActionType.SAFE.value
                result['confidence'] = 0.5
                result['explanation'].append("Mixed keywords with lower risk score")

        # Additional checks for specific high-risk scenarios
        if self._has_high_risk_combination(action_lower, destructive_matches, caution_matches):
            result['primary_classification'] = ActionType.CRITICAL.value
            result['confidence'] = 0.9
            result['requires_confirmation'] = True
            result['explanation'].append("High-risk combination detected")

        return result

    def _has_high_risk_combination(self, action_text: str, destructive_matches: List, caution_matches: List) -> bool:
        """
        Check for combinations of words that indicate high risk
        """
        # Check for destructive + urgency combinations
        has_urgency = any(indicator['matched_text'] in action_text for indicator in self._get_risk_indicators(action_text))

        if has_urgency and (len(destructive_matches) > 0 or len(caution_matches) > 0):
            return True

        # Check for bulk destructive operations
        bulk_words = [r'\ball\b', r'\beverything\b', r'\bcomplete\b', r'\bfull\b']
        bulk_patterns = [re.compile(word, re.IGNORECASE) for word in bulk_words]

        bulk_match = any(pattern.search(action_text) for pattern in bulk_patterns)
        destructive_with_bulk = any(pattern.search(action_text) for pattern in self.compiled_destructive)

        return bulk_match and destructive_with_bulk

    def _get_risk_indicators(self, action_text: str) -> List[Dict]:
        """
        Get risk indicators from the action text
        """
        risk_matches = []
        for pattern in self.compiled_risk:
            matches = pattern.finditer(action_text)
            for match in matches:
                risk_matches.append({
                    'pattern': pattern.pattern,
                    'matched_text': match.group(0),
                    'position': (match.start(), match.end())
                })
        return risk_matches

    def is_critical_action(self, action_text: str) -> bool:
        """
        Check if an action is critical and requires special attention
        """
        classification = self.classify_action(action_text)
        return classification['primary_classification'] in [
            ActionType.CRITICAL.value,
            ActionType.DESTRUCTIVE.value
        ]

    def requires_confirmation(self, action_text: str) -> bool:
        """
        Determine if an action requires user confirmation
        """
        classification = self.classify_action(action_text)
        return classification['requires_confirmation']

    def get_confirmation_message(self, action_text: str) -> str:
        """
        Generate an appropriate confirmation message for the action
        """
        classification = self.classify_action(action_text)

        if classification['primary_classification'] == ActionType.DESTRUCTIVE.value:
            return f"This action is destructive: '{action_text}'. Are you sure you want to proceed? This cannot be undone."
        elif classification['primary_classification'] == ActionType.CRITICAL.value:
            return f"This action is critical: '{action_text}'. Please confirm you want to proceed."
        elif classification['primary_classification'] == ActionType.CAUTION.value:
            return f"This action requires caution: '{action_text}'. Would you like to proceed?"
        else:
            return f"About to perform: '{action_text}'. Continue?"

    def analyze_action_sequence(self, action_sequence: List[str]) -> Dict[str, Any]:
        """
        Analyze a sequence of actions for cumulative risk
        """
        classifications = [self.classify_action(action) for action in action_sequence]

        # Calculate overall risk
        max_risk_score = max(c['risk_score'] for c in classifications)
        total_destructive = sum(1 for c in classifications if c['primary_classification'] == ActionType.DESTRUCTIVE.value)
        total_caution = sum(1 for c in classifications if c['primary_classification'] == ActionType.CAUTION.value)

        overall_classification = ActionType.SAFE.value
        if total_destructive > 0:
            overall_classification = ActionType.DESTRUCTIVE.value
        elif total_caution > 0:
            overall_classification = ActionType.CAUTION.value

        return {
            'individual_classifications': classifications,
            'overall_classification': overall_classification,
            'max_risk_score': max_risk_score,
            'total_destructive_actions': total_destructive,
            'total_caution_actions': total_caution,
            'requires_batch_confirmation': total_destructive > 0 or max_risk_score > 0.6
        }

    def get_action_recommendations(self, action_text: str) -> List[str]:
        """
        Get recommendations based on the action classification
        """
        classification = self.classify_action(action_text)
        recommendations = []

        if classification['requires_confirmation']:
            recommendations.append("This action requires user confirmation before proceeding")

        if classification['primary_classification'] == ActionType.DESTRUCTIVE.value:
            recommendations.extend([
                "Consider creating a backup before proceeding",
                "Double-check the target of this action",
                "Ensure you have permission to perform this action"
            ])
        elif classification['primary_classification'] == ActionType.CAUTION.value:
            recommendations.extend([
                "Review the parameters of this action",
                "Verify the impact of this action",
                "Consider the timing of this action"
            ])

        if classification['risk_score'] > 0.7:
            recommendations.append("Consider performing this action during off-peak hours")

        return recommendations


# Singleton instance
classifier = ActionClassifier()


def get_action_classifier() -> ActionClassifier:
    """Get the action classifier instance"""
    return classifier