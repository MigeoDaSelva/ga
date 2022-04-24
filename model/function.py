from typing import List
from dataclasses import dataclass

@dataclass
class Function:
    
    function: str
    terms: List[str]