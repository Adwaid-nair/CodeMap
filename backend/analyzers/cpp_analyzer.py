from .base import BaseAnalyzer
import os

try:
    from clang.cindex import Index, CursorKind
except ImportError:
    Index = None

class CppAnalyzer(BaseAnalyzer):
    def analyze(self):
        if not Index:
            return {"error": "clang/libclang not installed"}

        nodes = []
        edges = []
        
        try:
            index = Index.create()
            for root, dirs, files in os.walk(self.project_path):
                for file in files:
                    if file.endswith((".cpp", ".h", ".hpp", ".c")):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, self.project_path)
                        
                        tu = index.parse(full_path)
                        self._visit_cursor(tu.cursor, rel_path, nodes, edges)
        except Exception as e:
            return {"error": str(e)}

        return {
            "nodes": nodes,
            "edges": edges,
            "complexity": {"note": "C++ complexity not implemented"}
        }

    def _visit_cursor(self, cursor, rel_path, nodes, edges, parent_id=None):
        current_id = None
        
        if cursor.kind in [CursorKind.CLASS_DECL, CursorKind.FUNCTION_DECL, CursorKind.CXX_METHOD]:
            name = cursor.spelling
            if name:
                current_id = f"{rel_path}:{name}"
                kind_str = "class" if cursor.kind == CursorKind.CLASS_DECL else "function"
                nodes.append({"id": current_id, "label": name, "type": kind_str})
                
                if parent_id:
                    edges.append({"source": parent_id, "target": current_id, "type": "contains"})

        # Recurse
        for child in cursor.get_children():
            self._visit_cursor(child, rel_path, nodes, edges, current_id or parent_id)
