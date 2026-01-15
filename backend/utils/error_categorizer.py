from typing import Dict, List, Optional, Any
from enum import Enum
import re


class ErrorCategory(Enum):
    USER_INPUT_ERROR = "user_input_error"
    SYSTEM_ERROR = "system_error"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    BUSINESS_LOGIC_ERROR = "business_logic_error"
    SECURITY_ERROR = "security_error"
    DATA_ERROR = "data_error"
    UNKNOWN_ERROR = "unknown_error"


class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategorizer:
    def __init__(self):
        # Patterns for user input errors
        self.user_input_patterns = [
            r'invalid.*input',
            r'wrong.*format',
            r'not.*valid',
            r'incorrect.*data',
            r'unrecognized.*command',
            r'unknown.*action',
            r'missing.*required',
            r'insufficient.*information',
            r'ambiguous.*request',
            r'unclear.*instruction',
        ]

        # Patterns for system errors
        self.system_error_patterns = [
            r'timeout',
            r'connection.*refused',
            r'server.*error',
            r'internal.*error',
            r'database.*connection',
            r'failed.*to.*connect',
            r'system.*unavailable',
            r'service.*unavailable',
            r'memory.*error',
            r'runtime.*error',
        ]

        # Patterns for network errors
        self.network_error_patterns = [
            r'network.*error',
            r'connection.*timeout',
            r'network.*unreachable',
            r'dns.*lookup.*failed',
            r'http.*error',
            r'request.*failed',
            r'could not resolve',
            r'network.*is unreachable',
        ]

        # Patterns for validation errors
        self.validation_error_patterns = [
            r'validation.*failed',
            r'not.*meet.*criteria',
            r'does not match',
            r'out of range',
            r'invalid.*value',
            r'value.*too.*long',
            r'value.*too.*short',
            r'constraint.*violation',
            r'duplicate.*entry',
            r'unique.*constraint',
        ]

        # Patterns for business logic errors
        self.business_logic_patterns = [
            r'cannot.*perform.*operation',
            r'permission.*denied',
            r'not.*authorized',
            r'forbidden',
            r'access.*denied',
            r'precondition.*failed',
            r'conflict.*with.*existing',
            r'violates.*business.*rule',
            r'not.*allowed',
            r'operation.*not.*supported',
        ]

        # Patterns for security errors
        self.security_patterns = [
            r'unauthorized',
            r'authentication.*failed',
            r'authorization.*failed',
            r'access.*forbidden',
            r'security.*violation',
            r'csrf.*token',
            r'invalid.*credentials',
            r'account.*locked',
            r'rate.*limit',
            r'suspicious.*activity',
        ]

        # Patterns for data errors
        self.data_patterns = [
            r'resource.*not found',
            r'data.*does not exist',
            r'record.*missing',
            r'item.*not found',
            r'entity.*not found',
            r'no.*results',
            r'empty.*result',
            r'null.*pointer',
            r'data.*integrity',
            r'corrupted.*data',
        ]

        # Severity indicators
        self.severity_indicators = {
            ErrorSeverity.CRITICAL: [
                r'critical',
                r'emergency',
                r'panic',
                r'fatal',
                r'crash',
                r'breakdown',
                r'failure',
            ],
            ErrorSeverity.HIGH: [
                r'high.*severity',
                r'important',
                r'urgent',
                r'critical',
                r'severe',
                r'serious',
                r'bad',
            ],
            ErrorSeverity.MEDIUM: [
                r'medium',
                r'moderate',
                r'some',
                r'partial',
                r'warning',
                r'attention',
            ],
            ErrorSeverity.LOW: [
                r'low',
                r'minor',
                r'small',
                r'insignificant',
                r'negligible',
                r'cosmetic',
            ]
        }

        # Compile patterns for better performance
        self.compiled_patterns = {
            ErrorCategory.USER_INPUT_ERROR: [re.compile(p, re.IGNORECASE) for p in self.user_input_patterns],
            ErrorCategory.SYSTEM_ERROR: [re.compile(p, re.IGNORECASE) for p in self.system_error_patterns],
            ErrorCategory.NETWORK_ERROR: [re.compile(p, re.IGNORECASE) for p in self.network_error_patterns],
            ErrorCategory.VALIDATION_ERROR: [re.compile(p, re.IGNORECASE) for p in self.validation_error_patterns],
            ErrorCategory.BUSINESS_LOGIC_ERROR: [re.compile(p, re.IGNORECASE) for p in self.business_logic_patterns],
            ErrorCategory.SECURITY_ERROR: [re.compile(p, re.IGNORECASE) for p in self.security_patterns],
            ErrorCategory.DATA_ERROR: [re.compile(p, re.IGNORECASE) for p in self.data_patterns],
        }

        self.compiled_severity_patterns = {
            severity: [re.compile(p, re.IGNORECASE) for p in patterns]
            for severity, patterns in self.severity_indicators.items()
        }

    def categorize_error(self, error_message: str, exception_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Categorize an error based on its message and optional exception type
        """
        if not error_message:
            return {
                'category': ErrorCategory.UNKNOWN_ERROR.value,
                'severity': ErrorSeverity.MEDIUM.value,
                'confidence': 0.5,
                'matched_patterns': [],
                'exception_type': exception_type
            }

        # Check each category
        matches = {}
        max_confidence = 0
        best_category = ErrorCategory.UNKNOWN_ERROR

        for category, patterns in self.compiled_patterns.items():
            category_matches = []
            for pattern in patterns:
                match = pattern.search(error_message)
                if match:
                    category_matches.append({
                        'pattern': pattern.pattern,
                        'matched_text': match.group(0),
                        'start': match.start(),
                        'end': match.end()
                    })

            if category_matches:
                # Calculate confidence based on number of matches
                confidence = min(len(category_matches) * 0.3, 0.9)  # Max 90% for multiple matches
                matches[category] = {
                    'matches': category_matches,
                    'confidence': confidence
                }

                if confidence > max_confidence:
                    max_confidence = confidence
                    best_category = category

        # Determine severity
        severity = self._determine_severity(error_message)

        # If no specific category matched, use exception type as hint
        if best_category == ErrorCategory.UNKNOWN_ERROR and exception_type:
            best_category, max_confidence = self._infer_from_exception_type(exception_type)

        result = {
            'category': best_category.value,
            'severity': severity.value,
            'confidence': max_confidence,
            'matched_patterns': matches.get(best_category, {}).get('matches', []),
            'all_matches': {
                category.value: match_info['matches']
                for category, match_info in matches.items()
            },
            'exception_type': exception_type
        }

        return result

    def _determine_severity(self, error_message: str) -> ErrorSeverity:
        """
        Determine the severity of an error based on its message
        """
        severity_scores = {}

        for severity, patterns in self.compiled_severity_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern.search(error_message):
                    score += 1
            severity_scores[severity] = score

        # Return the severity with the highest score, defaulting to MEDIUM
        if max(severity_scores.values()) > 0:
            return max(severity_scores, key=severity_scores.get)
        else:
            # Default severity based on error category hints in the message
            lower_msg = error_message.lower()
            if any(word in lower_msg for word in ['not found', 'missing', 'does not exist']):
                return ErrorSeverity.MEDIUM  # Usually not critical
            elif any(word in lower_msg for word in ['timeout', 'connection', 'network']):
                return ErrorSeverity.HIGH  # Network issues can be serious
            else:
                return ErrorSeverity.MEDIUM

    def _infer_from_exception_type(self, exception_type: str) -> tuple[ErrorCategory, float]:
        """
        Infer error category from exception type
        """
        lower_type = exception_type.lower()

        if any(name in lower_type for name in ['valueerror', 'typeerror', 'attributeerror']):
            return ErrorCategory.VALIDATION_ERROR, 0.7
        elif any(name in lower_type for name in ['connection', 'timeout', 'socket', 'http']):
            return ErrorCategory.NETWORK_ERROR, 0.8
        elif any(name in lower_type for name in ['permission', 'auth', 'security', 'forbidden']):
            return ErrorCategory.SECURITY_ERROR, 0.9
        elif any(name in lower_type for name in ['keyerror', 'indexerror', 'notfound']):
            return ErrorCategory.DATA_ERROR, 0.75
        elif any(name in lower_type for name in ['runtime', 'system', 'memory', 'io']):
            return ErrorCategory.SYSTEM_ERROR, 0.85
        else:
            return ErrorCategory.UNKNOWN_ERROR, 0.3

    def get_user_friendly_message(self, error_category: str, original_message: str = "") -> str:
        """
        Generate a user-friendly error message based on the category
        """
        category = ErrorCategory(error_category)

        messages = {
            ErrorCategory.USER_INPUT_ERROR: "I had trouble understanding your request. Could you rephrase that?",
            ErrorCategory.SYSTEM_ERROR: "Something went wrong on my end. I'm working to resolve it.",
            ErrorCategory.NETWORK_ERROR: "I'm having trouble connecting right now. Please try again in a moment.",
            ErrorCategory.VALIDATION_ERROR: "Some of the information you provided isn't quite right. Could you check it?",
            ErrorCategory.BUSINESS_LOGIC_ERROR: "I can't perform that action due to system rules. Is there something else I can help with?",
            ErrorCategory.SECURITY_ERROR: "I can't complete that request for security reasons. Please verify your permissions.",
            ErrorCategory.DATA_ERROR: "I couldn't find the information you're looking for. Does it exist?",
            ErrorCategory.UNKNOWN_ERROR: "An unexpected error occurred. I've been notified and am looking into it."
        }

        return messages.get(category, "An error occurred. Please try again or contact support if the problem persists.")

    def get_suggested_actions(self, error_category: str) -> List[str]:
        """
        Get suggested actions based on error category
        """
        category = ErrorCategory(error_category)

        actions = {
            ErrorCategory.USER_INPUT_ERROR: [
                "Try rephrasing your request more specifically",
                "Break your request into smaller steps",
                "Provide more detailed information"
            ],
            ErrorCategory.SYSTEM_ERROR: [
                "Wait a moment and try again",
                "Refresh the page or restart the application",
                "Contact support if the issue persists"
            ],
            ErrorCategory.NETWORK_ERROR: [
                "Check your internet connection",
                "Wait a moment and try again",
                "Try again later when the connection is stable"
            ],
            ErrorCategory.VALIDATION_ERROR: [
                "Check the format of your input",
                "Verify that all required fields are filled",
                "Ensure values are within acceptable ranges"
            ],
            ErrorCategory.BUSINESS_LOGIC_ERROR: [
                "Review the system requirements for this action",
                "Try an alternative approach",
                "Contact an administrator if you believe you should have access"
            ],
            ErrorCategory.SECURITY_ERROR: [
                "Verify your account permissions",
                "Log out and log back in",
                "Contact your system administrator"
            ],
            ErrorCategory.DATA_ERROR: [
                "Verify the information you're looking for exists",
                "Try searching with different keywords",
                "Check if the item was recently deleted"
            ],
            ErrorCategory.UNKNOWN_ERROR: [
                "Try the action again",
                "Restart the application",
                "Contact support for assistance"
            ]
        }

        return actions.get(category, ["Try again", "Contact support if the problem persists"])

    def analyze_error_context(self, error_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a complete error context for categorization
        """
        error_message = error_details.get('message', '')
        exception_type = error_details.get('exception_type', '')
        stack_trace = error_details.get('stack_trace', '')

        # Combine message and stack trace for more accurate categorization
        full_context = f"{error_message} {stack_trace}".strip()

        category_result = self.categorize_error(full_context, exception_type)

        return {
            'original_error': error_details,
            'categorized': category_result,
            'user_friendly_message': self.get_user_friendly_message(category_result['category'], error_message),
            'suggested_actions': self.get_suggested_actions(category_result['category']),
            'can_retry': self._can_retry(category_result['category'])
        }

    def _can_retry(self, error_category: str) -> bool:
        """
        Determine if an error is retryable
        """
        category = ErrorCategory(error_category)
        return category in [
            ErrorCategory.SYSTEM_ERROR,
            ErrorCategory.NETWORK_ERROR,
            ErrorCategory.UNKNOWN_ERROR
        ]


# Singleton instance
categorizer = ErrorCategorizer()


def get_error_categorizer() -> ErrorCategorizer:
    """Get the error categorizer instance"""
    return categorizer