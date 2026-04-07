"""
fix_model.py - Auto-detects architecture and re-saves with tensorflow.keras
Run from: D:\MoodMate\MoodMate app\
Command:  py fix_model.py
"""
import tensorflow as tf
import tf_keras
import os

MODEL_PATH = 'models/emotion_model.keras'
BACKUP_PATH = 'models/emotion_model_backup.keras'

print("=" * 50)
print("Step 1: Loading model with tf_keras...")
try:
    old_model = tf_keras.models.load_model(MODEL_PATH, compile=False)
    print("✅ Loaded with tf_keras")
except Exception as e:
    print(f"❌ Failed: {e}")
    exit()

print("\nStep 2: Inspecting architecture...")
old_model.summary()
weights = old_model.get_weights()
print(f"\n   Total weight arrays: {len(weights)}")

print("\nStep 3: Rebuilding with tensorflow.keras using SAME architecture...")
new_layers = []
for layer in old_model.layers:
    cls_name = layer.__class__.__name__
    cfg = layer.get_config()

    if cls_name == 'Conv2D':
        new_layers.append(tf.keras.layers.Conv2D(
            filters=cfg['filters'],
            kernel_size=cfg['kernel_size'],
            padding=cfg['padding'],
            activation=cfg['activation']
        ))
    elif cls_name == 'MaxPooling2D':
        new_layers.append(tf.keras.layers.MaxPooling2D(pool_size=cfg['pool_size']))
    elif cls_name == 'BatchNormalization':
        new_layers.append(tf.keras.layers.BatchNormalization())
    elif cls_name == 'Dropout':
        new_layers.append(tf.keras.layers.Dropout(rate=cfg['rate']))
    elif cls_name == 'Flatten':
        new_layers.append(tf.keras.layers.Flatten())
    elif cls_name == 'Dense':
        new_layers.append(tf.keras.layers.Dense(
            units=cfg['units'],
            activation=cfg['activation']
        ))
    elif cls_name == 'InputLayer':
        pass

input_shape = old_model.input_shape[1:]
print(f"   Input shape: {input_shape}")

new_model = tf.keras.Sequential(
    [tf.keras.layers.Input(shape=input_shape)] + new_layers
)
new_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nStep 4: Transferring weights...")
try:
    new_model.set_weights(weights)
    print("✅ Weights transferred successfully!")
except Exception as e:
    print(f"❌ Weight transfer failed: {e}")
    exit()

print("\nStep 5: Saving fixed model...")
if os.path.exists(MODEL_PATH):
    os.rename(MODEL_PATH, BACKUP_PATH)
    print(f"   Backed up old model as: {BACKUP_PATH}")

new_model.save(MODEL_PATH)
print(f"✅ Fixed model saved to: {MODEL_PATH}")
print("\n🎉 Done! Now restart your server.")