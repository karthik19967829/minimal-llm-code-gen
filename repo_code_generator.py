#!/usr/bin/env python3
"""
Repository-level LLM Code Generator

Extends the basic LLM code generator to work with entire repositories,
perform multi-file analysis and modifications.
"""

import os
import json
from typing import Dict, List, Optional, Any
from llm_code_generator import LLMCodeGenerator
from repo_manager import RepoManager
from config_reader import load_config


class RepoCodeGenerator(LLMCodeGenerator):
    def __init__(self, api_key: Optional[str] = None, model: str = "openai"):
        """
        Initialize repository-level code generator.
        
        Args:
            api_key: API key (optional, will load from config if not provided)
            model: Model provider to use (openai, claude, gemini)
        """
        super().__init__(api_key, model)
        self.repo_manager = RepoManager()
    
    def analyze_repository(self, repo_url: str, branch: str = "main") -> Dict[str, Any]:
        """
        Clone and analyze a repository.
        
        Args:
            repo_url: Git repository URL
            branch: Branch to analyze
            
        Returns:
            Repository analysis results
        """
        print(f"Cloning repository: {repo_url}")
        clone_path = self.repo_manager.clone_repository(repo_url, branch)
        
        print("Analyzing repository structure...")
        analysis = self.repo_manager.analyze_repository()
        
        return analysis
    
    def generate_repository_summary(self, repo_url: str, branch: str = "main") -> str:
        """
        Generate a comprehensive summary of a repository using LLM.
        
        Args:
            repo_url: Git repository URL
            branch: Branch to analyze
            
        Returns:
            LLM-generated repository summary
        """
        # Get repository context
        self.analyze_repository(repo_url, branch)
        context = self.repo_manager.get_repository_context()
        
        prompt = f"""
Analyze this repository and provide a comprehensive summary:

{context}

Please provide:
1. Project overview and purpose
2. Main technologies and frameworks used
3. Architecture and structure analysis
4. Key components and their relationships
5. Potential improvements or issues
6. Development recommendations

Make your analysis detailed but concise.
"""
        
        return self.generate_code(prompt)
    
    def suggest_improvements(self, repo_url: str, focus_area: str = "", branch: str = "main") -> str:
        """
        Generate improvement suggestions for a repository.
        
        Args:
            repo_url: Git repository URL
            focus_area: Specific area to focus on (e.g., "performance", "security", "testing")
            branch: Branch to analyze
            
        Returns:
            LLM-generated improvement suggestions
        """
        self.analyze_repository(repo_url, branch)
        context = self.repo_manager.get_repository_context()
        
        focus_text = f"Focus specifically on: {focus_area}" if focus_area else "Consider all aspects"
        
        prompt = f"""
Analyze this repository and suggest specific improvements:

{context}

{focus_text}

Please provide:
1. Code quality improvements
2. Architecture enhancements
3. Performance optimizations
4. Security considerations
5. Testing improvements
6. Documentation suggestions
7. Specific code changes with examples

Provide actionable recommendations with code examples where applicable.
"""
        
        return self.generate_code(prompt)
    
    def implement_feature(self, repo_url: str, feature_description: str, 
                         branch: str = "main", create_pr: bool = False) -> Dict[str, Any]:
        """
        Implement a new feature across multiple files in a repository.
        
        Args:
            repo_url: Git repository URL
            feature_description: Description of feature to implement
            branch: Base branch to work from
            create_pr: Whether to create a new branch and prepare for PR
            
        Returns:
            Implementation results including modified files
        """
        # Analyze repository
        self.analyze_repository(repo_url, branch)
        context = self.repo_manager.get_repository_context()
        
        # Create new branch if requested
        if create_pr:
            feature_branch = f"feature/{feature_description.lower().replace(' ', '-')[:30]}"
            self.repo_manager.create_branch(feature_branch)
        
        # Generate implementation plan
        prompt = f"""
Based on this repository structure, implement the following feature:

FEATURE: {feature_description}

REPOSITORY CONTEXT:
{context}

Please provide a detailed implementation plan with:
1. List of files to modify/create
2. Specific code changes for each file
3. Any new dependencies or configurations needed
4. Testing considerations

Format your response as JSON with this structure:
{{
    "plan": "Overall implementation strategy",
    "files": [
        {{
            "path": "relative/path/to/file.py",
            "action": "create|modify",
            "content": "complete file content",
            "description": "what this file does"
        }}
    ],
    "dependencies": ["list", "of", "new", "dependencies"],
    "tests": ["list", "of", "test", "files", "to", "create"],
    "notes": "additional implementation notes"
}}
"""
        
        print("Generating implementation plan...")
        implementation_response = self.generate_code(prompt)
        
        try:
            # Parse JSON response
            implementation = json.loads(implementation_response)
            
            # Apply file changes
            modified_files = []
            for file_info in implementation.get("files", []):
                file_path = file_info["path"]
                content = file_info["content"]
                
                print(f"{'Creating' if file_info['action'] == 'create' else 'Modifying'}: {file_path}")
                self.repo_manager.write_file(file_path, content)
                modified_files.append(file_path)
            
            # Commit changes if in PR mode
            if create_pr:
                commit_message = f"Implement {feature_description}\n\nGenerated implementation including:\n"
                for file_info in implementation.get("files", []):
                    commit_message += f"- {file_info['action'].title()} {file_info['path']}\n"
                
                self.repo_manager.commit_changes(commit_message)
                print(f"Changes committed to branch: {feature_branch}")
            
            return {
                "success": True,
                "implementation": implementation,
                "modified_files": modified_files,
                "branch": feature_branch if create_pr else branch,
                "repo_path": self.repo_manager.repo_path
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse implementation response: {e}",
                "raw_response": implementation_response
            }
    
    def fix_issues(self, repo_url: str, issue_description: str, 
                   branch: str = "main", create_pr: bool = False) -> Dict[str, Any]:
        """
        Fix issues in a repository based on description.
        
        Args:
            repo_url: Git repository URL
            issue_description: Description of issues to fix
            branch: Base branch to work from
            create_pr: Whether to create a new branch and prepare for PR
            
        Returns:
            Fix results including modified files
        """
        # Analyze repository
        self.analyze_repository(repo_url, branch)
        context = self.repo_manager.get_repository_context()
        
        # Create new branch if requested
        if create_pr:
            fix_branch = f"fix/{issue_description.lower().replace(' ', '-')[:30]}"
            self.repo_manager.create_branch(fix_branch)
        
        # Generate fix plan
        prompt = f"""
Analyze this repository and fix the following issues:

ISSUES: {issue_description}

REPOSITORY CONTEXT:
{context}

Please provide specific fixes with:
1. Identification of the problems
2. Root cause analysis
3. Specific code changes needed
4. Files to modify

Format your response as JSON with this structure:
{{
    "analysis": "problem analysis and root causes",
    "fixes": [
        {{
            "file": "path/to/file.py",
            "issue": "description of issue in this file",
            "solution": "description of fix",
            "content": "complete fixed file content"
        }}
    ],
    "tests": ["suggested test changes"],
    "notes": "additional notes about the fixes"
}}
"""
        
        print("Analyzing issues and generating fixes...")
        fix_response = self.generate_code(prompt)
        
        try:
            # Parse JSON response
            fixes = json.loads(fix_response)
            
            # Apply fixes
            fixed_files = []
            for fix_info in fixes.get("fixes", []):
                file_path = fix_info["file"]
                content = fix_info["content"]
                
                print(f"Fixing: {file_path} - {fix_info['issue']}")
                self.repo_manager.write_file(file_path, content)
                fixed_files.append(file_path)
            
            # Commit changes if in PR mode
            if create_pr:
                commit_message = f"Fix: {issue_description}\n\n"
                commit_message += fixes.get("analysis", "") + "\n\n"
                for fix_info in fixes.get("fixes", []):
                    commit_message += f"- {fix_info['file']}: {fix_info['solution']}\n"
                
                self.repo_manager.commit_changes(commit_message)
                print(f"Fixes committed to branch: {fix_branch}")
            
            return {
                "success": True,
                "fixes": fixes,
                "fixed_files": fixed_files,
                "branch": fix_branch if create_pr else branch,
                "repo_path": self.repo_manager.repo_path
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Failed to parse fix response: {e}",
                "raw_response": fix_response
            }
    
    def cleanup(self):
        """Clean up temporary resources."""
        self.repo_manager.cleanup()