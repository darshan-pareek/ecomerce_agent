from langchain_core.tools import tool
from data import ORDERS, PRODUCTS

@tool
def get_order(order_id: str) -> dict:
    """
    Use this tool when the customer asks about a specific order.
    Fetches order status, delivery date, and product details
    for the given order ID (format: ORD-XXXX).
    Returns an error dict if the order ID does not exist.
    """
    result = ORDERS.get(order_id, {"error": f"No order found with ID {order_id}"})
    log_tool_call("get_order", {"order_id": order_id}, result)
    return result

@tool
def search_products(query: str) -> list:
    """
    Use this tool when the customer wants to find products,
    browse categories, or look for cheaper/similar alternatives.
    Searches product name, category, and description 
    using the given keyword. Returns a list of matching products.
    Returns empty list if nothing matches.
    """
    query_lower = query.lower()
    matches = [
        p for p in PRODUCTS.values()
        if query_lower in p["name"].lower()
        or query_lower in p["category"].lower()
        or query_lower in p["description"].lower()
    ]
    log_tool_call("search_products", {"query": query}, matches)
    return matches

@tool
def get_product(product_id: str) -> dict:
    """
    Use this tool when you already know a specific product_id
    and need its full details like name, price, and description.
    Returns an error dict if the product ID does not exist.
    """
    result = PRODUCTS.get(product_id, {"error": f"No product found with ID {product_id}"})
    log_tool_call("get_product", {"product_id": product_id}, result)
    return result

# Global list to store tool executions during a single query run
tool_calls_log = []

def clear_tool_calls() -> None:
    """Resets the recorded tool calls list."""
    global tool_calls_log
    tool_calls_log.clear()

def get_tool_calls() -> list:
    """Returns a copy of the executed tool calls."""
    return list(tool_calls_log)

def log_tool_call(tool_name: str, args: dict, result) -> None:
    """Prints a formatted trace of the tool call for the console and appends to the log."""
    print(f"\n[TOOL CALL] {tool_name}")
    print(f"  Args   : {args}")
    print(f"  Result : {result}")
    
    # Store the log dictionary for UI display
    tool_calls_log.append({
        "name": tool_name,
        "args": args,
        "result": result
    })

