"""Quick test to check if the model loads and works."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Step 1: Checking model file...")
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "model.keras")
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"  Found: {model_path} ({size_mb:.1f} MB)")
else:
    print(f"  NOT FOUND: {model_path}")
    sys.exit(1)

print("\nStep 2: Loading model...")
try:
    from backend.image_models import _get_model
    model = _get_model()
    print(f"  Input shape:  {model.input_shape}")
    print(f"  Output shape: {model.output_shape}")
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 3: Test prediction with dummy image...")
try:
    import numpy as np
    dummy = np.random.rand(1, 96, 96, 3).astype("float32")
    pred = model.predict(dummy, verbose=0)
    labels = ["angry", "happy", "neutral", "sad", "surprise"]
    print(f"  Prediction: {dict(zip(labels, [f'{p:.3f}' for p in pred[0]]))}")
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nStep 4: Test with actual image bytes...")
try:
    from PIL import Image
    import io
    # Create a simple test image
    img = Image.new("RGB", (100, 100), color=(128, 128, 128))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    test_bytes = buf.getvalue()

    from backend.image_models import detect_emotion_from_image
    result = detect_emotion_from_image(test_bytes)
    print(f"  Emotion: {result['emotion']} ({result['confidence']:.2%})")
    print(f"  Face detected: {result['face_detected']}")
except Exception as e:
    print(f"  FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ ALL TESTS PASSED! Image detection is working.")
