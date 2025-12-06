import git
import os

class GitAnalyzer:
    def __init__(self, project_path):
        self.project_path = project_path

    def get_commit_count(self):
        try:
            # Check if .git exists
            if not os.path.exists(os.path.join(self.project_path, '.git')):
                return None
            
            repo = git.Repo(self.project_path)
            return len(list(repo.iter_commits()))
        except Exception as e:
            print(f"Git analysis failed: {e}")
            return None
