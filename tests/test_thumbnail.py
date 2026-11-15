import os
import pytest
from PIL import Image
from thumbnail.generator import thumbnail_generator

def test_thumbnail_dimensions_and_export(tmp_path):
    base_img = str(tmp_path / "base.png")
    # Create simple base image
    im = Image.new("RGB", (1280, 720), color="#48CAE4")
    im.save(base_img)

    out_thumb = str(tmp_path / "thumb.jpg")
    result = thumbnail_generator.generate_thumbnail(
        title="The Rainbow Song",
        base_image_path=base_img,
        output_path=out_thumb,
        badge_text="SING ALONG!",
        character_name="Barnaby Bear"
    )

    assert os.path.exists(result)
    with Image.open(result) as thumb:
        assert thumb.size == (1280, 720)

