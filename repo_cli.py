#!/usr/bin/env python3
"""
Command Line Interface for Repository-level LLM Code Generator

Main entry point for repository operations.
"""

import argparse
import sys
import json
from repo_code_generator import RepoCodeGenerator


def main():
    parser = argparse.ArgumentParser(description="LLM-powered repository code generator")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a repository')
    analyze_parser.add_argument('repo_url', help='Git repository URL')
    analyze_parser.add_argument('--branch', default='main', help='Branch to analyze')
    analyze_parser.add_argument('--model', default='openai', help='Model provider to use')
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Generate repository summary')
    summary_parser.add_argument('repo_url', help='Git repository URL')
    summary_parser.add_argument('--branch', default='main', help='Branch to analyze')
    summary_parser.add_argument('--model', default='openai', help='Model provider to use')
    
    # Improve command
    improve_parser = subparsers.add_parser('improve', help='Suggest improvements')
    improve_parser.add_argument('repo_url', help='Git repository URL')
    improve_parser.add_argument('--focus', default='', help='Focus area (e.g., performance, security)')
    improve_parser.add_argument('--branch', default='main', help='Branch to analyze')
    improve_parser.add_argument('--model', default='openai', help='Model provider to use')
    
    # Feature command
    feature_parser = subparsers.add_parser('feature', help='Implement a new feature')
    feature_parser.add_argument('repo_url', help='Git repository URL')
    feature_parser.add_argument('description', help='Feature description')
    feature_parser.add_argument('--branch', default='main', help='Base branch')
    feature_parser.add_argument('--create-pr', action='store_true', help='Create new branch for PR')
    feature_parser.add_argument('--model', default='openai', help='Model provider to use')
    
    # Fix command
    fix_parser = subparsers.add_parser('fix', help='Fix issues in repository')
    fix_parser.add_argument('repo_url', help='Git repository URL')
    fix_parser.add_argument('description', help='Issue description')
    fix_parser.add_argument('--branch', default='main', help='Base branch')
    fix_parser.add_argument('--create-pr', action='store_true', help='Create new branch for PR')
    fix_parser.add_argument('--model', default='openai', help='Model provider to use')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        generator = RepoCodeGenerator(model=args.model)
        
        if args.command == 'analyze':
            print(f"Analyzing repository: {args.repo_url}")
            analysis = generator.analyze_repository(args.repo_url, args.branch)
            
            print("\n" + "="*60)
            print("REPOSITORY ANALYSIS")
            print("="*60)
            print(f"Path: {analysis['path']}")
            print(f"Files: {len(analysis['files'])}")
            print(f"Size: {analysis['size']} bytes")
            print(f"Languages: {', '.join(analysis['languages'].keys())}")
            
            if analysis.get('git_info'):
                print(f"Branch: {analysis['git_info'].get('current_branch', 'unknown')}")
                print(f"Remote: {analysis['git_info'].get('remote_url', 'unknown')}")
            
            print(f"\nTop file types:")
            for ext, count in sorted(analysis['languages'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {ext}: {count} files")
        
        elif args.command == 'summary':
            print(f"Generating summary for: {args.repo_url}")
            summary = generator.generate_repository_summary(args.repo_url, args.branch)
            
            print("\n" + "="*60)
            print("REPOSITORY SUMMARY")
            print("="*60)
            print(summary)
        
        elif args.command == 'improve':
            print(f"Generating improvements for: {args.repo_url}")
            if args.focus:
                print(f"Focus area: {args.focus}")
            
            improvements = generator.suggest_improvements(args.repo_url, args.focus, args.branch)
            
            print("\n" + "="*60)
            print("IMPROVEMENT SUGGESTIONS")
            print("="*60)
            print(improvements)
        
        elif args.command == 'feature':
            print(f"Implementing feature in: {args.repo_url}")
            print(f"Feature: {args.description}")
            
            result = generator.implement_feature(
                args.repo_url, 
                args.description, 
                args.branch, 
                args.create_pr
            )
            
            print("\n" + "="*60)
            print("FEATURE IMPLEMENTATION")
            print("="*60)
            
            if result['success']:
                print("✅ Feature implemented successfully!")
                print(f"Modified files: {', '.join(result['modified_files'])}")
                print(f"Working in: {result['repo_path']}")
                
                if args.create_pr:
                    print(f"Created branch: {result['branch']}")
                    print("Ready for push and PR creation!")
                
                # Show implementation details
                impl = result['implementation']
                if impl.get('plan'):
                    print(f"\nImplementation plan:\n{impl['plan']}")
                
                if impl.get('dependencies'):
                    print(f"\nNew dependencies: {', '.join(impl['dependencies'])}")
                
            else:
                print("❌ Feature implementation failed!")
                print(f"Error: {result['error']}")
                if result.get('raw_response'):
                    print(f"Raw response:\n{result['raw_response']}")
        
        elif args.command == 'fix':
            print(f"Fixing issues in: {args.repo_url}")
            print(f"Issues: {args.description}")
            
            result = generator.fix_issues(
                args.repo_url, 
                args.description, 
                args.branch, 
                args.create_pr
            )
            
            print("\n" + "="*60)
            print("ISSUE FIXES")
            print("="*60)
            
            if result['success']:
                print("✅ Issues fixed successfully!")
                print(f"Fixed files: {', '.join(result['fixed_files'])}")
                print(f"Working in: {result['repo_path']}")
                
                if args.create_pr:
                    print(f"Created branch: {result['branch']}")
                    print("Ready for push and PR creation!")
                
                # Show fix details
                fixes = result['fixes']
                if fixes.get('analysis'):
                    print(f"\nProblem analysis:\n{fixes['analysis']}")
                
                print(f"\nFixes applied:")
                for fix_info in fixes.get('fixes', []):
                    print(f"- {fix_info['file']}: {fix_info['solution']}")
                
            else:
                print("❌ Issue fixing failed!")
                print(f"Error: {result['error']}")
                if result.get('raw_response'):
                    print(f"Raw response:\n{result['raw_response']}")
        
        # Cleanup
        generator.cleanup()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()