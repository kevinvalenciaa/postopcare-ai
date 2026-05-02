from pathlib import Path
from typing import Optional

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

class PromptManager:
    """
    Manages loading and formatting of system prompt templates.
    """
    
    def __init__(self, prompts_dir: Optional[Path] = None):
        """
        Initialize PromptManager.
        
        Args:
            prompts_dir: Path to template directory. Defaults to PROMPTS_DIR.
        """
        self.prompts_dir = prompts_dir or PROMPTS_DIR
        # Cache templates in memory to prevent redundant disk I/O during batch generation
        self._cache: dict[str, str] = {}
    
    def get_prompt(self, template_name: str, **variables) -> str:
        """
        Format a specified template with provided variables.
        
        Args:
            template_name: Base name of the template file.
            **variables: Keyword arguments for template substitution.
            
        Returns:
            Formatted prompt string.
        """
        if template_name not in self._cache:
            file_path = self.prompts_dir / f"{template_name}.txt"
            with open(file_path, 'r', encoding='utf-8') as f:
                self._cache[template_name] = f.read()
                
        return self._cache[template_name].format(**variables)
    
    def list_templates(self) -> list[str]:
        """
        Retrieve all available template names.
        
        Returns:
            Sorted list of template base names.
        """
        if not self.prompts_dir.exists():
            return []
            
        return sorted([
            file.stem for file in self.prompts_dir.iterdir() 
            if file.is_file() and file.suffix == '.txt'
        ])
    
    def template_exists(self, template_name: str) -> bool:
        """
        Verify template existence on disk.
        
        Args:
            template_name: Base name of the template.
            
        Returns:
            True if template exists, False otherwise.
        """
        return (self.prompts_dir / f"{template_name}.txt").exists()

if __name__ == "__main__":
    pm = PromptManager()
    print("Available templates:", pm.list_templates())