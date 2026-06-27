# Unit tests for the store assistant agent's tool functions and metadata registration
import unittest
from tools import get_order, search_products, get_product
from agent import TOOLS

class TestStoreAgentTools(unittest.TestCase):
    
    def test_get_order_valid(self):
        """
        Verifies that get_order returns the correct customer details for a valid order.
        Why it matters: The agent relies on orders being correctly mapped to customer records.
        """
        # Call the underlying function directly using tool.func to bypass LangChain wrapping
        result = get_order.func("ORD-1001")
        self.assertIn("customer_name", result)
        self.assertEqual(result["customer_name"], "Alice Smith")

    def test_get_order_invalid(self):
        """
        Verifies that get_order returns an error message when a non-existent order ID is searched.
        Why it matters: Crucial for downstream error handling, allowing the LLM to report back gracefully.
        """
        result = get_order.func("ORD-9999")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No order found with ID ORD-9999")

    def test_search_products_found(self):
        """
        Verifies search_products retrieves matches when searching a valid keyword.
        Why it matters: Ensures user queries like 'shoes' map successfully to available stock.
        """
        results = search_products.func("shoes")
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)
        # Ensure matched products contain relevant query text
        for p in results:
            text_pool = (p["name"] + p["category"] + p["description"]).lower()
            self.assertIn("shoes", text_pool)

    def test_search_products_empty(self):
        """
        Verifies search_products returns an empty list for completely random searches.
        Why it matters: Ensures the search doesn't return unrelated listings when there is no matching stock.
        """
        results = search_products.func("xyzabc999")
        self.assertEqual(results, [])

    def test_get_product_valid(self):
        """
        Verifies get_product returns the full attributes of a product using its ID.
        Why it matters: Used during tool-chaining to pull detailed specs once an order's product_id is resolved.
        """
        result = get_product.func("PROD-101")
        self.assertIn("name", result)
        self.assertEqual(result["name"], "Running Shoes X1")

    def test_get_product_invalid(self):
        """
        Verifies get_product returns an error key when looking up a fake product ID.
        Why it matters: Ensures the agent has clear indications of failures instead of hallucinating details.
        """
        result = get_product.func("PROD-999")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No product found with ID PROD-999")

    def test_tool_has_name(self):
        """
        Verifies each tool contains a name attribute registered correctly by the @tool decorator.
        Why it matters: LangChain and LangGraph route calls to tool functions by matching their name attributes.
        """
        for tool_obj in TOOLS:
            # Asserts that the LangChain @tool decorator has added a .name attribute to the object
            self.assertTrue(hasattr(tool_obj, "name"))
            self.assertTrue(len(tool_obj.name) > 0)

if __name__ == "__main__":
    unittest.main()
