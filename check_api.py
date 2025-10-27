"""Quick check of API status"""
import requests

# Test login
auth = requests.post('http://localhost:9000/auth/login', json={
    'email': 'admin@ecommerce.com',
    'password': 'admin123'
})
print(f"Login status: {auth.status_code}")

if auth.status_code == 200:
    token = auth.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Try to list current products
    products = requests.get('http://localhost:9000/products', headers=headers)
    print(f"Products list status: {products.status_code}")
    if products.status_code == 200:
        data = products.json()
        print(f"Total products: {data.get('total', 0)}")
        print(f"Products: {len(data.get('products', []))}")

