"""
Extended example showing how to add new MCP tools.
This demonstrates the pattern for adding custom tools to the server.
"""

# Example: Adding a new tool "currency_converter"

from pydantic import BaseModel, Field
from app.schemas.tools import ToolInputBase


class CurrencyConverterInput(ToolInputBase):
    """Schema for currency converter tool input."""
    
    amount: float = Field(..., description="Amount to convert", gt=0)
    from_currency: str = Field(..., description="Source currency code (e.g., USD)")
    to_currency: str = Field(..., description="Target currency code (e.g., EUR)")


class CurrencyConverterTool:
    """Currency converter tool implementation."""
    
    async def execute(self, input_data: CurrencyConverterInput):
        """Execute currency conversion."""
        # Pseudo implementation - replace with real API call
        conversion_rates = {
            ("USD", "EUR"): 0.92,
            ("USD", "GBP"): 0.79,
            ("EUR", "USD"): 1.09,
            ("GBP", "USD"): 1.27,
        }
        
        rate = conversion_rates.get((input_data.from_currency, input_data.to_currency), 1.0)
        result = input_data.amount * rate
        
        return {
            "success": True,
            "from_currency": input_data.from_currency,
            "to_currency": input_data.to_currency,
            "from_amount": input_data.amount,
            "to_amount": round(result, 2),
            "rate": rate,
        }


# Add to TOOLS_REGISTRY in app/tools/implementations.py:
"""
"currency_converter": {
    "name": "currency_converter",
    "description": "Convert currencies",
    "input_schema": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Amount to convert",
            },
            "from_currency": {
                "type": "string",
                "description": "Source currency",
            },
            "to_currency": {
                "type": "string",
                "description": "Target currency",
            },
        },
        "required": ["amount", "from_currency", "to_currency"],
    },
    "handler": CurrencyConverterTool(),
}
"""

# Then add to tool execution handler in app/main.py:
"""
elif tool_name == "currency_converter":
    from app.schemas.tools import CurrencyConverterInput
    validated_input = CurrencyConverterInput(**tool_input)
    result = await handler.execute(validated_input)
"""

# Usage:
"""
curl -X POST http://localhost:8000/api/tools/execute \\
  -H "X-API-Key: your-api-key" \\
  -H "Content-Type: application/json" \\
  -d '{
    "tool": "currency_converter",
    "input": {
      "amount": 100,
      "from_currency": "USD",
      "to_currency": "EUR"
    }
  }'
"""

print("""
========================================
HOW TO ADD NEW TOOLS
========================================

1. Create tool schema in app/schemas/tools.py
   - Define InputSchema
   - Define OutputSchema

2. Create tool service in app/services/
   - Add API client or business logic

3. Create tool implementation in app/tools/implementations.py
   - Create Tool class with execute() method
   - Add to TOOLS_REGISTRY

4. Add handler in app/main.py
   - Add case in execute_tool() endpoint

5. Write tests in tests/unit/test_tools.py
   - Test successful execution
   - Test error handling
   - Test validation

6. Document tool in README.md

Example Tool Structure:
- Input: Validated with Pydantic
- Processing: Async execution with error handling
- Output: Structured response following MCP spec
- Logging: Track execution and errors
- Caching: Optional caching for repeated requests
- Rate limiting: Handled by middleware

Tips:
- Use async/await for all I/O operations
- Implement proper error handling
- Add comprehensive logging
- Write unit and integration tests
- Document all parameters and responses
- Consider caching frequently accessed data
- Implement retry logic for external API calls
- Use timeouts to prevent hanging requests
""")
