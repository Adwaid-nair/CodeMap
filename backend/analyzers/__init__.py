from .python_analyzer import PythonAnalyzer
from .java_analyzer import JavaAnalyzer
from .cpp_analyzer import CppAnalyzer

def get_analyzer(language, project_path):
    if language.lower() == "python":
        return PythonAnalyzer(project_path)
    elif language.lower() == "java":
        return JavaAnalyzer(project_path)
    elif language.lower() in ["cpp", "c++"]:
        return CppAnalyzer(project_path)
    else:
        return None
