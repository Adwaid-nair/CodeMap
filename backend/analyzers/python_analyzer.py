import os
import ast
from .base import BaseAnalyzer
from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor

class PythonAnalyzer(BaseAnalyzer):
    def analyze(self):
        nodes = []
        edges = []
        file_metrics = {}
        total_cc = 0
        count = 0

        # Walk through python files
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.project_path)
                    
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                        # AST Analysis (Simplified Call Graph)
                        tree = ast.parse(content)
                        visitor = CallGraphVisitor(rel_path)
                        visitor.visit(tree)
                        
                        nodes.extend(visitor.nodes)
                        edges.extend(visitor.edges)
                        
                        # Complexity Analysis
                        cv = ComplexityVisitor.from_code(content)
                        file_cc = sum([f.complexity for f in cv.functions]) + (cv.complexity if hasattr(cv, 'complexity') else 0)
                        
                        file_metrics[rel_path] = file_cc
                        total_cc += file_cc
                        count += 1
                        
                    except Exception as e:
                        print(f"Error analyzing {rel_path}: {e}")

        return {
            "nodes": nodes,
            "edges": edges,
            "complexity": {
                "file_metrics": file_metrics,
                "average_complexity": total_cc / count if count > 0 else 0
            }
        }

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.nodes = []
        self.edges = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        func_id = f"{self.filename}:{node.name}"
        self.nodes.append({"id": func_id, "label": node.name, "type": "function", "file": self.filename})
        
        previous_function = self.current_function
        self.current_function = func_id
        
        self.generic_visit(node)
        
        self.current_function = previous_function

    def visit_Call(self, node):
        if self.current_function:
            # Try to resolve call name
            callee = self._get_func_name(node)
            if callee:
                # We often don't know the exact file of the callee without deeper analysis/symbol table
                # For now, we assume it's an external call or create a loose node
                # To keep graph clean, we might only track if we can guess it's local, or just node name
                
                # Simplified: Edge to a node named 'callee' (might duplicate if not careful)
                # Ideally we want to link to existing definitions. 
                # For this MVP, we create an edge to the name.
                
                target_id = f"unknown:{callee}" # Placeholder
                self.edges.append({"source": self.current_function, "target": callee}) # Just use name for target for now

    def _get_func_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None
