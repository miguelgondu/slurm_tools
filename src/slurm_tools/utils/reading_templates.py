from pathlib import Path
from typing import Literal

from jinja2 import Template

from slurm_tools.templates import __file__ as templates_path


def read_template(template_name: Literal["array_template"]) -> Template:
    SLURM_UTILS_DIR = Path(templates_path).parent
    with open(SLURM_UTILS_DIR / f"{template_name}.sht", "r") as f:
        return Template(f.read())
