import re
from typing import Dict, Any

def camel_to_snake_case(data: Dict[str, Any]) -> Dict[str, Any]:
    """將字典的鍵從 camelCase 轉換為 snake_case。
    
    Args:
        data (Dict[str, Any]): 包含 camelCase 鍵的字典
        
    Returns:
        Dict[str, Any]: 包含 snake_case 鍵的字典
        
    Example:
        >>> camel_to_snake_case({"firstName": "John", "lastName": "Doe"})
        {'first_name': 'John', 'last_name': 'Doe'}
    """
    def convert(key: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
    
    return {convert(k): v for k, v in data.items()}

def replace_variable(text: str, variable_dict: Dict[str, Any], max_count: int = 0) -> str:
    """替換文字中的變數。
    
    將文字中的 {{variable}} 格式的變數替換為 variable_dict 中對應的值。
    
    Args:
        text (str): 包含 {{variable}} 格式變數的文字
        variable_dict (Dict[str, Any]): 包含變數值的字典
        max_count (int, optional): 每個變數的最大替換次數。預設為 0（無限制）
        
    Returns:
        str: 替換變數後的文字
        
    Example:
        >>> replace_variable("Hello {{name}}!", {"name": "World"})
        'Hello World!'
    """
    replaced_count: Dict[str, int] = {}
    
    def replace(match: re.Match) -> str:
        key = match.group(1)
        if max_count:
            if key not in replaced_count:
                replaced_count[key] = 1
            else:
                replaced_count[key] += 1
                if replaced_count[key] > max_count:
                    return match.group(0)
        return str(variable_dict.get(key, match.group(0)))

    pattern = r'\{\{([a-zA-Z0-9_]*)\}\}'
    return re.sub(pattern, replace, text) 