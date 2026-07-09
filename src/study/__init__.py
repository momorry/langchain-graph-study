from pathlib import Path


def _find_project_root(marker: str = "pyproject.toml") -> Path:
    """从当前文件向上查找标记文件，定位项目根目录"""
    current = Path(__file__).resolve().parent
    for parent in [current, *current.parents]:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"无法找到包含 {marker} 的项目根目录")


PROJECT_ROOT = _find_project_root()
