#!/usr/bin/env python3
"""
Configuration reader for LLM API keys and model settings.
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigReader:
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize config reader.
        
        Args:
            config_file: Path to the JSON configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file '{self.config_file}' not found")
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def get_api_key(self, model: str) -> str:
        """
        Get API key for specified model.
        
        Args:
            model: Model name (openai, claude, gemini)
            
        Returns:
            API key string
        """
        if model not in self.config["models"]:
            raise ValueError(f"Model '{model}' not found in config")
        
        api_key = self.config["models"][model]["api_key"]
        if not api_key:
            raise ValueError(f"API key for '{model}' is empty in config")
        
        return api_key
    
    def get_model_config(self, model: str) -> Dict[str, Any]:
        """
        Get complete configuration for specified model.
        
        Args:
            model: Model name (openai, claude, gemini)
            
        Returns:
            Dictionary with model configuration
        """
        if model not in self.config["models"]:
            raise ValueError(f"Model '{model}' not found in config")
        
        return self.config["models"][model]
    
    def get_default_model(self) -> str:
        """Get the default model name."""
        return self.config.get("default_model", "openai")
    
    def list_available_models(self) -> list:
        """List all available model names."""
        return list(self.config["models"].keys())


def load_config(config_file: str = "config.json") -> ConfigReader:
    """
    Load configuration from file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        ConfigReader instance
    """
    return ConfigReader(config_file)


if __name__ == "__main__":
    try:
        config = load_config()
        print("Available models:", config.list_available_models())
        print("Default model:", config.get_default_model())
        
        for model in config.list_available_models():
            model_config = config.get_model_config(model)
            has_key = bool(model_config["api_key"])
            print(f"{model}: API key {'configured' if has_key else 'not set'}")
    
    except Exception as e:
        print(f"Error: {e}")