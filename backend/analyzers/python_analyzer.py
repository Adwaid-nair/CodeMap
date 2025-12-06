import os
import ast
from .base import BaseAnalyzer
from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor

class PythonAnalyzer(BaseAnalyzer):
    def analyze(self):
        nodes = []
        raw_edges = []
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
                        raw_edges.extend(visitor.calls)
                        
                        # Complexity Analysis
                        cv = ComplexityVisitor.from_code(content)
                        file_cc = sum([f.complexity for f in cv.functions]) + (cv.complexity if hasattr(cv, 'complexity') else 0)
                        
                        file_metrics[rel_path] = file_cc
                        total_cc += file_cc
                        count += 1
                        
                    except Exception as e:
                        print(f"Error analyzing {rel_path}: {e}")

        # Post-processing: Resolve edges
        # 1. Map function names to IDs (Simple approach: first match wins)
        #    In a real system, we'd need imports/scopes to resolve correctly.
        func_map = {}
        for n in nodes:
            # key: function name, value: node ID
            # If multiple functions have same name, we overwrite (limitation of MVP)
            func_map[n['label']] = n['id']

        final_edges = []
        existing_node_ids = set(n['id'] for n in nodes)

        for src, target_name in raw_edges:
            target_id = None
            
            if target_name in func_map:
                target_id = func_map[target_name]
            else:
                # External or unparsed function
                target_id = f"external:{target_name}"
                if target_id not in existing_node_ids:
                    nodes.append({
                        "id": target_id,
                        "label": target_name,
                        "type": "external",
                        "style": { "background": "#475569", "border": "1px dashed #94a3b8" }
                    })
                    existing_node_ids.add(target_id)
            
            final_edges.append({
                "source": src,
                "target": target_id,
                "animated": True
            })

        return {
            "nodes": nodes,
            "edges": final_edges,
            "complexity": {
                "file_metrics": file_metrics,
                "average_complexity": total_cc / count if count > 0 else 0
            },
            "issues": {
                "count": sum(1 for val in file_metrics.values() if val > 10),
                "threshold": 10
            }
        }

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.nodes = []
        self.calls = [] # (source_id, target_name)
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
            callee = self._get_func_name(node)
            if callee:
                self.calls.append((self.current_function, callee))

    def _get_func_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None
