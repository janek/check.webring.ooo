import names_dataset as nd

print("attributes:", [attr for attr in dir(nd) if not attr.startswith("_")])

print("\n=== TRYING NameDataset class ===")

try:
    dataset = nd.NameDataset()
    print("NameDataset created successfully!")
    print(
        "Available methods:",
        [method for method in dir(dataset) if not method.startswith("_")],
    )

    # Try some methods
    print("\n=== TESTING METHODS ===")

    # Try search
    try:
        result = dataset.search("Alice")
        print("Search result for 'Alice':", result)
    except Exception as e:
        print("Error with search:", e)

    # Try accessing data
    try:
        if hasattr(dataset, "first_names"):
            print("first_names type:", type(dataset.first_names))
            if hasattr(dataset.first_names, "keys"):
                keys = list(dataset.first_names.keys())[:10]
                print("first_names keys (first 10):", keys)
    except Exception as e:
        print("Error accessing first_names:", e)

    print("\n=== MORE TESTS ===")

    # Test getting top names
    print("=== TOP NAMES TEST ===")
    try:
        top_first_names = dataset.get_top_names(n=10, use_first_names=True)
        print("Top 10 first names:", top_first_names)
    except Exception as e:
        print("Error with get_top_names:", e)

    print("\n=== MALE NAMES ===")
    try:
        top_male = dataset.get_top_names(n=5, use_first_names=True, gender="Male")
        print("Top 5 male names:", top_male)
    except Exception as e:
        print("Error with male names:", e)

    print("\n=== FEMALE NAMES ===")
    try:
        top_female = dataset.get_top_names(n=5, use_first_names=True, gender="Female")
        print("Top 5 female names:", top_female)
    except Exception as e:
        print("Error with female names:", e)

    print("\n=== AUTO COMPLETE TEST ===")
    try:
        autocomplete = dataset.auto_complete("ali", n=5)
        print("Auto-complete for 'ali':", autocomplete)
    except Exception as e:
        print("Error with auto_complete:", e)

    print("\n=== FUZZY SEARCH TEST ===")
    try:
        fuzzy = dataset.fuzzy_search("alise", n=5)  # misspelling of Alice
        print("Fuzzy search for 'alise':", fuzzy)
    except Exception as e:
        print("Error with fuzzy_search:", e)

    print("\n=== DATA SIZE ===")
    if dataset.first_names:
        print("Total first names:", len(dataset.first_names))
    if dataset.last_names:
        print("Total last names:", len(dataset.last_names))

except Exception as e:
    print("Error creating NameDataset:", e)
