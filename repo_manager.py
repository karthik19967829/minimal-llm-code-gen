#!/usr/bin/env python3
"""
Repository Manager for LLM Code Generator

Handles git repository operations, cloning, analysis, and multi-file modifications.
"""

import os
import subprocess
import tempfile
import shutil
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
import fnmatch


class RepoManager:
    def __init__(self, work_dir: Optional[str] = None):
        """
        Initialize repository manager.
        
        Args:
            work_dir: Working directory for repository operations
        """
        self.work_dir = work_dir or tempfile.mkdtemp(prefix="llm_repo_")
        self.current_repo = None
        self.repo_path = None
    
    def clone_repository(self, repo_url: str, branch: str = "main") -> str:
        """
        Clone a git repository.
        
        Args:
            repo_url: Git repository URL
            branch: Branch to clone (default: main)
            
        Returns:
            Path to cloned repository
        """
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        clone_path = os.path.join(self.work_dir, repo_name)
        
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)
        
        cmd = ["git", "clone", "-b", branch, repo_url, clone_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Failed to clone repository: {result.stderr}")
        
        self.current_repo = repo_url
        self.repo_path = clone_path
        return clone_path
    
    def analyze_repository(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze repository structure and content.
        
        Args:
            path: Repository path (uses current repo if not provided)
            
        Returns:
            Repository analysis data
        """
        repo_path = path or self.repo_path
        if not repo_path or not os.path.exists(repo_path):
            raise ValueError("No repository path available")
        
        analysis = {
            "path": repo_path,
            "files": [],
            "languages": {},
            "structure": {},
            "size": 0,
            "git_info": {}
        }
        
        # Get git information
        try:
            os.chdir(repo_path)
            
            # Get current branch
            result = subprocess.run(["git", "branch", "--show-current"], 
                                  capture_output=True, text=True)
            analysis["git_info"]["current_branch"] = result.stdout.strip()
            
            # Get remote URL
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                  capture_output=True, text=True)
            analysis["git_info"]["remote_url"] = result.stdout.strip()
            
        except Exception as e:
            analysis["git_info"]["error"] = str(e)
        
        # Analyze file structure
        for root, dirs, files in os.walk(repo_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo_path)
                
                # Get file info
                file_info = {
                    "path": rel_path,
                    "size": os.path.getsize(file_path),
                    "extension": Path(file).suffix.lower()
                }
                
                analysis["files"].append(file_info)
                analysis["size"] += file_info["size"]
                
                # Count languages by extension
                ext = file_info["extension"]
                if ext:
                    analysis["languages"][ext] = analysis["languages"].get(ext, 0) + 1
        
        return analysis
    
    def find_files(self, pattern: str, path: Optional[str] = None) -> List[str]:
        """
        Find files matching a pattern in the repository.
        
        Args:
            pattern: File pattern (e.g., "*.py", "test_*.js")
            path: Repository path (uses current repo if not provided)
            
        Returns:
            List of matching file paths
        """
        repo_path = path or self.repo_path
        if not repo_path:
            raise ValueError("No repository path available")
        
        matches = []
        for root, dirs, files in os.walk(repo_path):
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)
                    matches.append(rel_path)
        
        return matches
    
    def read_file(self, file_path: str, repo_path: Optional[str] = None) -> str:
        """
        Read a file from the repository.
        
        Args:
            file_path: Relative path to file
            repo_path: Repository path (uses current repo if not provided)
            
        Returns:
            File content as string
        """
        repo_path = repo_path or self.repo_path
        if not repo_path:
            raise ValueError("No repository path available")
        
        full_path = os.path.join(repo_path, file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding for binary files
            with open(full_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def write_file(self, file_path: str, content: str, repo_path: Optional[str] = None) -> None:
        """
        Write content to a file in the repository.
        
        Args:
            file_path: Relative path to file
            content: File content
            repo_path: Repository path (uses current repo if not provided)
        """
        repo_path = repo_path or self.repo_path
        if not repo_path:
            raise ValueError("No repository path available")
        
        full_path = os.path.join(repo_path, file_path)
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_branch(self, branch_name: str, repo_path: Optional[str] = None) -> None:
        """
        Create and checkout a new git branch.
        
        Args:
            branch_name: Name of the new branch
            repo_path: Repository path (uses current repo if not provided)
        """
        repo_path = repo_path or self.repo_path
        if not repo_path:
            raise ValueError("No repository path available")
        
        os.chdir(repo_path)
        
        # Create and checkout new branch
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    
    def commit_changes(self, message: str, repo_path: Optional[str] = None) -> None:
        """
        Commit all changes in the repository.
        
        Args:
            message: Commit message
            repo_path: Repository path (uses current repo if not provided)
        """
        repo_path = repo_path or self.repo_path
        if not repo_path:
            raise ValueError("No repository path available")
        
        os.chdir(repo_path)
        
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", message], check=True)
    
    def push_changes(self, branch: Optional[str] = None, repo_path: Optional[str] = None) -> None:
        """
        Push changes to remote repository.
        
        Args:
            branch: Branch to push (current branch if not provided)
            repo_path: Repository path (uses current repo if not provided)
        """
        repo_path = repo_path or self.repo_path
        if not repo_path:
            raise ValueError("No repository path available")
        
        os.chdir(repo_path)
        
        if branch:
            subprocess.run(["git", "push", "-u", "origin", branch], check=True)
        else:
            subprocess.run(["git", "push"], check=True)
    
    def get_repository_context(self, max_files: int = 20) -> str:
        """
        Get repository context for LLM analysis.
        
        Args:
            max_files: Maximum number of files to include in context
            
        Returns:
            Repository context as formatted string
        """
        if not self.repo_path:
            raise ValueError("No repository loaded")
        
        analysis = self.analyze_repository()
        context = []
        
        # Add repository overview
        context.append("=== REPOSITORY ANALYSIS ===")
        context.append(f"Path: {analysis['path']}")
        context.append(f"Total files: {len(analysis['files'])}")
        context.append(f"Size: {analysis['size']} bytes")
        context.append(f"Languages: {', '.join(analysis['languages'].keys())}")
        
        if analysis['git_info']:
            context.append(f"Current branch: {analysis['git_info'].get('current_branch', 'unknown')}")
            context.append(f"Remote: {analysis['git_info'].get('remote_url', 'unknown')}")
        
        context.append("\n=== FILE STRUCTURE ===")
        
        # Add key files (prioritize common important files)
        important_patterns = [
            "README*", "*.md", "package.json", "requirements.txt", 
            "Cargo.toml", "pom.xml", "build.gradle", "Makefile",
            "*.py", "*.js", "*.ts", "*.go", "*.rs", "*.java"
        ]
        
        included_files = set()
        files_added = 0
        
        # First, add important files
        for pattern in important_patterns:
            if files_added >= max_files:
                break
            
            matches = self.find_files(pattern)
            for file_path in matches[:5]:  # Limit per pattern
                if file_path not in included_files and files_added < max_files:
                    try:
                        content = self.read_file(file_path)
                        context.append(f"\n--- {file_path} ---")
                        context.append(content[:2000])  # Limit content length
                        included_files.add(file_path)
                        files_added += 1
                    except Exception:
                        continue
        
        return "\n".join(context)
    
    def cleanup(self) -> None:
        """Clean up temporary directories."""
        if self.work_dir and os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)