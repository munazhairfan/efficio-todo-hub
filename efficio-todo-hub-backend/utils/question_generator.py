from typing import List, Dict, Optional
import random


class QuestionGenerator:
    def __init__(self):
        # Templates for different types of clarifying questions
        self.question_templates = {
            'vague_action': [
                "Could you please specify what exactly you'd like me to do?",
                "I'm not sure what specific action you want me to take. Could you clarify?",
                "Can you be more specific about what you want to accomplish?",
                "What exactly would you like me to do with this?",
                "I need more details to help you. What specific action are you looking for?"
            ],
            'missing_target': [
                "Which specific item are you referring to?",
                "Could you please specify which item you mean?",
                "I need more information to identify the target. Can you clarify?",
                "Can you be more specific about which item you want to work with?",
                "What item are you talking about? Could you provide more details?"
            ],
            'missing_details': [
                "I need more information to complete this request. Could you provide more details?",
                "Can you elaborate on what you need?",
                "What additional information can you share to help me understand?",
                "I need more specifics to help you effectively. What else can you tell me?",
                "Could you provide more context to help me assist you better?"
            ],
            'confirmation': [
                "Just to confirm, do you want me to proceed with this action?",
                "Before I proceed, can you confirm that this is what you want?",
                "Are you sure you want to proceed with this?",
                "This action cannot be undone. Do you still want to proceed?",
                "I want to make sure I understand. Are you certain about this action?"
            ],
            'generic_help': [
                "I'm here to help! Could you tell me what you need assistance with?",
                "How can I assist you today?",
                "What can I help you with?",
                "What would you like me to do for you?",
                "How can I be of service?"
            ],
            'task_specific': [
                "Would you like to create, update, delete, or view tasks?",
                "Do you want to see your current tasks, add a new one, or update an existing one?",
                "What would you like to do with your tasks?",
                "Are you looking to manage your tasks in some way?",
                "Would you like to interact with your tasks?"
            ],
            'status_change': [
                "Which task would you like to update?",
                "What status would you like to change it to?",
                "Could you specify which task's status needs to be changed?",
                "Which task are you referring to?",
                "Can you provide more details about the status change?"
            ],
            'creation_details': [
                "What would you like to create?",
                "Could you provide details about what needs to be created?",
                "What specific item would you like to add?",
                "Can you give me more information about what you want to create?",
                "What type of item are you looking to create?"
            ],
            'deletion_verification': [
                "Are you sure you want to delete this? This action cannot be undone.",
                "Just confirming - you want to delete this, right?",
                "Deleting items is permanent. Do you still want to proceed?",
                "Please confirm that you want to delete this item.",
                "This will permanently delete the item. Is that what you want?"
            ]
        }

    def generate_questions(self, category: str, count: int = 1) -> List[str]:
        """Generate clarifying questions based on category"""
        if category not in self.question_templates:
            # Default to generic help if category not found
            category = 'generic_help'

        available_questions = self.question_templates[category]

        # If we need more questions than available, duplicate and shuffle
        if count <= len(available_questions):
            # Randomly select the requested number of questions
            selected = random.sample(available_questions, count)
        else:
            # Repeat questions if more are needed
            selected = available_questions.copy()
            while len(selected) < count:
                remaining = count - len(selected)
                additional = random.sample(available_questions, min(remaining, len(available_questions)))
                selected.extend(additional)

        return selected

    def generate_for_ambiguity_analysis(self, ambiguity_analysis: Dict) -> List[str]:
        """Generate clarifying questions based on ambiguity analysis results"""
        questions = []

        # If there are vague phrases detected, use specific templates
        if 'categories' in ambiguity_analysis:
            categories = ambiguity_analysis['categories']

            # Check for specific categories that need targeted questions
            if isinstance(categories, dict):
                if categories.get('actions'):
                    questions.extend(self.generate_questions('vague_action', 1))

                if categories.get('objects'):
                    questions.extend(self.generate_questions('missing_target', 1))

                if 'vague_phrases' in categories and categories['vague_phrases']:
                    questions.extend(self.generate_questions('missing_details', 1))

        # If there are specific suggestion-based questions from analysis
        if 'suggestions' in ambiguity_analysis and ambiguity_analysis['suggestions']:
            # Convert suggestions to question format
            for suggestion in ambiguity_analysis['suggestions'][:2]:  # Limit to 2 suggestions
                question = f"To be clear: {suggestion.replace('?', '').replace('.', '')}?"
                questions.append(question)

        # Add generic questions if not enough specific ones
        if len(questions) < 2:
            questions.extend(self.generate_questions('missing_details', 2 - len(questions)))

        return list(set(questions))  # Remove duplicates

    def generate_task_specific_questions(self) -> List[str]:
        """Generate questions specifically for task-related interactions"""
        return self.generate_questions('task_specific', 3)

    def generate_status_change_questions(self) -> List[str]:
        """Generate questions for status change requests"""
        return self.generate_questions('status_change', 2)

    def generate_creation_questions(self) -> List[str]:
        """Generate questions for creation requests"""
        return self.generate_questions('creation_details', 2)

    def generate_deletion_questions(self) -> List[str]:
        """Generate questions for deletion requests"""
        return self.generate_questions('deletion_verification', 2)

    def generate_confirmation_question(self) -> str:
        """Generate a confirmation question"""
        return self.generate_questions('confirmation', 1)[0]

    def generate_custom_question(self, base_topic: str, specificity: str = "medium") -> str:
        """Generate a custom clarifying question based on topic and desired specificity"""
        if specificity == "high":
            return f"Regarding {base_topic}, can you provide specific details about what you need?"
        elif specificity == "medium":
            return f"Could you clarify what you mean by {base_topic}?"
        else:  # low specificity
            return f"I'm not sure how to help with {base_topic}. Can you explain further?"

    def generate_follow_up_questions(self, previous_response: str) -> List[str]:
        """Generate follow-up questions based on previous response"""
        follow_up_templates = [
            f"You mentioned '{previous_response}'. Can you elaborate on that?",
            f"Based on '{previous_response}', what else should I know?",
            f"Regarding '{previous_response}', are there any specifics I should consider?",
            f"You said '{previous_response}'. How does that relate to what you need help with?",
            f"Thanks for mentioning '{previous_response}'. What would you like me to do with this information?"
        ]

        return random.sample(follow_up_templates, min(2, len(follow_up_templates)))

    def get_all_available_categories(self) -> List[str]:
        """Return all available question categories"""
        return list(self.question_templates.keys())

    def generate_multi_layer_questions(self, categories: List[str], count_per_category: int = 1) -> List[str]:
        """Generate questions from multiple categories"""
        all_questions = []
        for category in categories:
            if category in self.question_templates:
                questions = self.generate_questions(category, count_per_category)
                all_questions.extend(questions)

        # Shuffle to mix different types
        random.shuffle(all_questions)
        return all_questions


# Singleton instance
generator = QuestionGenerator()


def get_question_generator() -> QuestionGenerator:
    """Get the question generator instance"""
    return generator