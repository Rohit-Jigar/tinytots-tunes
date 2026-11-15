from typing import Dict, Any, List
from characters.models import Character
from core.safety import SafetyChecker
from planner.catalog_20 import catalog_manager

class LyricWriter:
    """
    Composes original, rhythm-aligned, educational nursery rhymes and sing-along scripts.
    Guarantees copyright-free content and age-appropriate vocabulary (ages 1-5).
    """

    @classmethod
    def write_lyrics(cls, song_idea: Dict[str, Any], character: Character) -> Dict[str, Any]:
        topic = song_idea.get("title", "Happy Day")
        category = song_idea.get("category", "General")
        char_name = character.name

        # Enforce safety check on inputs
        SafetyChecker.enforce_safety(topic, context="Lyric Topic")
        SafetyChecker.enforce_safety(char_name, context="Lyric Character Name")

        # Check if topic matches our official 20-song curriculum catalog
        cat_song = catalog_manager.get_song_by_title(topic)
        if cat_song:
            sections = cat_song["sections"]
        # Category-driven lyric templates with dynamic rhyming structures
        elif "color" in topic.lower() or "color" in category.lower():
            sections = [
                {
                    "type": "Intro",
                    "lines": [
                        f"Hello little friends! I'm {char_name}!",
                        "Look at all the magical colors around us today!",
                        "Let's sing our Rainbow Song! [Giggle]"
                    ],
                    "action_cues": ["Wave both hands cheerfully", "Point up at the sky"]
                },
                {
                    "type": "Verse 1",
                    "lines": [
                        "Red is the apple sweet and bright,",
                        "Yellow is the sun shining warm and light!",
                        "Blue is the ocean where the little fish play,",
                        "Colors make us smile every single day!"
                    ],
                    "action_cues": ["Show red apple", "Make big circle with arms for sun", "Wiggle hands like swimming fish"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Red, yellow, blue, and green!",
                        "The prettiest rainbow you've ever seen!",
                        "Clap, clap, clap and dance with me, [Clap!]",
                        "Colors are as happy as happy can be!"
                    ],
                    "action_cues": ["Clap hands three times", "Twirl around joyfully"]
                },
                {
                    "type": "Verse 2",
                    "lines": [
                        "Green is the clover on the grassy hill,",
                        "Orange is the pumpkin sitting sweet and still!",
                        "Purple is the grape juicy on the vine,",
                        "Look at all our colors how they glow and shine!"
                    ],
                    "action_cues": ["Touch the ground", "Cup hands like round pumpkin", "Smile and sparkle fingers"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Red, yellow, blue, and green!",
                        "The prettiest rainbow you've ever seen!",
                        "Clap, clap, clap and dance with me, [Clap!]",
                        "Colors are as happy as happy can be!"
                    ],
                    "action_cues": ["Clap hands three times", "Big playful jump"]
                },
                {
                    "type": "Outro",
                    "lines": [
                        "Yay! You know all your rainbow colors!",
                        f"Great job singing along with {char_name}!",
                        "See you next time, little friends! Bye-bye! [Chime]"
                    ],
                    "action_cues": ["Cheer and wave goodbye", "Bow with a warm smile"]
                }
            ]
        elif "teeth" in topic.lower() or "habit" in category.lower():
            sections = [
                {
                    "type": "Intro",
                    "lines": [
                        f"Wake up, wake up, little sleepyhead! It's {char_name}!",
                        "Time to get our toothbrushes ready! [Chime]",
                        "Let's make our teeth sparkle bright!"
                    ],
                    "action_cues": ["Stretch arms wide", "Hold up a colorful toothbrush"]
                },
                {
                    "type": "Verse 1",
                    "lines": [
                        "Squeeze a little paste, just a tiny pea,",
                        "Now hold your brush so happy and free!",
                        "Up and down, brush them clean and white,",
                        "Brush in the morning and brush at night!"
                    ],
                    "action_cues": ["Pretend to squeeze tube", "Move brush up and down in front of mouth"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Brush, brush, brush your teeth, round and round!",
                        "The happiest brushing song in town! [Pop!]",
                        "Left and right and all around,",
                        "Sparkly clean without a frown!"
                    ],
                    "action_cues": ["Circle brushing motion", "Big sparkly grin with thumbs up"]
                },
                {
                    "type": "Verse 2",
                    "lines": [
                        "Brush the teeth in front, brush the teeth in back,",
                        "Healthy little teeth stay right on track!",
                        "Swish with the water, spit it in the sink, [Splash!]",
                        "Look at that smile, what do you think?"
                    ],
                    "action_cues": ["Point to front teeth then back molars", "Puff cheeks and pretend to swish"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Brush, brush, brush your teeth, round and round!",
                        "The happiest brushing song in town! [Pop!]",
                        "Left and right and all around,",
                        "Sparkly clean without a frown!"
                    ],
                    "action_cues": ["Circle brushing motion", "Big sparkly grin"]
                },
                {
                    "type": "Outro",
                    "lines": [
                        "Sparkle sparkle! What a brilliant smile!",
                        f"{char_name} is so proud of you!",
                        "Keep brushing every day! High five! [Pop!]"
                    ],
                    "action_cues": ["Hold up hand for high-five", "Wave happily"]
                }
            ]
        elif "penguin" in topic.lower() or "count" in category.lower():
            sections = [
                {
                    "type": "Intro",
                    "lines": [
                        "Brrr! Look at all the fluffy white snow!",
                        f"Let's count our penguin friends with {char_name}!",
                        "Are you ready? Let's go! [Giggle]"
                    ],
                    "action_cues": ["Shiver playfully", "Point to snowy hill"]
                },
                {
                    "type": "Verse 1",
                    "lines": [
                        "One little penguin waddling on the ice,",
                        "Two little penguins eating something nice!",
                        "Three little penguins sliding down the hill,",
                        "Wheee down the snow they never stay still!"
                    ],
                    "action_cues": ["Hold up 1 finger", "Hold up 2 fingers", "Hold up 3 fingers and make slide motion"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Waddle, waddle, waddle, slide and play!",
                        "Counting little penguins all through the day! [Pop!]",
                        "Flap your little wings and stamp your feet, [Stamp!]",
                        "Dancing along to the penguin beat!"
                    ],
                    "action_cues": ["Waddle side to side", "Flap elbows like penguin wings"]
                },
                {
                    "type": "Verse 2",
                    "lines": [
                        "Four little penguins splashing in the sea,",
                        "Five little penguins happy as can be!",
                        "One, two, three, four, five in a line,",
                        "All of our penguin friends look so fine!"
                    ],
                    "action_cues": ["Hold up 4 fingers", "Hold up 5 fingers", "Count each finger one by one"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Waddle, waddle, waddle, slide and play!",
                        "Counting little penguins all through the day! [Pop!]",
                        "Flap your little wings and stamp your feet, [Stamp!]",
                        "Dancing along to the penguin beat!"
                    ],
                    "action_cues": ["Waddle side to side", "Flap elbows like penguin wings"]
                },
                {
                    "type": "Outro",
                    "lines": [
                        "Five happy penguins! You did it!",
                        "You counted all the way from one to five!",
                        f"{char_name} says you're a superstar! Bye-bye!"
                    ],
                    "action_cues": ["Clap enthusiastically", "Blow a friendly kiss and wave"]
                }
            ]
        else:
            # Default energetic toddler song
            sections = [
                {
                    "type": "Intro",
                    "lines": [
                        f"Hi friends! Come sing and play with {char_name}!",
                        f"Today we're singing about {topic}!",
                        "Let's dance together! [Chime]"
                    ],
                    "action_cues": ["Wave both hands", "Bounce on toes"]
                },
                {
                    "type": "Verse 1",
                    "lines": [
                        "Step to the left, step to the right,",
                        "Sunshine is glowing so warm and bright!",
                        "Jump in the air as high as you can,",
                        "Clap your two hands, you're our number one fan!"
                    ],
                    "action_cues": ["Step left and right", "Jump high", "Clap twice"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Sing, sing, sing with joy and glee,",
                        "Learning is fun for you and me! [Giggle]",
                        "Twirl all around and tap your shoes, [Tap!]",
                        "Singing our happy TinyTots tunes!"
                    ],
                    "action_cues": ["Twirl in a circle", "Tap feet on the floor"]
                },
                {
                    "type": "Verse 2",
                    "lines": [
                        "Reach up high and touch the sky,",
                        "Watch the pretty butterfly fluttering by!",
                        "Bend down low and touch your toes,",
                        "Give a little wiggle to your button nose!"
                    ],
                    "action_cues": ["Reach arms high", "Flutter fingers like butterfly", "Touch toes", "Wiggle nose"]
                },
                {
                    "type": "Chorus",
                    "lines": [
                        "Sing, sing, sing with joy and glee,",
                        "Learning is fun for you and me! [Giggle]",
                        "Twirl all around and tap your shoes, [Tap!]",
                        "Singing our happy TinyTots tunes!"
                    ],
                    "action_cues": ["Twirl in a circle", "Tap feet on the floor"]
                },
                {
                    "type": "Outro",
                    "lines": [
                        "That was so much fun dancing with you!",
                        f"{char_name} loves you so much!",
                        "Sing again soon! Bye-bye friends! [Chime]"
                    ],
                    "action_cues": ["Hug self warmly", "Wave goodbye with both hands"]
                }
            ]

        # Flatten full text for TTS and subtitles
        full_text_lines = []
        for s in sections:
            full_text_lines.extend(s["lines"])

        return {
            "title": topic,
            "character_id": character.id,
            "character_name": character.name,
            "sections": sections,
            "full_lyrics_text": "\n".join(full_text_lines),
            "estimated_lines": len(full_text_lines)
        }

