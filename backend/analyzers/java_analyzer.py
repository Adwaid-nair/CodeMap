from .base import BaseAnalyzer
import os

try:
    import javalang
except ImportError:
    javalang = None

class JavaAnalyzer(BaseAnalyzer):
    def analyze(self):
        if not javalang:
            return {"error": "javalang library not installed"}

        nodes = []
        edges = []
        file_metrics = {}
        
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".java"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.project_path)
                    
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        tree = javalang.parse.parse(content)
                        
                        # Extract classes and methods
                        for path, node in tree.filter(javalang.tree.ClassDeclaration):
                            class_id = f"{rel_path}:{node.name}"
                            nodes.append({"id": class_id, "label": node.name, "type": "class"})
                            
                            for method in node.methods:
                                method_id = f"{class_id}:{method.name}"
                                nodes.append({"id": method_id, "label": method.name, "type": "method"})
                                edges.append({"source": class_id, "target": method_id, "type": "contains"})
                                
                                # Simplified complexity: count statements?
                                # Javalang doesn't have built-in CC, would need custom visitor.
                                # Skipping CC for MVP Java.
                                
                    except Exception as e:
                        print(f"Error parsing {rel_path}: {e}")

        return {
            "nodes": nodes,
            "edges": edges,
            "complexity": {"note": "Java complexity not yet implemented"}
        }
