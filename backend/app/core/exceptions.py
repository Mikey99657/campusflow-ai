class CampusFlowError(Exception):
    """Base exception for CampusFlow AI."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class AgentError(CampusFlowError):
    """Agent execution error."""

    def __init__(self, message: str, agent_name: str = "unknown"):
        super().__init__(message, code="AGENT_ERROR")
        self.agent_name = agent_name


class LLMError(CampusFlowError):
    """LLM API error."""

    def __init__(self, message: str):
        super().__init__(message, code="LLM_ERROR")


class TaskError(CampusFlowError):
    """Task execution error."""

    def __init__(self, message: str):
        super().__init__(message, code="TASK_ERROR")


class NotFoundError(CampusFlowError):
    """Resource not found."""

    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} with id '{id}' not found", code="NOT_FOUND")


class ValidationError(CampusFlowError):
    """Validation error."""

    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")
