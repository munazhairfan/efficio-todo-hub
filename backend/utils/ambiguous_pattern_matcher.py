import re
from typing import List, Dict, Tuple, Optional
from enum import Enum


class AmbiguityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AmbiguousPatternMatcher:
    def __init__(self):
        # High-level ambiguity patterns (vague requests)
        self.high_ambiguity_patterns = [
            {
                'pattern': r'\b(do|handle|manage|deal with|take care of|work on|process|sort out|figure out|look into|check out|take a look at|mess with|tinker with|play with)\b.*\b(tasks?|items?|things?|stuff|work|job|assignments?|todos?)\b',
                'category': 'vague_action',
                'severity': AmbiguityLevel.HIGH,
                'message': 'The action requested is too vague. Please specify what exactly you want to do.'
            },
            {
                'pattern': r'\b(change|update|modify|adjust|alter|tweak|fix|edit|work on|touch|deal with)\b.*\b(status|priority|due date|deadline|title|description|details?|info|information)\b',
                'category': 'missing_target',
                'severity': AmbiguityLevel.HIGH,
                'message': 'The target for this action is not specified. Which item needs to be updated?'
            },
            {
                'pattern': r'\b(mark|set|make|turn|flag)\b.*\b(done|completed?|finished|complete|ready|closed)\b',
                'category': 'missing_target',
                'severity': AmbiguityLevel.HIGH,
                'message': 'The target for marking as done is not specified. Which item needs to be marked?'
            }
        ]

        # Medium-level ambiguity patterns (some info but incomplete)
        self.medium_ambiguity_patterns = [
            {
                'pattern': r'\b(delete|remove|kill|erase|wipe|eliminate|get rid of)\b.*\b(tasks?|items?|things?|entries?)\b',
                'category': 'deletion_without_target',
                'severity': AmbiguityLevel.MEDIUM,
                'message': 'Deletion requested but no specific target specified.'
            },
            {
                'pattern': r'\b(create|add|make|generate|produce|build|establish)\b.*\b(new|another|more|additional)\b',
                'category': 'creation_without_details',
                'severity': AmbiguityLevel.MEDIUM,
                'message': 'Creation requested but no details about what to create.'
            },
            {
                'pattern': r'\b(find|search|locate|seek|hunt|discover|identify)\b.*\b(tasks?|items?|things?|entries?)\b',
                'category': 'search_without_criteria',
                'severity': AmbiguityLevel.MEDIUM,
                'message': 'Search requested but no criteria specified.'
            }
        ]

        # Low-level ambiguity patterns (slightly unclear)
        self.low_ambiguity_patterns = [
            {
                'pattern': r'\b(list|show|display|present|give me|provide|fetch|retrieve|get)\b.*\b(tasks?|items?|things?|entries?)\b',
                'category': 'generic_display',
                'severity': AmbiguityLevel.LOW,
                'message': 'Generic display request, may need filtering or sorting.'
            },
            {
                'pattern': r'\b(help|assist|support|aid|guide|advise|suggest)\b',
                'category': 'help_request',
                'severity': AmbiguityLevel.LOW,
                'message': 'General help request, may need specifics.'
            }
        ]

        # Critical ambiguity patterns (potentially harmful)
        self.critical_ambiguity_patterns = [
            {
                'pattern': r'\b(delete|remove|destroy|nuke|obliterate|annihilate|eradicate)\b.*\ball\b|\beverything\b',
                'category': 'bulk_deletion',
                'severity': AmbiguityLevel.CRITICAL,
                'message': 'Potentially dangerous bulk deletion request detected.'
            }
        ]

        # Compile all patterns for better performance
        self.compiled_patterns = {}
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for better performance"""
        all_patterns = (
            self.high_ambiguity_patterns +
            self.medium_ambiguity_patterns +
            self.low_ambiguity_patterns +
            self.critical_ambiguity_patterns
        )

        for i, pattern_info in enumerate(all_patterns):
            compiled_pattern = re.compile(pattern_info['pattern'], re.IGNORECASE)
            self.compiled_patterns[i] = {
                'compiled': compiled_pattern,
                'original': pattern_info
            }

    def match_patterns(self, text: str) -> List[Dict]:
        """Match text against all patterns and return matches"""
        matches = []
        text_lower = text.lower()

        for idx, pattern_info in self.compiled_patterns.items():
            compiled_pattern = pattern_info['compiled']
            original_info = pattern_info['original']

            if compiled_pattern.search(text_lower):
                match = compiled_pattern.search(text_lower)
                matches.append({
                    'matched_text': match.group(0),
                    'category': original_info['category'],
                    'severity': original_info['severity'],
                    'message': original_info['message'],
                    'start_pos': match.start(),
                    'end_pos': match.end()
                })

        # Sort by severity (critical first, then high, medium, low)
        matches.sort(key=lambda x: ['critical', 'high', 'medium', 'low'].index(x['severity'].value))

        return matches

    def get_ambiguity_level(self, text: str) -> AmbiguityLevel:
        """Determine the overall ambiguity level of the text"""
        matches = self.match_patterns(text)

        if not matches:
            return AmbiguityLevel.LOW

        # Get the highest severity among matches
        max_severity = max(matches, key=lambda x: ['low', 'medium', 'high', 'critical'].index(x['severity'].value))
        return max_severity['severity']

    def is_ambiguous(self, text: str, min_severity: AmbiguityLevel = AmbiguityLevel.MEDIUM) -> bool:
        """Check if text is ambiguous based on minimum severity threshold"""
        ambiguity_level = self.get_ambiguity_level(text)
        severity_order = ['low', 'medium', 'high', 'critical']

        return severity_order.index(ambiguity_level.value) >= severity_order.index(min_severity.value)

    def get_clarification_questions(self, text: str) -> List[str]:
        """Generate clarification questions based on detected ambiguity patterns"""
        matches = self.match_patterns(text)
        questions = []

        for match in matches:
            # Add the specific message from the pattern
            questions.append(match['message'])

            # Add more specific questions based on category
            if match['category'] == 'vague_action':
                questions.extend([
                    "What specific action would you like to perform?",
                    "Could you provide more details about what you want to accomplish?"
                ])
            elif match['category'] == 'missing_target':
                questions.extend([
                    "Which specific item are you referring to?",
                    "Can you provide more details to identify the target?"
                ])
            elif match['category'] == 'deletion_without_target':
                questions.extend([
                    "Which specific item would you like to delete?",
                    "Can you be more specific about what should be removed?"
                ])
            elif match['category'] == 'creation_without_details':
                questions.extend([
                    "What exactly would you like to create?",
                    "Can you provide details about what needs to be created?"
                ])
            elif match['category'] == 'search_without_criteria':
                questions.extend([
                    "What criteria should I use to search?",
                    "Can you specify what you're looking for?"
                ])
            elif match['category'] == 'bulk_deletion':
                questions.extend([
                    "Did you really mean to delete everything?",
                    "This seems like a bulk deletion. Could you confirm what you want to delete?"
                ])

        # Remove duplicates while preserving order
        seen = set()
        unique_questions = []
        for q in questions:
            if q not in seen:
                seen.add(q)
                unique_questions.append(q)

        return unique_questions

    def analyze_ambiguity(self, text: str) -> Dict:
        """Comprehensive ambiguity analysis"""
        matches = self.match_patterns(text)
        ambiguity_level = self.get_ambiguity_level(text)
        is_ambiguous = self.is_ambiguous(text)
        clarification_questions = self.get_clarification_questions(text)

        return {
            'text': text,
            'is_ambiguous': is_ambiguous,
            'ambiguity_level': ambiguity_level.value,
            'matches': matches,
            'clarification_questions': clarification_questions,
            'match_count': len(matches)
        }


# Singleton instance
matcher = AmbiguousPatternMatcher()


def get_ambiguous_pattern_matcher() -> AmbiguousPatternMatcher:
    """Get the pattern matcher instance"""
    return matcher