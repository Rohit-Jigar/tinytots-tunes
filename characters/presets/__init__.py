from typing import List
from characters.models import Character

DEFAULT_PRESET_CHARACTERS: List[Character] = [
    # 1. Barnaby Bear — friendly brown teddy bear
    Character(
        id="barnaby_bear",
        name="Barnaby Bear",
        species="Brown Teddy Bear",
        color_palette=["#8B5A2B (Warm Honey Brown)", "#00A896 (Teal Dungarees)", "#FFF1D0 (Warm Cream Tummy)", "#E63946 (Cherry Red Button)"],
        clothing="Bright teal corduroy dungarees with a single large red wooden button on the front bib",
        distinctive_features="Round fuzzy ears with cream inner fur, warm circular cream tummy, button nose, sparkling curious brown eyes, warm open smile",
        proportions="Plump toddler teddy bear build, rounded tummy, stubby paws, 1:2 head-to-body ratio",
        personality="Curious, warm-hearted, protective big-brother figure, loves counting, dancing, and nature adventures",
        voice_profile={
            "voice_name": "en-US-AnaNeural",
            "gender": "Friendly Child/Female",
            "pitch": "+15%",
            "rate": "+0%",
            "style": "cheerful, comforting, melodious"
        },
        animation_habits="Bouncy knee-bends on downbeats, patting tummy when excited, waving both paws joyfully",
        visual_prompt="cute 3D cartoon baby brown teddy bear named Barnaby Bear, soft warm honey-brown plush fur, cream tummy, wearing teal dungarees with red button, Disney-Pixar 3D preschool animation style, soft cinematic rim lighting, 8k",
        reference_image_path="data/characters/barnaby_bear_ref.png"
    ),

    # 2. Pip — cheerful little yellow bird
    Character(
        id="pip_bird",
        name="Pip the Bird",
        species="Yellow Songbird",
        color_palette=["#FFD166 (Sunshine Yellow)", "#FF9F1C (Bright Orange Beak)", "#118AB2 (Sky Blue Cap)", "#FFFFFF (Feather Accents)"],
        clothing="Tiny sky-blue aviator cap with soft felt goggles pushed up on his forehead",
        distinctive_features="Chubby round canary body, joyful tuft of head feathers, tiny orange beak, wide expressive anime-styled eyes that blink together",
        proportions="Chubby round spherical body, tiny fluttering wings, cute wobbly hops",
        personality="Super energetic, musical, whistles catchy hooks, loves rhyming and flying loop-de-loops",
        voice_profile={
            "voice_name": "en-US-JennyNeural",
            "gender": "Energetic Child",
            "pitch": "+25%",
            "rate": "+10%",
            "style": "chirpy, bright, high-energy"
        },
        animation_habits="Quick joyful wing flutters, head tilts left-and-right, hovering slightly off the ground",
        visual_prompt="adorable chubby baby cartoon songbird Pip, bright sunshine yellow feathers, sky-blue aviator cap with goggles, orange beak, big sparkling eyes, singing joyfully, Pixar 3D preschool render, 8k",
        reference_image_path="data/characters/pip_bird_ref.png"
    ),

    # 3. Penny — cute pink bunny
    Character(
        id="penny_bunny",
        name="Penny Bunny",
        species="Pink Bunny",
        color_palette=["#FFB3C6 (Pastel Powder Pink)", "#FFFFFF (Snow White Muzzle & Paws)", "#C77DFF (Lavender Pinafore)", "#FF758F (Coral Bow)"],
        clothing="Soft lavender pinafore dress over a white ruffled collar with a cute coral bow behind her left ear",
        distinctive_features="Long velvety pink ears that bounce and fold with emotion, pink twitchy nose, big gentle hazel eyes, fluffy puff-ball tail",
        proportions="Slender cute bunny toddler, long expressive floppy ears, bouncy light feet",
        personality="Sweet, gentle, loves bedtime lullabies, counting stars, sharing toys, and gentle hopping games",
        voice_profile={
            "voice_name": "en-US-AnaNeural",
            "gender": "Sweet Preschooler",
            "pitch": "+18%",
            "rate": "-5%",
            "style": "gentle, sweet, reassuring"
        },
        animation_habits="Playful nose twitches, ear tips flopping on jumps, clapping paws in front of chest",
        visual_prompt="cute baby cartoon pink bunny Penny Bunny, velvety powder pink fur, white paws, wearing lavender pinafore dress with coral ribbon, long floppy ears, joyful sweet 3D preschool style, 8k",
        reference_image_path="data/characters/penny_bunny_ref.png"
    ),

    # 4. Zara Zebra — playful zebra
    Character(
        id="zara_zebra",
        name="Zara Zebra",
        species="Playful Zebra",
        color_palette=["#7B2CBF (Pastel Purple Stripes)", "#FFFFFF (Pure White Coat)", "#06D6A0 (Mint Green Overalls)", "#FFB703 (Sunny Yellow Buckles)"],
        clothing="Pastel mint green artist overalls with purple pockets carrying oversized colorful wooden crayons",
        distinctive_features="Whimsical gentle purple stripes instead of black, fluffy purple mohawk mane with a yellow daisy flower pinned near her ear",
        proportions="Playful foal proportions, sturdy hooves, swishy cartoon tail with purple tuft",
        personality="Artistic, quirky, loves dancing to rhythmic beats, painting the sky with colors, and stomping her hooves in time",
        voice_profile={
            "voice_name": "en-US-JennyNeural",
            "gender": "Playful Child",
            "pitch": "+12%",
            "rate": "+5%",
            "style": "rhythmic, playful, expressive"
        },
        animation_habits="Trotting hooves in sync with rhythm, swishing tail side-to-side, flourishing crayons in the air",
        visual_prompt="adorable baby cartoon zebra Zara Zebra with soft pastel purple stripes and white coat, wearing mint green overalls, daisy in purple mane, joyful artistic 3D preschool style, 8k",
        reference_image_path="data/characters/zara_zebra_ref.png"
    ),

    # 5. Sunny — friendly little sunshine character
    Character(
        id="sunny_sunshine",
        name="Sunny",
        species="Little Sunshine",
        color_palette=["#FFD000 (Golden Sunlight)", "#FF8800 (Warm Amber Corona)", "#FF595E (Rosy Pink Cheeks)", "#FFFFFF (Sparkle Highlights)"],
        clothing="Tiny sky-blue cloud bowtie with soft golden sparkle dust hovering around him",
        distinctive_features="Glowing golden circular face with soft rounded sun rays that pulse gently, rosy blush cheeks, huge beaming smile, sparkling starry eyes",
        proportions="Floating circular sun character with gentle undulating curved rays, floating cartoon hands with white cartoon gloves",
        personality="Radiant optimism, guides morning routines, greets every day with laughter, warms the world and spreads good morning cheer",
        voice_profile={
            "voice_name": "en-US-AnaNeural",
            "gender": "Bright Child",
            "pitch": "+22%",
            "rate": "+5%",
            "style": "beaming, radiant, musical"
        },
        animation_habits="Gentle bobbing in the sky, sun rays stretching and pulsing to the tempo, winking one star-eye",
        visual_prompt="cute living 3D cartoon baby sun character named Sunny, smiling face with rosy cheeks, soft rounded golden rays, wearing tiny cloud bowtie, floating in a bright pastel sky, Pixar 3D aesthetic, volumetric warm glow, 8k",
        reference_image_path="data/characters/sunny_sunshine_ref.png"
    )
]
