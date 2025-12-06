from .python_analyzer import PythonAnalyzer
from .java_analyzer import JavaAnalyzer
from .cpp_analyzer import CppAnalyzer
from .git_analyzer import GitAnalyzer

def get_analyzer(language, project_path):
    if language.lower() == "python":
        return PythonAnalyzer(project_path)
    elif language.lower() == "java":
        return JavaAnalyzer(project_path)
    elif language.lower() in ["cpp", "c++"]:
        return CppAnalyzer(project_path)
    else:
        return None

def get_git_analyzer(project_path):
    return GitAnalyzer(project_path)
