import re
from typing import List, Tuple, Optional
from enum import Enum


class IntentType(Enum):
    AMBIGUOUS = "ambiguous"
    CLEAR_ACTION = "clear_action"
    NEEDS_CONTEXT = "needs_context"
    CONFIRMATION_REQUIRED = "confirmation_required"


class IntentDetector:
    def __init__(self):
        # Patterns for ambiguous/vague inputs
        self.ambiguous_patterns = [
            r'do something with.*',
            r'change.*',
            r'update.*',
            r'modify.*',
            r'work on.*',
            r'handle.*',
            r'take care of.*',
            r'look at.*',
            r'check.*',
            r'deal with.*',
            r'adjust.*',
            r'mess with.*',
            r'fiddle with.*',
            r'sort.*',
            r'organize.*',
            r'clean up.*',
            r'fix.*',
            r'resolve.*',
            r'address.*',
            r'attend to.*',
            r'tend to.*',
            r'manage.*',
            r'process.*',
            r'handle.*',
            r'perform.*',
            r'execute.*',
            r'do.*',
            r'work.*',
            r'act on.*',
        ]

        # Patterns for specific actions
        self.action_patterns = [
            (r'(create|add|make|new)\s+(?:a\s+)?(\w+)', ('create', '{object}')),
            (r'(delete|remove|destroy|erase)\s+(?:the\s+)?(.+)', ('delete', '{target}')),
            (r'(update|modify|change|edit)\s+(?:the\s+)?(.+)', ('update', '{target}')),
            (r'(get|show|display|list|view)\s+(?:the\s+)?(.+)', ('read', '{target}')),
            (r'(find|search|locate|look for)\s+(?:the\s+)?(.+)', ('search', '{target}')),
            (r'(complete|finish|done|mark as complete)\s+(?:the\s+)?(.+)', ('complete', '{target}')),
            (r'(start|begin|initiate)\s+(?:the\s+)?(.+)', ('start', '{target}')),
        ]

        # Patterns that indicate missing information
        self.missing_info_patterns = [
            r'change status',
            r'update status',
            r'mark as done',
            r'mark as complete',
            r'change priority',
            r'update due date',
            r'modify description',
            r'edit title',
        ]

        # Patterns that indicate confirmation might be needed
        self.confirmation_patterns = [
            r'delete',
            r'remove',
            r'destroy',
            r'eradicate',
            r'wipe',
            r'purge',
            r'obliterate',
        ]

    def detect_intent(self, user_input: str) -> Tuple[IntentType, dict]:
        """
        Detect the intent from user input and return intent type with additional info
        """
        user_input_lower = user_input.lower().strip()

        # Check for confirmation-required actions
        for pattern in self.confirmation_patterns:
            if re.search(pattern, user_input_lower):
                return IntentType.CONFIRMATION_REQUIRED, {
                    'action': 'delete_operation',
                    'confidence': 0.8
                }

        # Check for ambiguous patterns first
        for pattern in self.ambiguous_patterns:
            if re.search(pattern, user_input_lower):
                return IntentType.AMBIGUOUS, {
                    'reason': 'vague_request',
                    'detected_phrase': pattern,
                    'confidence': 0.9
                }

        # Check for missing information patterns
        for pattern in self.missing_info_patterns:
            if re.search(pattern, user_input_lower):
                return IntentType.NEEDS_CONTEXT, {
                    'reason': 'missing_specific_target',
                    'detected_phrase': pattern,
                    'confidence': 0.85
                }

        # Check for specific actions
        for pattern, action_info in self.action_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                action, target_template = action_info
                groups = match.groups()

                if len(groups) > 1:
                    target = groups[1]
                    return IntentType.CLEAR_ACTION, {
                        'action': action,
                        'target': target,
                        'confidence': 0.95
                    }
                else:
                    target = groups[0] if groups else ''
                    return IntentType.CLEAR_ACTION, {
                        'action': action,
                        'target': target,
                        'confidence': 0.95
                    }

        # If no specific pattern matched, check for general ambiguity
        tokens = user_input_lower.split()
        if len(tokens) < 3:
            # Very short input might be ambiguous
            return IntentType.AMBIGUOUS, {
                'reason': 'too_short',
                'word_count': len(tokens),
                'confidence': 0.7
            }

        # Default to clear action if nothing else matches
        return IntentType.CLEAR_ACTION, {
            'action': 'unknown',
            'raw_input': user_input,
            'confidence': 0.5
        }

    def is_ambiguous(self, user_input: str) -> bool:
        """Check if the input is ambiguous"""
        intent_type, _ = self.detect_intent(user_input)
        return intent_type == IntentType.AMBIGUOUS

    def needs_context(self, user_input: str) -> bool:
        """Check if the input needs additional context"""
        intent_type, _ = self.detect_intent(user_input)
        return intent_type in [IntentType.NEEDS_CONTEXT, IntentType.AMBIGUOUS]

    def requires_confirmation(self, user_input: str) -> bool:
        """Check if the input requires confirmation"""
        intent_type, _ = self.detect_intent(user_input)
        return intent_type == IntentType.CONFIRMATION_REQUIRED

    def get_missing_information(self, user_input: str) -> List[str]:
        """Identify what information is missing from the input"""
        missing_info = []

        user_input_lower = user_input.lower()

        # Check for patterns that indicate missing specific information
        if re.search(r'change status|update status|mark as done|mark as complete', user_input_lower):
            missing_info.append("Which specific item needs its status changed?")

        if re.search(r'change priority|update priority', user_input_lower):
            missing_info.append("Which specific item needs its priority changed?")

        if re.search(r'update due date', user_input_lower):
            missing_info.append("Which specific item needs its due date updated?")

        if re.search(r'modify description|edit description', user_input_lower):
            missing_info.append("Which specific item needs its description modified?")

        if re.search(r'edit title', user_input_lower):
            missing_info.append("Which specific item needs its title edited?")

        # If it's a generic action without a target
        if self.is_ambiguous(user_input):
            missing_info.append("What specifically would you like to do?")

        return missing_info

    def classify_input(self, user_input: str) -> dict:
        """
        Comprehensive classification of the user input
        """
        intent_type, details = self.detect_intent(user_input)

        result = {
            'intent_type': intent_type.value,
            'details': details,
            'is_ambiguous': self.is_ambiguous(user_input),
            'needs_context': self.needs_context(user_input),
            'requires_confirmation': self.requires_confirmation(user_input),
            'missing_info': self.get_missing_information(user_input),
            'original_input': user_input
        }

        return result


# Singleton instance
detector = IntentDetector()


def get_intent_detector() -> IntentDetector:
    """Get the intent detector instance"""
    return detector