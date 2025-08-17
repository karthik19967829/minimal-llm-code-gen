#!/usr/bin/env python3
"""
LLM Code Generator and Executor

This script takes a problem statement, generates code using an LLM API,
and executes the generated code safely.
"""

import sys
import subprocess
import tempfile
import os
import json
import argparse
from typing import Optional, Dict, Any
import requests
from config_reader import load_config


class LLMCodeGenerator:
    def __init__(self, api_key: Optional[str] = None, model: str = "openai"):
        """
        Initialize the LLM Code Generator
        
        Args:
            api_key: API key (optional, will load from config if not provided)
            model: Model provider to use (openai, claude, gemini)
        """
        try:
            config = load_config()
            if api_key:
                self.api_key = api_key
                self.model = config.get_model_config("openai")["model_name"]
                self.api_url = config.get_model_config("openai")["api_url"]
            else:
                model_config = config.get_model_config(model)
                self.api_key = model_config["api_key"]
                self.model = model_config["model_name"]
                self.api_url = model_config["api_url"]
        except Exception as e:
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.model = "gpt-3.5-turbo"
            self.api_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("API key is required. Add it to config.json or set environment variable.")
    
    def generate_code(self, problem_statement: str) -> str:
        """
        Generate Python code for the given problem statement using LLM
        
        Args:
            problem_statement: Description of the problem to solve
            
        Returns:
            Generated Python code as string
        """
        prompt = f"""
You are a Python code generator. Given a problem statement, generate clean, executable Python code.

Problem: {problem_statement}

Requirements:
1. Generate only Python code that solves the problem
2. Include necessary imports
3. Add a main function or execution block
4. Make the code self-contained and executable
5. Do not include explanations or markdown formatting
6. Ensure the code is safe and doesn't perform harmful operations

Generate the Python code:
"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_completion_tokens": 2000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            generated_code = result["choices"][0]["message"]["content"].strip()
            
            # Clean up the code (remove markdown formatting if present)
            if generated_code.startswith("```python"):
                generated_code = generated_code[9:]
            if generated_code.startswith("```"):
                generated_code = generated_code[3:]
            if generated_code.endswith("```"):
                generated_code = generated_code[:-3]
            
            return generated_code.strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling LLM API: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {e}")
    
    def execute_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute the generated Python code safely
        
        Args:
            code: Python code to execute
            timeout: Maximum execution time in seconds
            
        Returns:
            Dictionary with execution results including stdout, stderr, and return code
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute the code in a subprocess for safety
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Execution timed out after {timeout} seconds",
                "success": False
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": f"Execution error: {str(e)}",
                "success": False
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except OSError:
                pass
    
    def solve_problem(self, problem_statement: str, execute: bool = True, timeout: int = 30) -> Dict[str, Any]:
        """
        Complete workflow: generate and optionally execute code for a problem
        
        Args:
            problem_statement: Description of the problem to solve
            execute: Whether to execute the generated code
            timeout: Maximum execution time in seconds
            
        Returns:
            Dictionary with generated code and execution results
        """
        try:
            print(f"Generating code for: {problem_statement}")
            code = self.generate_code(problem_statement)
            
            result = {
                "problem": problem_statement,
                "generated_code": code,
                "execution": None
            }
            
            if execute:
                print("Executing generated code...")
                execution_result = self.execute_code(code, timeout)
                result["execution"] = execution_result
            
            return result
            
        except Exception as e:
            return {
                "problem": problem_statement,
                "generated_code": None,
                "execution": None,
                "error": str(e)
            }


def main():
    parser = argparse.ArgumentParser(description="Generate and execute code using LLM")
    parser.add_argument("problem", help="Problem statement to solve")
    parser.add_argument("--no-execute", action="store_true", help="Generate code without executing")
    parser.add_argument("--timeout", type=int, default=30, help="Execution timeout in seconds")
    parser.add_argument("--model", default="openai", help="Model provider to use (openai, claude, gemini)")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--output", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    try:
        generator = LLMCodeGenerator(api_key=args.api_key, model=args.model)
        result = generator.solve_problem(
            args.problem, 
            execute=not args.no_execute, 
            timeout=args.timeout
        )
        
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        
        print("\n" + "="*50)
        print("GENERATED CODE:")
        print("="*50)
        print(result["generated_code"])
        
        if result["execution"]:
            print("\n" + "="*50)
            print("EXECUTION RESULTS:")
            print("="*50)
            if result["execution"]["success"]:
                print("✅ Execution successful!")
                if result["execution"]["stdout"]:
                    print("Output:")
                    print(result["execution"]["stdout"])
            else:
                print("❌ Execution failed!")
                if result["execution"]["stderr"]:
                    print("Error:")
                    print(result["execution"]["stderr"])
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to {args.output}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()