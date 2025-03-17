from pathlib import Path
from string import Template
from typing import Dict, Union
import warnings

class PromptTemplate(Template):
    
    def __init__(self, template: Union[str, Path], role='user'):
        """
        支持两种初始化方式：
        1. 直接传入模板字符串
        2. 传入文件路径（Path对象或有效路径字符串）
        """
        self.role = role
        if isinstance(template, Path) or self._is_valid_path(template):
            template_path = Path(template)
            if not template_path.exists():
                raise FileNotFoundError(f"Template file not found: {template_path}")
            if template_path.is_dir():
                raise IsADirectoryError(f"Template path is a directory: {template_path}")
            
            try:
                template_str = template_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                warnings.warn(f"File {template_path} may not be text format, trying to read anyway...")
                template_str = template_path.read_bytes().decode("utf-8", errors="ignore")
            
            super().__init__(template_str)
        else:
            super().__init__(template)

    def _is_valid_path(self, template: str) -> bool:
        """判断字符串是否是有效的路径格式"""
        return any(
            template.startswith(prefix)
            for prefix in ("./", "../", "/", "~", "C:\\", "D:\\")
        ) or ("/" in template or "\\" in template)

    def render(self, variables: Dict[str, str] = None) -> Dict[str, str]:
        try:
            
            return{
                "role": self.role,
                "content": self.substitute(variables)
            }
            
        except KeyError as e:
            missing_key = e.args[0]
            raise ValueError(
                f"Missing required template variable: {missing_key}\n"
                f"Available variables: {list(variables.keys())}"
            ) from None
        except ValueError as e:
            raise ValueError(f"Template format error: {str(e)}") from None
        
    @classmethod
    def messgae(self, input: str, role)  -> Dict[str, str]:
        return{
                "role": role,
                "content": input
            }
            

class SystemTemplate(PromptTemplate):
    def __init__(self, template: str = "我是由DeepSeek公司开发的智能助手deepseek-r1, 用户提问时请始终用中文回答"):
        super().__init__(template, role="system")

    
    def render(self, variables: Dict[str, str] = None) -> Dict[str, str]:
        base = super().render(variables)
        return base