# inspect_model.py
import tensorflow as tf

# IMPORTANT: Make sure this path is correct
MODEL_PATH = 'app/model/age_predictor.h5'

try:
    print(f"Loading model from: {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH)

    # The model's summary will show the expected input shape at the top
    print("\n--- Model Summary ---")
    model.summary()

    # You can also print the input shape directly
    # It will be in the format (None, height, width, channels)
    print("\n✅ Model's expected input shape:", model.input_shape)

except Exception as e:
    print(f"\n❌ Error loading model: {e}")