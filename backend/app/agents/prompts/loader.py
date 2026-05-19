from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Template directory
TEMPLATES_DIR = Path(__file__).parent / "templates"

# Jinja2 environment
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    trim_blocks=True,
    lstrip_blocks=True,
)


def load_prompt(template_name: str, **kwargs) -> str:
    """Load and render a prompt template.

    Args:
        template_name: Template filename without .j2 extension
        **kwargs: Variables to pass to the template

    Returns:
        Rendered prompt string
    """
    template = _env.get_template(f"{template_name}.j2")
    return template.render(**kwargs)


def list_templates() -> list[str]:
    """List all available prompt templates."""
    return [f.stem for f in TEMPLATES_DIR.glob("*.j2")]
