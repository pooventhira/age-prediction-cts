import pickle
with open('app/model/age_predictor.pkl', 'rb') as f:
    loaded_object = pickle.load(f)
    print(f"Type: {type(loaded_object)}")
    print(f"Content: {loaded_object}")
    if hasattr(loaded_object, '__dict__'):
        print(f"Attributes: {dir(loaded_object)}")