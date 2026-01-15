import random
from typing import Dict, List, Optional, Any
from enum import Enum


class ConfirmationType(Enum):
    DESTRUCTIVE = "destructive"
    CAUTIONARY = "cautionary"
    STANDARD = "standard"
    BULK = "bulk"
    SENSITIVE = "sensitive"


class ConfirmationGenerator:
    def __init__(self):
        # Templates for destructive actions
        self.destructive_templates = [
            "This action is {action_type} and cannot be undone. Are you absolutely sure you want to proceed with '{action}'?",
            "Warning: This will {action_desc} permanently. Continuing will result in irreversible changes. Confirm if you're sure.",
            "Heads up: This {action_type} action will permanently {action_desc}. Please confirm if you want to proceed.",
            "Important: This action will {action_desc} forever. There's no way to undo this. Do you want to continue?",
            "Attention: You're about to {action_desc} which cannot be reversed. Please confirm to proceed."
        ]

        # Templates for cautionary actions
        self.cautionary_templates = [
            "This action requires caution: {action}. Would you like to proceed?",
            "Heads up: This action ({action}) might have significant effects. Do you want to continue?",
            "Note: This {action_type} action could impact multiple items. Please confirm if you're ready.",
            "Careful: This action ({action}) may affect several records. Would you like to proceed?",
            "Reminder: This action ({action}) requires your attention. Please confirm to continue."
        ]

        # Templates for standard actions
        self.standard_templates = [
            "About to {action_desc}. Please confirm to proceed.",
            "Ready to {action_desc}. Would you like to continue?",
            "Preparing to {action_desc}. Confirm to execute.",
            "This will {action_desc}. Do you want to proceed?",
            "Ready to carry out '{action}'. Please confirm."
        ]

        # Templates for bulk operations
        self.bulk_templates = [
            "This is a bulk operation affecting {count} items. Are you sure you want to {action_desc} all of them?",
            "Warning: This bulk action will {action_desc} {count} items simultaneously. Please confirm to proceed.",
            "Heads up: This bulk operation will affect {count} items. Do you want to continue?",
            "Notice: You're about to {action_desc} {count} items at once. Please confirm this is intentional.",
            "Alert: This bulk action will permanently {action_desc} {count} items. Are you certain?"
        ]

        # Templates for sensitive operations
        self.sensitive_templates = [
            "This is a sensitive operation involving {data_type} data. Extra confirmation needed to {action_desc}.",
            "Security notice: This action ({action}) involves sensitive data. Please verify your identity to proceed.",
            "Privacy alert: This action ({action}) affects personal data. Confirm if you're authorized to proceed.",
            "Security check: This {action_type} action involves confidential information. Please confirm authorization.",
            "Data protection notice: This action ({action}) may impact sensitive data. Are you authorized to proceed?"
        ]

        # Positive confirmation responses
        self.positive_responses = [
            "Confirmed! Proceeding with the action.",
            "Got it! Moving forward with your request.",
            "Understood! Executing the action now.",
            "Acknowledged! Starting the process.",
            "Approved! Carrying out the action.",
            "Confirmed! I'll take care of that for you.",
            "Yes, sir! Executing your command.",
            "Roger that! Processing your request.",
            "On it! Starting the action now.",
            "Affirmative! Proceeding as requested."
        ]

        # Negative confirmation responses
        self.negative_responses = [
            "Cancelled! The action has been aborted.",
            "Understood! Action cancelled and nothing was changed.",
            "Okay! I've stopped the process.",
            "No problem! The action has been cancelled.",
            "Cancelled! Nothing was affected.",
            "Got it! Action terminated.",
            "Understood! I've cancelled the request.",
            "Okay! Process stopped.",
            "Action aborted! Nothing happened.",
            "Cancelled! Stopping the operation."
        ]

        # Follow-up questions after confirmation
        self.follow_up_questions = [
            "Is there anything else I can help you with?",
            "How did that work out for you?",
            "Was that what you were looking for?",
            "Need any further assistance?",
            "Is there anything else on your mind?",
            "How else can I assist you?",
            "Do you need help with something else?",
            "Anything else I can do for you?",
            "Want to try something else?",
            "What else can I help with?"
        ]

    def generate_confirmation_message(
        self,
        action: str,
        action_type: ConfirmationType,
        count: Optional[int] = None,
        action_description: Optional[str] = None,
        data_type: Optional[str] = None
    ) -> str:
        """
        Generate an appropriate confirmation message based on action type
        """
        # Set defaults
        if not action_description:
            action_description = f"perform {action}"

        # Choose template based on action type
        if action_type == ConfirmationType.DESTRUCTIVE:
            template = random.choice(self.destructive_templates)
        elif action_type == ConfirmationType.CAUTIONARY:
            template = random.choice(self.cautionary_templates)
        elif action_type == ConfirmationType.STANDARD:
            template = random.choice(self.standard_templates)
        elif action_type == ConfirmationType.BULK:
            template = random.choice(self.bulk_templates)
        elif action_type == ConfirmationType.SENSITIVE:
            template = random.choice(self.sensitive_templates)
        else:
            # Default to standard
            template = random.choice(self.standard_templates)

        # Format the template with provided information
        formatted_message = template.format(
            action=action,
            action_type=action_type.value,
            action_desc=action_description,
            count=count or 0,
            data_type=data_type or "personal"
        )

        return formatted_message

    def generate_positive_response(self) -> str:
        """
        Generate a positive response after confirmation
        """
        return random.choice(self.positive_responses)

    def generate_negative_response(self) -> str:
        """
        Generate a negative response after cancellation
        """
        return random.choice(self.negative_responses)

    def generate_follow_up_question(self) -> str:
        """
        Generate a follow-up question after completing an action
        """
        return random.choice(self.follow_up_questions)

    def generate_destructive_confirmation(self, action: str, item: str = "the item") -> str:
        """
        Generate a confirmation message for destructive actions
        """
        action_description = f"permanently delete {item}" if "delete" in action.lower() else f"{action} {item}"

        return self.generate_confirmation_message(
            action=action,
            action_type=ConfirmationType.DESTRUCTIVE,
            action_description=action_description
        )

    def generate_bulk_confirmation(self, action: str, count: int, item_type: str = "items") -> str:
        """
        Generate a confirmation message for bulk operations
        """
        action_description = f"{action} {count} {item_type}"

        return self.generate_confirmation_message(
            action=action,
            action_type=ConfirmationType.BULK,
            count=count,
            action_description=action_description
        )

    def generate_sensitive_confirmation(self, action: str, data_type: str = "personal data") -> str:
        """
        Generate a confirmation message for sensitive operations
        """
        action_description = f"access {data_type}" if "access" in action.lower() else f"{action} {data_type}"

        return self.generate_confirmation_message(
            action=action,
            action_type=ConfirmationType.SENSITIVE,
            data_type=data_type,
            action_description=action_description
        )

    def generate_cautionary_confirmation(self, action: str, item: str = "the item") -> str:
        """
        Generate a confirmation message for cautionary actions
        """
        action_description = f"{action} {item}"

        return self.generate_confirmation_message(
            action=action,
            action_type=ConfirmationType.CAUTIONARY,
            action_description=action_description
        )

    def generate_standard_confirmation(self, action: str) -> str:
        """
        Generate a confirmation message for standard actions
        """
        action_description = f"{action}"

        return self.generate_confirmation_message(
            action=action,
            action_type=ConfirmationType.STANDARD,
            action_description=action_description
        )

    def create_confirmation_flow(
        self,
        action: str,
        action_type: ConfirmationType,
        count: Optional[int] = None,
        item: Optional[str] = None,
        data_type: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Create a complete confirmation flow with message, positive and negative responses
        """
        confirmation_message = self.generate_confirmation_message(
            action=action,
            action_type=action_type,
            count=count,
            action_description=f"{action} {item}" if item else action,
            data_type=data_type
        )

        return {
            "confirmation_message": confirmation_message,
            "positive_response": self.generate_positive_response(),
            "negative_response": self.generate_negative_response(),
            "follow_up": self.generate_follow_up_question()
        }

    def get_confirmation_style_options(self) -> Dict[str, str]:
        """
        Get different style options for confirmation messages
        """
        return {
            "direct": "Are you sure you want to {action}? (Y/N)",
            "descriptive": "This will {action_desc} and cannot be undone. Confirm to proceed.",
            "warning": "⚠️ Warning: {action_desc} will permanently change things. Confirm if certain.",
            "polite": "Would you like me to {action} for you? Please confirm.",
            "formal": "This action ({action}) requires your explicit confirmation to proceed."
        }

    def generate_styled_confirmation(
        self,
        action: str,
        style: str = "descriptive",
        action_description: Optional[str] = None
    ) -> str:
        """
        Generate a confirmation message in a specific style
        """
        styles = self.get_confirmation_style_options()

        if style not in styles:
            style = "descriptive"  # Default fallback

        template = styles[style]

        if not action_description:
            action_description = f"perform {action}"

        return template.format(action=action, action_desc=action_description)

    def generate_ranged_confirmation(
        self,
        action: str,
        min_items: int,
        max_items: int,
        item_type: str = "items"
    ) -> str:
        """
        Generate a confirmation for operations affecting a range of items
        """
        if min_items == max_items:
            return self.generate_bulk_confirmation(action, min_items, item_type)
        else:
            action_description = f"{action} between {min_items} and {max_items} {item_type}"
            return self.generate_confirmation_message(
                action=action,
                action_type=ConfirmationType.BULK,
                count=max_items,  # Use max for the template
                action_description=action_description
            )


# Singleton instance
generator = ConfirmationGenerator()


def get_confirmation_generator() -> ConfirmationGenerator:
    """Get the confirmation generator instance"""
    return generator