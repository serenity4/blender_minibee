import os
cache_dir = os.environ["BLENDER_CACHE"]
os.makedirs(cache_dir, exist_ok=True)
print(os.listdir(cache_dir))
