'use client';

import { ChatMessage } from '@/types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
  isOwnMessage?: boolean;
}

export default function MessageBubble({ message, isOwnMessage = false }: MessageBubbleProps) {
  const messageClass = isOwnMessage
    ? 'ml-auto bg-blue-500 text-white rounded-br-none'
    : 'mr-auto bg-gray-200 text-gray-800 rounded-bl-none';

  const containerClass = isOwnMessage ? 'justify-end' : 'justify-start';

  // Determine status indicator
  let statusIndicator = '';
  if (message.status === 'error') {
    statusIndicator = '❌';
  } else if (message.status === 'delivered') {
    statusIndicator = '✓✓';
  } else if (message.status === 'sent') {
    statusIndicator = '✓';
  }

  return (
    <div className={`flex ${containerClass} mb-4 opacity-0 animate-fadeInSlideUp`}>
      <div className={`max-w-xs md:max-w-md px-4 py-2 rounded-lg ${messageClass} transition-all duration-300 ease-in-out`}>
        <div className="text-sm">{message.content}</div>
        <div className="flex justify-between items-center mt-1 text-xs opacity-70 transition-all duration-300 ease-in-out">
          <span>
            {message.timestamp instanceof Date
              ? message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              : new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
          {statusIndicator && (
            <span className="ml-2 transition-all duration-300 ease-in-out">{statusIndicator}</span>
          )}
        </div>
      </div>
    </div>
  );
}