import re
from typing import List, Dict, Tuple
from enum import Enum


class VagueTermCategory(Enum):
    ACTIONS = "actions"
    OBJECTS = "objects"
    QUANTIFIERS = "quantifiers"
    TIME = "time"
    UNCERTAIN = "uncertain"


class VagueTermDetector:
    def __init__(self):
        # Dictionary of vague terms categorized by type
        self.vague_terms = {
            VagueTermCategory.ACTIONS: [
                # General action words that don't specify what to do
                r'\bdo\b', r'\bhandle\b', r'\bdeal with\b', r'\btake care of\b',
                r'\bwork on\b', r'\bprocess\b', r'\bsort out\b', r'\bfigure out\b',
                r'\blook into\b', r'\bcheck\b', r'\bmanage\b', r'\baddress\b',
                r'\bfiddle with\b', r'\bmess with\b', r'\btinker with\b',
                r'\bplay with\b', r'\bfix\b', r'\bresolve\b', r'\badjust\b',
                r'\bedit\b', r'\btouch\b', r'\bwork\b', r'\bdeal\b'
            ],
            VagueTermCategory.OBJECTS: [
                # General object references that don't specify what
                r'\bthings?\b', r'\bstuff\b', r'\bit\b', r'\bthem\b',
                r'\bthose\b', r'\bthese\b', r'\bthat\b', r'\bthis\b',
                r'\bitems?\b', r'\btasks?\b', r'\bworks?\b', r'\bjobs?\b',
                r'\bassignments?\b', r'\btodos?\b', r'\bentries?\b', r'\bobjects?\b'
            ],
            VagueTermCategory.QUANTIFIERS: [
                # Vague quantity indicators
                r'\bsome\b', r'\ball\b', r'\beverything\b', r'\bmany\b',
                r'\bmultiple\b', r'\bseveral\b', r'\ba few\b', r'\btons of\b',
                r'\blots of\b', r'\bquite a bit\b', r'\benough\b', r'\bvarious\b',
                r'\bdifferent\b', r'\bnumerous\b', r'\bcertain\b', r'\bspecific\b'
            ],
            VagueTermCategory.TIME: [
                # Vague time references
                r'\bson\b', r'\blater\b', r'\bwhenever\b', r'\bwhen possible\b',
                r'\basap\b', r'\bsoon\b', r'\bnow\b', r'\bimmediately\b',
                r'\bquickly\b', r'\bfast\b', r'\bby end of day\b', r'\bthis week\b',
                r'\bnext week\b', r'\bsomeday\b', r'\bwhenever convenient\b'
            ],
            VagueTermCategory.UNCERTAIN: [
                # Words indicating uncertainty
                r'\bmaybe\b', r'\bperhaps\b', r'\bpossibly\b', r'\bprobably\b',
                r'\bmight\b', r'\bcould\b', r'\bshould\b', r'\btry to\b',
                r'\battempt\b', r'\bhopefully\b', r'\bif possible\b', r'\bif feasible\b',
                r'\bideally\b', r'\bpreferably\b', r'\busually\b', r'\bgenerally\b'
            ]
        }

        # Pre-compile regex patterns for performance
        self.compiled_patterns = {}
        self._compile_patterns()

        # Common vague phrases that indicate unclear intent
        self.vague_phrases = [
            r'\bdo something\b',
            r'\bwork on it\b',
            r'\bhandle that\b',
            r'\bdeal with them\b',
            r'\btake care of this\b',
            r'\bfigure it out\b',
            r'\blook into that\b',
            r'\bcheck it out\b',
            r'\bdo whatever\b',
            r'\bmake it work\b',
            r'\bfix the problem\b',
            r'\bsolve this\b',
            r'\bdeal with issues\b',
            r'\bhandle everything\b',
            r'\btake care of business\b',
            r'\bwork things out\b',
            r'\biron things out\b',
            r'\bsmooth things out\b'
        ]

        # Compile phrase patterns
        self.compiled_phrase_patterns = [re.compile(phrase, re.IGNORECASE) for phrase in self.vague_phrases]

    def _compile_patterns(self):
        """Compile regex patterns for all vague term categories"""
        for category, patterns in self.vague_terms.items():
            self.compiled_patterns[category] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

    def detect_vague_terms(self, text: str) -> List[Dict]:
        """Detect all vague terms in the text and return details about them"""
        detections = []

        # Check for vague phrases first
        for i, phrase_pattern in enumerate(self.compiled_phrase_patterns):
            matches = phrase_pattern.finditer(text)
            for match in matches:
                detections.append({
                    'term': match.group(0),
                    'category': 'vague_phrase',
                    'position': (match.start(), match.end()),
                    'confidence': 0.95
                })

        # Check for individual vague terms by category
        for category, patterns in self.compiled_patterns.items():
            for i, pattern in enumerate(patterns):
                matches = pattern.finditer(text)
                for match in matches:
                    detections.append({
                        'term': match.group(0),
                        'category': category.value,
                        'position': (match.start(), match.end()),
                        'confidence': 0.8 if category == VagueTermCategory.UNCERTAIN else 0.9
                    })

        return detections

    def get_vague_term_categories(self, text: str) -> Dict[VagueTermCategory, List[str]]:
        """Get all vague terms grouped by category"""
        result = {category: [] for category in VagueTermCategory}

        detections = self.detect_vague_terms(text)
        for detection in detections:
            if detection['category'] != 'vague_phrase':
                category = VagueTermCategory(detection['category'])
                if detection['term'] not in result[category]:
                    result[category].append(detection['term'])

        # Also add vague phrases separately
        vague_phrases_found = []
        for phrase_pattern in self.compiled_phrase_patterns:
            matches = phrase_pattern.findall(text)
            for match in matches:
                if match not in vague_phrases_found:
                    vague_phrases_found.append(match)

        result['vague_phrases'] = vague_phrases_found

        return result

    def is_vague(self, text: str, min_detections: int = 1) -> bool:
        """Check if text contains vague terms above a threshold"""
        detections = self.detect_vague_terms(text)
        return len(detections) >= min_detections

    def get_vagueness_score(self, text: str) -> float:
        """
        Calculate a vagueness score between 0 and 1
        0 = very specific, 1 = very vague
        """
        detections = self.detect_vague_terms(text)
        if not detections:
            return 0.0

        # Base score on number of detections
        base_score = min(len(detections) * 0.2, 0.8)  # Up to 0.8 for multiple detections

        # Boost score if vague phrases are found
        phrase_detections = [d for d in detections if d['category'] == 'vague_phrase']
        phrase_bonus = min(len(phrase_detections) * 0.3, 0.4)  # Up to 0.4 bonus for phrases

        # Boost score if multiple categories are represented
        categories_represented = len(set(d['category'] for d in detections))
        category_bonus = min(categories_represented * 0.1, 0.2)  # Up to 0.2 bonus for variety

        total_score = min(base_score + phrase_bonus + category_bonus, 1.0)
        return total_score

    def suggest_specific_alternatives(self, text: str) -> List[str]:
        """Suggest more specific alternatives to vague terms"""
        suggestions = []

        # Check for common vague patterns and suggest alternatives
        if re.search(r'\bdo something\b', text, re.IGNORECASE):
            suggestions.append("Specify what action you want to take (create, update, delete, etc.)")

        if re.search(r'\bchange status\b', text, re.IGNORECASE):
            suggestions.append("Specify which item's status to change and what status to set it to")

        if re.search(r'\bwork on\b', text, re.IGNORECASE):
            suggestions.append("Specify what exactly needs work and what kind of work (update, review, complete, etc.)")

        if re.search(r'\bdeal with\b', text, re.IGNORECASE):
            suggestions.append("Be more specific about the action you want taken")

        if re.search(r'\ball\b', text, re.IGNORECASE) and re.search(r'\bdelete\b', text, re.IGNORECASE):
            suggestions.append("Confirm if you really mean to delete everything, or specify which items to delete")

        # Add suggestions based on detected vague terms
        detections = self.detect_vague_terms(text)
        for detection in detections:
            if detection['category'] == VagueTermCategory.ACTIONS.value:
                suggestions.append(f"Instead of '{detection['term']}', specify the exact action you want to take")
            elif detection['category'] == VagueTermCategory.OBJECTS.value:
                suggestions.append(f"Instead of '{detection['term']}', specify which particular item(s) you mean")
            elif detection['category'] == VagueTermCategory.QUANTIFIERS.value:
                suggestions.append(f"Instead of '{detection['term']}', provide specific quantities or limits")

        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for s in suggestions:
            if s not in seen:
                seen.add(s)
                unique_suggestions.append(s)

        return unique_suggestions

    def analyze_vagueness(self, text: str) -> Dict:
        """Comprehensive vagueness analysis"""
        detections = self.detect_vague_terms(text)
        categories = self.get_vague_term_categories(text)
        vagueness_score = self.get_vagueness_score(text)
        is_vague = self.is_vague(text)
        suggestions = self.suggest_specific_alternatives(text)

        return {
            'text': text,
            'is_vague': is_vague,
            'vagueness_score': vagueness_score,
            'detections': detections,
            'categories': categories,
            'suggestion_count': len(suggestions),
            'suggestions': suggestions,
            'detection_count': len(detections)
        }


# Singleton instance
detector = VagueTermDetector()


def get_vague_term_detector() -> VagueTermDetector:
    """Get the vague term detector instance"""
    return detector