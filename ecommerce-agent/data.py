# Fake store database for the chatbot agent
# Two plain Python dicts simulating a database of orders and products

# 5 sample orders with realistic status details
ORDERS = {
  "ORD-1001": {
    "order_id": "ORD-1001",
    "customer_name": "Alice Smith",
    "product_id": "PROD-101",
    "status": "Shipped",
    "estimated_delivery": "2026-06-28"
  },
  "ORD-1002": {
    "order_id": "ORD-1002",
    "customer_name": "Bob Jones",
    "product_id": "PROD-104",
    "status": "Processing",
    "estimated_delivery": "2026-06-30"
  },
  "ORD-1003": {
    "order_id": "ORD-1003",
    "customer_name": "Carol White",
    "product_id": "PROD-102",
    "status": "Delivered",
    "estimated_delivery": "2026-06-20"
  },
  "ORD-1004": {
    "order_id": "ORD-1004",
    "customer_name": "David Brown",
    "product_id": "PROD-106",
    "status": "Out for Delivery",
    "estimated_delivery": "2026-06-26"
  },
  "ORD-1005": {
    "order_id": "ORD-1005",
    "customer_name": "Eva Green",
    "product_id": "PROD-103",
    "status": "Shipped",
    "estimated_delivery": "2026-06-27"
  }
}

# 8 sample products spanning footwear, laptops, and electronics
PRODUCTS = {
  "PROD-101": {
    "product_id": "PROD-101", 
    "name": "Running Shoes X1", 
    "category": "Footwear", 
    "price": 89.99, 
    "description": "Lightweight running shoes for daily training"
  },
  "PROD-102": {
    "product_id": "PROD-102", 
    "name": "Classic Leather Boots",
    "category": "Footwear", 
    "price": 120.00,
    "description": "Durable leather boots for casual and formal wear"
  },
  "PROD-103": {
    "product_id": "PROD-103", 
    "name": "MacBook Air M2",
    "category": "Laptop", 
    "price": 999.99,
    "description": "Thin and light laptop with Apple M2 chip"
  },
  "PROD-104": {
    "product_id": "PROD-104", 
    "name": "Noise-Canceling Headphones",
    "category": "Electronics", 
    "price": 199.99,
    "description": "Wireless over-ear headphones with ANC"
  },
  "PROD-105": {
    "product_id": "PROD-105", 
    "name": "Budget Laptop Z3",
    "category": "Laptop", 
    "price": 449.99,
    "description": "Affordable laptop for students and everyday tasks"
  },
  "PROD-106": {
    "product_id": "PROD-106", 
    "name": "Sport Sandals Pro",
    "category": "Footwear", 
    "price": 55.00,
    "description": "Comfortable sandals for outdoor and beach activities"
  },
  "PROD-107": {
    "product_id": "PROD-107", 
    "name": "Wired Earbuds Basic",
    "category": "Electronics", 
    "price": 19.99,
    "description": "Simple wired earbuds with clear audio"
  },
  "PROD-108": {
    "product_id": "PROD-108", 
    "name": "Trail Running Shoes",
    "category": "Footwear", 
    "price": 75.00,
    "description": "Rugged shoes designed for off-road trail running"
  }
}
