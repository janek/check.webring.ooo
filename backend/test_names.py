import names_dataset as nd

print("Creating NameDataset instance...")
dataset = nd.NameDataset()
print("NameDataset loaded successfully!")

print("\n=== AVAILABLE METHODS ===")
methods = [method for method in dir(dataset) if not method.startswith("_")]
print("Available methods:", methods)

print("\n=== SEARCH TEST ===")
result = dataset.search("Alice")
print("Search result for 'Alice':", result)

print("\n=== SEARCH TEST 2 ===")
result = dataset.search("Philippe")
print("Search result for 'Philippe':", result)

print("\n=== COUNTRY CODES ===")
country_codes = dataset.get_country_codes(alpha_2=True)
print("Country codes (first 10):", country_codes[:10])

print("\n=== DATA SIZE ===")
if dataset.first_names:
    print("Total first names:", len(dataset.first_names))
if dataset.last_names:
    print("Total last names:", len(dataset.last_names))

print("\n=== SAMPLE FIRST NAMES ===")
if dataset.first_names:
    sample_names = list(dataset.first_names.keys())[:20]
    print("First 20 names:", sample_names)

print("\n=== SAMPLE FIRST NAME DATA ===")
if dataset.first_names and "Alice" in dataset.first_names:
    alice_data = dataset.first_names["Alice"]
    print("Alice data:", alice_data)
