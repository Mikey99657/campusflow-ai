// Message types
export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  agentName?: string;
  timestamp: Date;
}

// Chat types
export interface ChatRequest {
  message: string;
  conversationId?: number;
  agentType?: string;
}

export interface StreamEvent {
  event: "agent_thinking" | "agent_message" | "tool_call" | "agent_done" | "done" | "error";
  data: {
    agent?: string;
    content?: string;
    delta?: string;
    tool?: string;
    input?: string;
    output?: string;
    message?: string;
    conversationId?: number;
    status?: string;
  };
}

// Task types
export interface Task {
  id: number;
  title: string;
  description?: string;
  taskType: string;
  status: "pending" | "decomposing" | "running" | "completed" | "failed";
  priority: number;
  result?: string;
  errorMessage?: string;
  createdAt: string;
  startedAt?: string;
  completedAt?: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  taskType: string;
}

// Agent types
export interface AgentInfo {
  name: string;
  description: string;
  capabilities: string[];
}
