"use client";

import ReactMarkdown from "react-markdown";
import { Message } from "@/types";
import { CodeBlock } from "./CodeBlock";
import { cn } from "@/lib/utils";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={cn("flex gap-3 mb-4", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
          AI
        </div>
      )}

      <div
        className={cn(
          "max-w-[80%] rounded-lg px-4 py-3",
          isUser
            ? "bg-primary-500 text-white"
            : "bg-gray-100 text-gray-900"
        )}
      >
        {message.agentName && !isUser && (
          <div className="text-xs text-gray-500 mb-1">{message.agentName}</div>
        )}

        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <ReactMarkdown
            components={{
              code({ node, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || "");
                const codeString = String(children).replace(/\n$/, "");

                if (match) {
                  return <CodeBlock language={match[1]}>{codeString}</CodeBlock>;
                }

                return (
                  <code className="bg-gray-200 px-1 py-0.5 rounded text-sm" {...props}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-700 text-sm font-bold flex-shrink-0">
          U
        </div>
      )}
    </div>
  );
}
