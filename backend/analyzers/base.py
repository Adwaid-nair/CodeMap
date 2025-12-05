from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAnalyzer(ABC):
    def __init__(self, project_path: str):
        self.project_path = project_path

    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """
        Perform analysis and return a dictionary containing:
        - nodes: List[Dict] (graph nodes)
        - edges: List[Dict] (graph edges)
        - complexity: Dict (metrics)
        """
        pass
