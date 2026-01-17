from typing import Dict, List, Optional, Any
from enum import Enum
import re


class ErrorMessageStyle(Enum):
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    DIRECT = "direct"
    SUPPORTIVE = "supportive"


class ErrorMessageGenerator:
    def __init__(self):
        # Templates for different types of errors
        self.error_templates = {
            'user_input_error': {
                'friendly': [
                    "I had a little trouble understanding that. Could you try saying it a different way?",
                    "Hmm, I'm not quite sure what you mean. Could you give me a bit more detail?",
                    "I got a bit lost there. Can you explain that again in a different way?",
                    "I'm having trouble following your request. Could you rephrase that for me?",
                    "That didn't quite come through clearly. What did you mean to say?"
                ],
                'professional': [
                    "I encountered an issue understanding your request. Could you please clarify?",
                    "There seems to be some ambiguity in your request. Please provide additional details.",
                    "I'm unable to process your request as stated. Could you rephrase it?",
                    "I need more specific information to fulfill your request. Could you elaborate?",
                    "Your request requires clarification. Please provide more specific details."
                ],
                'casual': [
                    "Not sure I got that. Mind rephrasing?",
                    "Can you say that a different way? I'm a bit confused.",
                    "Lost me there. Can you break it down for me?",
                    "Say what now? I didn't quite catch that.",
                    "Could you put that in different words? Thanks!"
                ],
                'direct': [
                    "I don't understand your request. Please be more specific.",
                    "Invalid input. Please rephrase your request.",
                    "Unable to process. Provide clearer instructions.",
                    "Request unclear. Please specify what you want.",
                    "Input does not match expected format. Try again."
                ],
                'supportive': [
                    "No worries, these things happen! Could you try rephrasing that?",
                    "Don't worry, I just need a little more clarity. Could you explain that differently?",
                    "It's okay, let's try this again. Could you say that another way?",
                    "Sometimes communication gets tricky. Can you give me more details?",
                    "We all have moments like this. Could you help me understand better?"
                ]
            },
            'system_error': {
                'friendly': [
                    "Oops! Something went sideways on my end. Give me a moment to sort it out.",
                    "Whoops! I hit a bump in the road. Let me see if I can smooth things out.",
                    "Ack! My bad - something went wrong here. I'm looking into it!",
                    "Aw nuts! Something's not working right on my side. Let me fix this.",
                    "Oh dear! I seem to have hit a snag. I'm on it!"
                ],
                'professional': [
                    "A system error has occurred. Our team has been notified and is investigating.",
                    "An unexpected error has occurred on the server side. We're working to resolve it.",
                    "A technical issue has occurred. Our systems are monitoring the situation.",
                    "An internal error has occurred. We're actively working to restore normal operation.",
                    "A server-side error has occurred. Our team is addressing this issue."
                ],
                'casual': [
                    "Dang, something broke on my end. Hold tight while I figure this out.",
                    "Crud! Server's acting up. Lemme see what's happening.",
                    "Ah shoot, hit an error. Working on getting this sorted.",
                    "Server's being stubborn. Gimme a sec to sort this out.",
                    "Well that's not supposed to happen. Let me check this out."
                ],
                'direct': [
                    "A system error occurred. Please try again later.",
                    "Server error. Service temporarily unavailable.",
                    "Technical issue detected. Operation failed.",
                    "Internal server error. Contact support if issue persists.",
                    "System malfunction. Retry operation later."
                ],
                'supportive': [
                    "I know this can be frustrating, but I'm working on resolving this technical issue.",
                    "I understand this isn't ideal. I'm actively working to get things back on track.",
                    "I appreciate your patience as I work through this technical hiccup.",
                    "These things happen sometimes. I'm on top of this and will have it fixed soon.",
                    "Thank you for bearing with me while I resolve this issue."
                ]
            },
            'validation_error': {
                'friendly': [
                    "It looks like some of the information might need a little adjustment. Could you check it?",
                    "I noticed something that might need tweaking. Could you take another look?",
                    "There might be a small issue with the data you provided. Want to review it?",
                    "I think there might be a little mismatch with what you entered. Could you double-check?",
                    "The information you gave me seems a bit off. Could you verify it?"
                ],
                'professional': [
                    "The data provided does not meet the required validation criteria. Please review and correct.",
                    "One or more fields do not meet the expected format or requirements. Please adjust accordingly.",
                    "Validation failed for the submitted data. Please ensure all requirements are met.",
                    "Input validation failed. Please review the submitted information and correct any issues.",
                    "Submitted data does not conform to required format. Please verify and resubmit."
                ],
                'casual': [
                    "The info you sent doesn't quite match what I'm expecting. Wanna double-check?",
                    "Something's not quite right with the data. Can you take another look?",
                    "The format's a bit off. Could you fix up what you sent?",
                    "Not quite matching what I need. Could you tweak that?",
                    "That's not fitting the mold I need. Mind adjusting?"
                ],
                'direct': [
                    "Data validation failed. Correct the input and try again.",
                    "Invalid data format. Follow the required format.",
                    "Validation error. Fix input data and retry.",
                    "Data does not meet requirements. Correct and resubmit.",
                    "Format validation failed. Check input format."
                ],
                'supportive': [
                    "It's easy to make small mistakes. Could you take a look and adjust as needed?",
                    "We all make typos sometimes. Could you review the information you provided?",
                    "No problem at all! Could you just double-check those details?",
                    "These little mismatches happen. Could you verify the information?",
                    "I'm here to help you get this right. Could you review what you entered?"
                ]
            },
            'resource_not_found': {
                'friendly': [
                    "I looked everywhere but couldn't find that. Are you sure it exists?",
                    "I couldn't locate what you're looking for. Maybe it's hiding somewhere else?",
                    "I'm drawing a blank on that one. Are you sure it's there?",
                    "That seems to be missing. Did you mean something else?",
                    "I searched high and low but came up empty-handed. Any other ideas?"
                ],
                'professional': [
                    "The requested resource could not be found. Please verify the resource identifier.",
                    "Resource not located. Please confirm the resource exists and the identifier is correct.",
                    "Requested item not found. Please check the resource name or ID.",
                    "The specified resource does not exist. Verify the resource information.",
                    "Resource lookup failed. Please ensure the resource identifier is accurate."
                ],
                'casual': [
                    "Can't find that anywhere. Did you spell it right?",
                    "Not seeing that anywhere. You sure it's there?",
                    "Nothing's coming up for that. Maybe try a different name?",
                    "That's a no-show. Double-check what you're looking for?",
                    "Drawing a blank. Are you sure that exists?"
                ],
                'direct': [
                    "Resource not found. Verify the identifier.",
                    "Item does not exist. Check resource ID.",
                    "Not found. Invalid resource identifier.",
                    "Resource lookup failed. Check spelling.",
                    "No match found. Verify resource name."
                ],
                'supportive': [
                    "I know it can be frustrating when you can't find something. Let me help you locate it.",
                    "I understand you're looking for something specific. Could we try a different approach?",
                    "I'm sorry I couldn't find what you're looking for. Can I help you find an alternative?",
                    "Sometimes things get misplaced. Let me help you find what you need.",
                    "I wish I had better news. Let me see if I can help you find what you're looking for."
                ]
            },
            'permission_denied': {
                'friendly': [
                    "It looks like you might need special permission for that. Want me to point you in the right direction?",
                    "I think you might need higher access for this. I can help you understand why.",
                    "This one requires special access. Let me explain what's needed.",
                    "You'll need elevated privileges for this action. Can I help explain the process?",
                    "This is a restricted action. Let me guide you on how to get access."
                ],
                'professional': [
                    "Access denied due to insufficient permissions. Contact your system administrator.",
                    "Insufficient privileges to perform this action. Access level upgrade required.",
                    "Permission denied. This action requires elevated access rights.",
                    "Unauthorized access attempt. Proper authorization required for this operation.",
                    "Security clearance insufficient. Higher permission level required."
                ],
                'casual': [
                    "You need higher perms for this. Talk to your admin maybe?",
                    "Not in your access zone. Gotta have more privileges for this.",
                    "Nope, not allowed. Need better access for this one.",
                    "Access denied! Upgrade your permissions first.",
                    "Can't do that. Need higher clearance for this action."
                ],
                'direct': [
                    "Access denied. Insufficient permissions.",
                    "Unauthorized. Upgrade required.",
                    "Permission denied. Cannot proceed.",
                    "Insufficient privileges. Access rejected.",
                    "Forbidden. Higher access required."
                ],
                'supportive': [
                    "I understand you need this access. Let me help you understand how to get the proper permissions.",
                    "I know this can be frustrating. Let me guide you on how to obtain the necessary access.",
                    "I'm here to help you navigate the permission process.",
                    "I wish I could grant access directly. Let me show you the right path.",
                    "This is just a process, not a rejection. Let me help you with the next steps."
                ]
            }
        }

        # Generic fallback messages
        self.generic_messages = {
            'friendly': "I seem to have hit a bit of a snag. Could you help me understand what you need?",
            'professional': "An unexpected condition has occurred. Please provide additional clarification.",
            'casual': "Something's not right here. Wanna try again?",
            'direct': "Operation failed. Please retry with corrected input.",
            'supportive': "I'm here to help you work through this. What specifically do you need assistance with?"
        }

    def generate_error_message(
        self,
        error_type: str,
        style: ErrorMessageStyle = ErrorMessageStyle.FRIENDLY,
        custom_context: Optional[str] = None
    ) -> str:
        """
        Generate a user-friendly error message based on error type and style
        """
        # Normalize error type
        normalized_type = self._normalize_error_type(error_type)

        # Get style string
        style_str = style.value

        # Look for the specific error type and style
        if normalized_type in self.error_templates:
            if style_str in self.error_templates[normalized_type]:
                # Select a random message from the list
                import random
                message = random.choice(self.error_templates[normalized_type][style_str])

                # Add custom context if provided
                if custom_context:
                    message += f" Specifically: {custom_context}"

                return message

        # If not found, use generic message
        return self.generic_messages.get(style_str, self.generic_messages['friendly'])

    def _normalize_error_type(self, error_type: str) -> str:
        """
        Normalize error type to match known categories
        """
        error_type_lower = error_type.lower()

        # Map various error type expressions to our known categories
        if any(keyword in error_type_lower for keyword in [
            'input', 'understand', 'parse', 'invalid', 'format', 'malformed', 'syntax'
        ]):
            return 'user_input_error'

        if any(keyword in error_type_lower for keyword in [
            'system', 'server', 'internal', 'runtime', 'connection', 'database', 'timeout'
        ]):
            return 'system_error'

        if any(keyword in error_type_lower for keyword in [
            'validate', 'validation', 'check', 'criteria', 'requirement', 'constraint'
        ]):
            return 'validation_error'

        if any(keyword in error_type_lower for keyword in [
            'not found', 'missing', 'unknown', 'does not exist', '404', 'lookup', 'search'
        ]):
            return 'resource_not_found'

        if any(keyword in error_type_lower for keyword in [
            'permission', 'access', 'authorize', 'forbidden', 'unauthorized', 'denied', 'privilege'
        ]):
            return 'permission_denied'

        # Default to user input error if no match
        return 'user_input_error'

    def generate_multiple_messages(
        self,
        error_type: str,
        styles: List[ErrorMessageStyle],
        count_per_style: int = 1
    ) -> Dict[str, List[str]]:
        """
        Generate multiple error messages in different styles
        """
        result = {}
        for style in styles:
            messages = []
            for _ in range(count_per_style):
                msg = self.generate_error_message(error_type, style)
                messages.append(msg)
            result[style.value] = messages
        return result

    def customize_message(
        self,
        base_message: str,
        tone_adjective: str,
        add_empathy: bool = False,
        add_guidance: bool = False
    ) -> str:
        """
        Customize a base message with specific tone and additional elements
        """
        result = base_message

        # Add empathetic language if requested
        if add_empathy:
            empathetic_prefixes = [
                "I understand this might be frustrating, ",
                "I know this isn't ideal, but ",
                "I apologize for the inconvenience, ",
                "I appreciate your patience, "
            ]
            import random
            result = random.choice(empathetic_prefixes) + result

        # Add guidance if requested
        if add_guidance:
            guidance_suffixes = [
                " Please try again with different input.",
                " Consider rephrasing your request.",
                " You might want to check the format of your input.",
                " Feel free to ask for help if you need clarification.",
                " Don't hesitate to reach out if you need assistance."
            ]
            import random
            result += random.choice(guidance_suffixes)

        return result

    def generate_contextual_message(
        self,
        error_type: str,
        user_action: str,
        affected_item: str,
        style: ErrorMessageStyle = ErrorMessageStyle.FRIENDLY
    ) -> str:
        """
        Generate an error message that includes context about what the user was trying to do
        """
        base_message = self.generate_error_message(error_type, style)

        # Add contextual information
        context_part = f" when trying to {user_action}"
        if affected_item:
            context_part += f" {affected_item}"

        # Insert context into the message
        import random
        insertion_points = [
            f"I encountered an issue{context_part}. {base_message}",
            f"{base_message} I ran into problems{context_part}.",
            f"{base_message} The issue occurred{context_part}."
        ]

        return random.choice(insertion_points)

    def get_message_variants(self, error_type: str) -> Dict[str, str]:
        """
        Get the same message in all available styles
        """
        variants = {}
        for style in ErrorMessageStyle:
            variants[style.value] = self.generate_error_message(error_type, style)
        return variants


# Singleton instance
generator = ErrorMessageGenerator()


def get_error_message_generator() -> ErrorMessageGenerator:
    """Get the error message generator instance"""
    return generator