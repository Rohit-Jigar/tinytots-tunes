"""
TinyTots Tunes - 20 Original Preschool Song Catalog & Production Curriculum
100% Original, Trademark-Safe, COPPA-Compliant, Educational Nursery Songs
"""

from typing import Dict, Any, List, Optional
from characters.models import Character

SONG_CATALOG_20: List[Dict[str, Any]] = [
    {
        "number": 1,
        "id": "video_01",
        "title": "The Dancing Dinosaur Song",
        "category": "Movement & Gross Motor Skills",
        "lead_character_id": "barnaby_bear",
        "target_age": "2-5 years",
        "bpm": 120,
        "tempo": "Upbeat 120 BPM",
        "educational_goals": [
            "Gross motor movement (stomp, roar, wiggle, clap)",
            "Rhythmic imitation and balance",
            "Prehistoric animal vocabulary (Dino, tail, footprints)"
        ],
        "hook": "Stomp stomp stomp like a friendly dinosaur, dance with Barnaby Bear and roar!",
        "visual_theme": "Lush prehistoric valley with gentle pink volcanoes, giant smiling flowers, and soft green hills",
        "sections": [
            {
                "type": "Intro",
                "lines": [
                    "Hello little stompers! It's Barnaby Bear!",
                    "Put on your dinosaur feet and stomp with me!",
                    "Are you ready to roar? Let's go! [Roar!]"
                ],
                "action_cues": ["Wave both hands enthusiastically", "Show pretend dinosaur claws"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Big green footprints in the sand,",
                    "Dinosaur dancing across the land!",
                    "Stomp your two feet, one and two,",
                    "Here comes a happy dino dance for you!"
                ],
                "action_cues": ["Stomp right foot then left foot", "Sway arms side to side like a dancing dinosaur"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Stomp, stomp, dinosaur, stomp on the floor!",
                    "Give a little wiggle and a happy roar! [Roar!]",
                    "Swish your big tail, tap your tiny claws,",
                    "Dinosaur dancing gives a loud applause! [Clap!]"
                ],
                "action_cues": ["Stomp rhythmically", "Wiggle hips and roar", "Wiggle tail", "Clap hands three times"]
            },
            {
                "type": "Verse 2",
                "lines": [
                    "Flap little pterodactyl wings so high,",
                    "Flying past the clouds in the sunny sky!",
                    "Spin all around like a dino spinning top,",
                    "Dancing to the beat that will never stop!"
                ],
                "action_cues": ["Flap arms like gentle wings", "Spin in a slow joyful circle"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Stomp, stomp, dinosaur, stomp on the floor!",
                    "Give a little wiggle and a happy roar! [Roar!]",
                    "Swish your big tail, tap your tiny claws,",
                    "Dinosaur dancing gives a loud applause! [Clap!]"
                ],
                "action_cues": ["Stomp feet to beat", "Big dinosaur roar", "Clap excitedly"]
            },
            {
                "type": "Outro",
                "lines": [
                    "Whew! That was such a mighty dinosaur stomp!",
                    "Barnaby Bear had so much fun with you!",
                    "See you next time, little dinos! Roar and bye-bye! [Chime]"
                ],
                "action_cues": ["Wipe brow and smile warmly", "Wave goodbye with both paws"]
            }
        ]
    },
    {
        "number": 2,
        "id": "video_02",
        "title": "ABC Phonics Adventure",
        "category": "Language & Early Literacy",
        "lead_character_id": "pip_bird",
        "secondary_character_id": "penny_bunny",
        "target_age": "2-5 years",
        "bpm": 116,
        "tempo": "Playful 116 BPM",
        "educational_goals": [
            "Phonemic letter-sound association (A-apple, B-ball, C-cat)",
            "Early alphabet recognition and vocal pronunciation",
            "Active call-and-response engagement"
        ],
        "hook": "Sing A, B, C with Pip the Bird and learn the sounds of every word!",
        "visual_theme": "Whimsical storybook garden with floating alphabet cloud bubbles, flower petals, and wooden ABC blocks",
        "sections": [
            {
                "type": "Intro",
                "lines": [
                    "Chirp chirp! Hello friends! I'm Pip the Bird!",
                    "Come fly through the alphabet garden with me and Penny!",
                    "Let's sing our magical ABC phonics song! [Chirp!]"
                ],
                "action_cues": ["Flutter tiny yellow wings", "Perch on a wooden letter block"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "A is for Apple, a-a-apple sweet,",
                    "B is for Ball that bounces at our feet! [Boing!]",
                    "C is for Cat saying meow meow meow,",
                    "Look at all the letters that we're learning now!"
                ],
                "action_cues": ["Hold pretend apple", "Bounce hands like ball", "Pretend whisker scratch"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "A, B, C, D, sing along with me,",
                    "Letters are as happy as happy can be!",
                    "Chirp the sounds, clap to the beat, [Clap!]",
                    "Reading with Pip is such a sunny treat!"
                ],
                "action_cues": ["Trace letters in air", "Clap on downbeat", "Flutter wings joyfully"]
            },
            {
                "type": "Verse 2",
                "lines": [
                    "D is for Duck saying quack quack quack,",
                    "E is for Elephant with trunks right on track!",
                    "F is for Frog hopping in the spring, [Boing!]",
                    "Oh what joyful happiness letters bring!"
                ],
                "action_cues": ["Duck bill hand motion", "Trunk arm swing", "Little frog hop"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "A, B, C, D, sing along with me,",
                    "Letters are as happy as happy can be!",
                    "Chirp the sounds, clap to the beat, [Clap!]",
                    "Reading with Pip is such a sunny treat!"
                ],
                "action_cues": ["Point to floating cloud letters", "Spin and chirp"]
            },
            {
                "type": "Outro",
                "lines": [
                    "You know your phonics sounds so well!",
                    "Pip the Bird is cheering for you! Hooray!",
                    "Keep singing your ABCs! Bye-bye! [Chirp!]"
                ],
                "action_cues": ["Bow sweetly", "Cheer and flutter off to the sky"]
            }
        ]
    },
    {
        "number": 3,
        "id": "video_03",
        "title": "Wheels on the Happy Bus",
        "category": "Vehicles & Community",
        "lead_character_id": "zara_zebra",
        "target_age": "1-4 years",
        "bpm": 122,
        "tempo": "Bouncy 122 BPM",
        "educational_goals": ["Community transport", "Rotational arm movements", "Cause and effect sounds (beep, swish)"],
        "hook": "Round and round through the friendly town, driving with Zara with never a frown!",
        "visual_theme": "Pastel village with smiling houses, rainbow crosswalks, and rolling green hills",
        "sections": [
            {
                "type": "Intro",
                "lines": ["All aboard the Happy Bus! I'm Zara Zebra!", "Hold onto your seats, friends!", "Let's roll through town! [Honk!]"],
                "action_cues": ["Honk imaginary horn", "Wave out the bus window"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "The wheels on the Happy Bus go round and round,",
                    "Rolling smoothly through the smiling town!",
                    "Up and down the gentle hill we ride,",
                    "With all our friendly buddies sitting side by side!"
                ],
                "action_cues": ["Roll arms over each other", "Lean left and right"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Beep beep goes the horn, toot toot toot! [Beep!]",
                    "Wipers on the glass go swish swish swoot!",
                    "Sing with Zara, wave your hands so high,",
                    "Rolling under the bright blue sky!"
                ],
                "action_cues": ["Press steering wheel horn", "Swish arms like wipers"]
            },
            {
                "type": "Verse 2",
                "lines": [
                    "The doors on the bus go open and shut,",
                    "Stepping on the bus, no ifs or but!",
                    "The bell on the bus goes ding ding ding! [Ding!]",
                    "Listen to the passengers laugh and sing!"
                ],
                "action_cues": ["Open and close arms", "Ring bell motion"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Beep beep goes the horn, toot toot toot! [Beep!]",
                    "Wipers on the glass go swish swish swoot!",
                    "Sing with Zara, wave your hands so high,",
                    "Rolling under the bright blue sky!"
                ],
                "action_cues": ["Press steering wheel horn", "Swish arms like wipers"]
            },
            {
                "type": "Outro",
                "lines": ["We arrived at our happy bus stop!", "Great driving with Zara Zebra!", "See you on the next ride! Beep beep! [Honk!]"],
                "action_cues": ["Wave goodbye happily"]
            }
        ]
    },
    {
        "number": 4,
        "id": "video_04",
        "title": "Five Little Funny Monkeys",
        "category": "Numbers & Counting",
        "lead_character_id": "barnaby_bear",
        "target_age": "2-5 years",
        "bpm": 118,
        "tempo": "Playful 118 BPM",
        "educational_goals": ["Counting down 5 to 1", "Gentle safety lesson", "Rhythmic jumping"],
        "hook": "Five playful monkeys bouncing on the bed, Barnaby Bear says rest your head!",
        "visual_theme": "Cozy pastel bedroom with fluffy pillows, star nightlight, and wooden bedframe",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Look at those silly monkeys! I'm Barnaby Bear!", "They are jumping so high!", "Let's count them together! 1, 2, 3, 4, 5! [Boing!]"],
                "action_cues": ["Hold up 5 fingers", "Point at bouncy bed"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Five little monkeys jumping on the bed,",
                    "One bounced high and bumped his soft head! [Pop!]",
                    "Barnaby called the doctor who kindly said,",
                    "No more jumping on the bouncy bed!"
                ],
                "action_cues": ["Bounce hands", "Gently tap head", "Shake pointer finger playfully"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Bounce, bounce, little monkeys, giggle and play,",
                    "Counting down the numbers every single day! [Giggle]",
                    "Four, three, two, and down to one,",
                    "Gentle little hugs when the jumping is done!"
                ],
                "action_cues": ["Jump on spot", "Count down fingers", "Wrap arms in hug"]
            },
            {
                "type": "Verse 2",
                "lines": [
                    "Now all the little monkeys are resting their heads,",
                    "Snuggled up warmly in their cozy beds!",
                    "Dreaming of bananas, sweet and bright,",
                    "Sleep tight little monkeys, nighty-night! [Chime]"
                ],
                "action_cues": ["Rest cheek on folded hands", "Smile softly"]
            },
            {
                "type": "Outro",
                "lines": ["All the monkeys are safe and sound!", "Barnaby Bear loves counting with you!", "Sweet dreams, little friends! [Chime]"],
                "action_cues": ["Whisper gently and wave"]
            }
        ]
    },
    {
        "number": 5,
        "id": "video_05",
        "title": "Colors Around the World",
        "category": "Colors & Creativity",
        "lead_character_id": "penny_bunny",
        "target_age": "2-5 years",
        "bpm": 116,
        "tempo": "Cheerful 116 BPM",
        "educational_goals": ["Identify Red, Blue, Yellow, Green, Purple, Pink", "Global landmarks & nature"],
        "hook": "Paint the world in colors bright, with Penny Bunny day and night!",
        "visual_theme": "Art studio meadow with oversized rainbow crayons, watercolor easel, and blooming flowers",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Hop hop! Hello! I'm Penny Bunny!", "Grab your paintbrushes, friends!", "Let's color our beautiful world! [Pop!]"],
                "action_cues": ["Hop twice", "Hold a giant watercolor brush"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Red is the tulip growing in the spring,",
                    "Blue is the ocean where dolphins sing!",
                    "Yellow is the sun shining from above,",
                    "Pink is the flower that bunnies love!"
                ],
                "action_cues": ["Paint stroke in air", "Wiggle like dolphin", "Cup hands for sun"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Colors, colors, all around the world!",
                    "Every little flag and banner unfurled!",
                    "Swirl your brush and splash with glee, [Splash!]",
                    "Colors are as magical as can be!"
                ],
                "action_cues": ["Twirl brush in air", "Clap hands"]
            },
            {
                "type": "Outro",
                "lines": ["What a colorful masterpiece we made!", "Penny Bunny loves your creativity!", "Keep painting! Bye-bye! [Chime]"],
                "action_cues": ["Curtsy sweetly and wave"]
            }
        ]
    },
    {
        "number": 6,
        "id": "video_06",
        "title": "The Magical Number Train",
        "category": "Numbers & Counting",
        "lead_character_id": "zara_zebra",
        "target_age": "2-5 years",
        "bpm": 120,
        "tempo": "Upbeat 120 BPM",
        "educational_goals": ["Counting numbers 1 through 10", "Sequence ordering", "Train sound effects"],
        "hook": "Choo choo chugga chugga down the track, counting numbers forward and back!",
        "visual_theme": "Candy-cane railway winding through rainbow hills, tunnel of stars, and marshmallow clouds",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Choo choo! All aboard! Conductor Zara Zebra here!", "Listen to the train whistle blow!", "Let's count our train cars! [Whistle!]"],
                "action_cues": ["Pull train whistle cord", "March in place"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Car number one has a big red star,",
                    "Car number two travels near and far!",
                    "Three little bells go ring ring ring, [Ding!]",
                    "Car number four makes the whistle sing!"
                ],
                "action_cues": ["Show 1, 2, 3, 4 fingers", "Ring hand bell"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Chugga chugga choo choo, count with me,",
                    "Numbers on the train as easy as can be!",
                    "Rolling on the tracks under sunny skies, [Whistle!]",
                    "Counting to ten is a big surprise!"
                ],
                "action_cues": ["Train arm pistons motion", "Jump and shout choo choo"]
            },
            {
                "type": "Outro",
                "lines": ["The train reached the station!", "You counted all the cars so well!", "Choo choo and bye-bye! [Whistle!]"],
                "action_cues": ["Wave train conductor cap"]
            }
        ]
    },
    {
        "number": 7,
        "id": "video_07",
        "title": "Little Bunny's Bedtime Song",
        "category": "Bedtime & Calming",
        "lead_character_id": "penny_bunny",
        "target_age": "0-4 years",
        "bpm": 80,
        "tempo": "Gentle 80 BPM",
        "educational_goals": ["Calm transition to sleep", "Breathing regulation", "Feeling safe and loved"],
        "hook": "Close your sleepy eyes, soft and sweet, Penny Bunny tucks your little feet.",
        "visual_theme": "Lavender twilight sky, crescent moon rocking gently, floating pastel stars",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Shh, little sleepyhead. It's Penny Bunny.", "The stars are coming out to say goodnight.", "Let's snuggle in our blanket. [Chime]"],
                "action_cues": ["Gentle whisper", "Pull soft blanket up"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "The moon is shining like a silver pearl,",
                    "Goodnight to every little boy and girl.",
                    "The little birds have tucked their wings in tight,",
                    "Rest your sleepy head until morning light."
                ],
                "action_cues": ["Slow sway", "Rest head on hands"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Hush-a-bye, sleepy star, glowing from above,",
                    "You are wrapped in gentle bedtime love.",
                    "Breathe in slow, breathe out sweet, [Chime]",
                    "Dreamland is waiting for your sleepy feet."
                ],
                "action_cues": ["Slow deep breath", "Soft rocking motion"]
            },
            {
                "type": "Outro",
                "lines": ["Sweet dreams, darling friend.", "Penny Bunny loves you so much.", "Goodnight, sleep tight. [Chime]"],
                "action_cues": ["Blow a gentle goodnight kiss"]
            }
        ]
    },
    {
        "number": 8,
        "id": "video_08",
        "title": "The Animal Sounds Party",
        "category": "Animals & Nature",
        "lead_character_id": "barnaby_bear",
        "target_age": "1-4 years",
        "bpm": 124,
        "tempo": "Energetic 124 BPM",
        "educational_goals": ["Animal vocalizations (Woof, Meow, Moo, Oink, Roar)", "Auditory processing"],
        "hook": "Lions roar and puppies bark, party with Barnaby in the animal park!",
        "visual_theme": "Sunny safari festival with colorful party banners, dancing balloons, and safari tents",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Welcome to the Animal Party! I'm Barnaby Bear!", "All our animal friends are here to sing!", "Show me your best animal sounds! [Roar!]"],
                "action_cues": ["Clap hands", "Cup ear to listen"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "The happy little puppy goes woof woof woof!",
                    "Chasing his ball on the sunny roof! [Bark!]",
                    "The spotted gentle cow goes moo moo moo,",
                    "Chewing on the grass under skies of blue!"
                ],
                "action_cues": ["Puppy paw motion", "Cow horn gesture"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Animal sounds, animal cheer,",
                    "The happiest party in the whole wide year!",
                    "Bark, meow, moo, and roar with me, [Roar!]",
                    "Wild and happy as we can be!"
                ],
                "action_cues": ["Dance and bounce", "Roar playfully"]
            },
            {
                "type": "Outro",
                "lines": ["What a noisy, joyful animal party!", "You made the best animal sounds!", "High five from Barnaby! Bye-bye! [Pop!]"],
                "action_cues": ["High five towards camera", "Wave goodbye"]
            }
        ]
    },
    {
        "number": 9,
        "id": "video_09",
        "title": "Brush Your Teeth Every Day",
        "category": "Daily Habits & Hygiene",
        "lead_character_id": "barnaby_bear",
        "target_age": "1-5 years",
        "bpm": 120,
        "tempo": "Bouncy 120 BPM",
        "educational_goals": ["Morning and evening brushing habit", "Circular brushing technique", "Positive health attitude"],
        "hook": "Up and down, round and round, sparkly teeth without a frown!",
        "visual_theme": "Bright bubbly bathroom with giant rainbow toothbrush, smiling toothpaste tube, and sparkling mirrors",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Time for tooth care! It's Barnaby Bear!", "Got your colorful toothbrush ready?", "Let's make our teeth sparkle clean! [Chime]"],
                "action_cues": ["Hold up toothbrush", "Big wide smile"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "A dab of yummy paste, just like a little pea,",
                    "Brush front and back so happily!",
                    "Up and down, up and down, clean every bite,",
                    "Brush in the morning and brush at night!"
                ],
                "action_cues": ["Pretend to squeeze tube", "Up and down brushing motion"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Brush, brush, brush your teeth, round and round!",
                    "The cleanest, brightest smile in town! [Pop!]",
                    "Spit in the sink, rinse with a swish, [Splash!]",
                    "Sparkly clean is our happy wish!"
                ],
                "action_cues": ["Circular brushing gesture", "Rinse and swish puff cheeks"]
            },
            {
                "type": "Outro",
                "lines": ["Look at those dazzling, sparkly teeth!", "Barnaby Bear is so proud of you!", "Keep brushing every day! Bye-bye! [Chime]"],
                "action_cues": ["Point to shiny teeth", "Thumbs up and wave"]
            }
        ]
    },
    {
        "number": 10,
        "id": "video_10",
        "title": "The Happy Farm Adventure",
        "category": "Animals & Agriculture",
        "lead_character_id": "zara_zebra",
        "secondary_character_id": "pip_bird",
        "target_age": "1-4 years",
        "bpm": 120,
        "tempo": "Lively 120 BPM",
        "educational_goals": ["Farm animals (Pig, sheep, horse, hen)", "Rural vocabulary (Barn, tractor, hay)"],
        "hook": "Tractor rolling on the farm, sunny morning bright and warm!",
        "visual_theme": "Red wooden barn, yellow hay bales, friendly green pastures, and smiling sunflowers",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Welcome to the Happy Farm! Zara Zebra here with Pip!", "Look at that big red barn!", "Let's say hello to all the farm friends! [Chirp!]"],
                "action_cues": ["Wave farmer hat", "Point to barn"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "The pink little piggies play in the hay, [Oink!]",
                    "Oinking and rolling the morning away!",
                    "The fluffy white sheep say baa baa baa,",
                    "Happiest sheep you ever saw!"
                ],
                "action_cues": ["Snout wiggle motion", "Fluffy wool arms"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "On the Happy Farm with Zara and Pip,",
                    "Taking a joyful countryside trip!",
                    "Tractor goes putter putter down the lane, [Chug!]",
                    "Sunshine washing away the rain!"
                ],
                "action_cues": ["Steer tractor", "Wave both hands"]
            },
            {
                "type": "Outro",
                "lines": ["What a wonderful day on the farm!", "Pip and Zara love visiting the animals!", "See you at the barn! Bye-bye! [Chime]"],
                "action_cues": ["Bow together and wave"]
            }
        ]
    },
    {
        "number": 11,
        "id": "video_11",
        "title": "Shapes in My Toy Box",
        "category": "Early Math & Geometry",
        "lead_character_id": "sunny",
        "target_age": "2-5 years",
        "bpm": 116,
        "tempo": "Bouncy 116 BPM",
        "educational_goals": ["Identify Circle, Square, Triangle, Star", "Tracing shapes with fingers"],
        "hook": "Round like a ball, square like a block, find all the shapes in the ticking clock!",
        "visual_theme": "Playroom with giant building blocks, shape sorter, plush carpet, and sunny window",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Good morning sunshine friends! It's Sunny!", "Look inside my magical toy box!", "Let's discover all the lovely shapes! [Giggle]"],
                "action_cues": ["Beam brightly", "Open toy chest lid"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "A circle is round, it rolls on the floor,",
                    "A square has four sides, just like the front door!",
                    "A triangle has points, one, two, and three,",
                    "Look at the shapes with happy Sunny!"
                ],
                "action_cues": ["Trace circle in air", "Trace square in air", "Make triangle with fingers"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Shapes, shapes, everywhere you see,",
                    "Building and learning for you and me!",
                    "Round like the sun, tall like a tree, [Pop!]",
                    "Shapes are as fun as fun can be!"
                ],
                "action_cues": ["Spin and sparkle", "Clap on downbeat"]
            },
            {
                "type": "Outro",
                "lines": ["You are a super shape master!", "Sunny is beaming with joy for you!", "Keep finding shapes! Bye-bye! [Chime]"],
                "action_cues": ["Radiate warm light and wave"]
            }
        ]
    },
    {
        "number": 12,
        "id": "video_12",
        "title": "Let's Learn Opposites",
        "category": "Cognitive & Language",
        "lead_character_id": "barnaby_bear",
        "secondary_character_id": "pip_bird",
        "target_age": "2-5 years",
        "bpm": 118,
        "tempo": "Playful 118 BPM",
        "educational_goals": ["Opposite pairs: Big/Small, Up/Down, Fast/Slow, Happy/Quiet", "Contrasting actions"],
        "hook": "Big like a bear, small like a bird, learn every wonderful opposite word!",
        "visual_theme": "Playground with seesaws, balance beams, tall ladders, and low tunnels",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Hello friends! Barnaby Bear and Pip are here!", "I am big, and Pip is small!", "Let's play the Opposites Game! [Chirp!]"],
                "action_cues": ["Stretch arms wide", "Point to tiny Pip"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Reach UP high to the fluffy cloud,",
                    "Crouch DOWN low, quiet not loud! [Shh!]",
                    "Run FAST like a cheetah on the go,",
                    "Walk SLOW like a turtle nice and low!"
                ],
                "action_cues": ["Reach high", "Crouch low", "Run on spot", "Slow-motion crawl"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Opposites, opposites, play along,",
                    "Dancing and singing our opposite song!",
                    "High and low, near and far, [Pop!]",
                    "You are our brilliant shining star!"
                ],
                "action_cues": ["Jump high", "Wave hands"]
            },
            {
                "type": "Outro",
                "lines": ["Great job with all the opposites!", "You learned them so quickly!", "Barnaby and Pip say goodbye! [Chime]"],
                "action_cues": ["Hug each other and wave"]
            }
        ]
    },
    {
        "number": 13,
        "id": "video_13",
        "title": "The Little Astronauts",
        "category": "Science & Exploration",
        "lead_character_id": "zara_zebra",
        "secondary_character_id": "sunny",
        "target_age": "2-5 years",
        "bpm": 122,
        "tempo": "Energetic 122 BPM",
        "educational_goals": ["Space exploration (Rocket, stars, moon, helmet)", "Countdown 5-4-3-2-1 Blast Off"],
        "hook": "5, 4, 3, 2, 1, blast off into space, zoom around the stars with a smile on your face!",
        "visual_theme": "Pastel cosmos with smiling purple planets, friendly rings around Saturn, and a silver rocket",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Astronaut Zara Zebra checking in! Sunny is our star guide!", "Put on your space helmets, cadets!", "Countdown with me! 5, 4, 3, 2, 1... BLAST OFF! [Whoosh!]"],
                "action_cues": ["Put on space helmet", "Rocket blast off jump"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Zooming past the glowing moon,",
                    "Playing a zero-gravity tune!",
                    "Floating like a feather in the cosmic breeze,",
                    "Past the Milky Way and the starry seas!"
                ],
                "action_cues": ["Floating arm movement", "Slow-motion kicks"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Little astronauts flying high,",
                    "Rocket ship sailing across the sky!",
                    "Wave to Earth, say hello to Mars, [Chime]",
                    "Dancing happily among the stars!"
                ],
                "action_cues": ["Wave towards Earth", "Spin gently like floating"]
            },
            {
                "type": "Outro",
                "lines": ["Mission complete, space explorers!", "Zara and Sunny safely landed home!", "Keep reaching for the stars! Bye-bye! [Chime]"],
                "action_cues": ["Salute playfully and wave"]
            }
        ]
    },
    {
        "number": 14,
        "id": "video_14",
        "title": "Rain Rain Rainbow Day",
        "category": "Weather & Nature",
        "lead_character_id": "sunny",
        "target_age": "1-4 years",
        "bpm": 114,
        "tempo": "Playful 114 BPM",
        "educational_goals": ["Rain and sunshine cycle", "Rainbow formation", "Splashing in puddles in boots"],
        "hook": "Pitter patter raindrop, puddle jumping fun, rain and sunshine make a rainbow for everyone!",
        "visual_theme": "Spring garden with rain puddles, yellow rain boots, smiling clouds, and radiant rainbow arch",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Pitter patter! It's Sunny with some rainy day magic!", "Put on your little yellow boots!", "Let's splash and find the rainbow! [Splash!]"],
                "action_cues": ["Wiggle fingers like falling rain", "Stomp yellow boots"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Pitter patter raindrops falling from the cloud, [Drip!]",
                    "Little frogs are singing happy and loud!",
                    "When the rain stops and the sunshine glows,",
                    "A beautiful rainbow arching through the rose!"
                ],
                "action_cues": ["Flutter fingers downward", "Trace large arch with both arms"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Rain, rain, puddle jump splash! [Splash!]",
                    "Sunny smiling in a flash!",
                    "Red and orange, yellow, green, and blue,",
                    "Rainbow day is sparkling for you!"
                ],
                "action_cues": ["Jump into pretend puddle", "Beam wide smile"]
            },
            {
                "type": "Outro",
                "lines": ["The sky is bright and clear!", "Sunny brings the warm smiles every time!", "See you under the rainbow! Bye-bye! [Chime]"],
                "action_cues": ["Warm rays glow", "Wave goodbye"]
            }
        ]
    },
    {
        "number": 15,
        "id": "video_15",
        "title": "Clean Up Toy Song",
        "category": "Social & Emotional Learning",
        "lead_character_id": "barnaby_bear",
        "target_age": "1-5 years",
        "bpm": 120,
        "tempo": "Bouncy 120 BPM",
        "educational_goals": ["Responsibility and tidiness", "Teamwork and helping", "Positive habit transition"],
        "hook": "Pick up toys, one by one, cleaning up together is super duper fun!",
        "visual_theme": "Cheerful nursery room with toy bins, teddy shelves, colorful rugs, and sparkling clean floors",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Playtime was wonderful! Barnaby Bear here!", "Now it's time for our Clean Up Song!", "Let's help each other put the toys away! [Chime]"],
                "action_cues": ["Look at scattered toys", "Open colorful toy box"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Put the blocks into the wooden crate,",
                    "Stacking them up so neat and straight!",
                    "Put the cuddly teddy on the cozy bed,",
                    "Resting his sweet little furry head!"
                ],
                "action_cues": ["Pick up block and place inside", "Pat teddy bear"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Clean up, clean up, everybody everywhere!",
                    "Clean up, clean up, show how much you care!",
                    "Put away the cars, put away the dolls, [Pop!]",
                    "A tidy happy room for one and all!"
                ],
                "action_cues": ["Gather motion with arms", "High five gesture"]
            },
            {
                "type": "Outro",
                "lines": ["Look how clean and sparkling our room is!", "Barnaby Bear gives you a big teddy hug!", "Great helping today! Bye-bye! [Chime]"],
                "action_cues": ["Bear hug motion", "Wave goodbye"]
            }
        ]
    },
    {
        "number": 16,
        "id": "video_16",
        "title": "The Jungle Counting Adventure",
        "category": "Numbers & Counting",
        "lead_character_id": "pip_bird",
        "target_age": "2-5 years",
        "bpm": 118,
        "tempo": "Rhythmic 118 BPM",
        "educational_goals": ["Counting objects 1 through 5", "Jungle wildlife (Monkeys, parrots, frogs)", "Rhythmic chanting"],
        "hook": "Count the coconuts, count the vines, singing along where the jungle shines!",
        "visual_theme": "Emerald jungle canopy with friendly vines, waterfalls, giant smiling leaves, and golden sunlight",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Chirp chirp! Welcome to the Jungle! I'm Pip the Bird!", "Look at all the tall green trees!", "Let's count our jungle friends! [Chirp!]"],
                "action_cues": ["Flutter through leaves", "Perch on tropical branch"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "One funny monkey swinging on the vine, [Ooh!]",
                    "Two golden butterflies looking so fine!",
                    "Three little tree frogs hopping in the dew, [Boing!]",
                    "Singing a jungle song for me and you!"
                ],
                "action_cues": ["Swing arm like vine", "Flutter two fingers", "Three little hops"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "One, two, three, four, jungle counting fun!",
                    "Dancing in the shade, dancing in the sun!",
                    "Chirp with Pip, count along with glee, [Chirp!]",
                    "Wild and wonderful under the tree!"
                ],
                "action_cues": ["Count on fingers", "Twirl wings"]
            },
            {
                "type": "Outro",
                "lines": ["You are the greatest jungle counter!", "Pip the Bird loves exploring with you!", "Fly high little friends! Bye-bye! [Chirp!]"],
                "action_cues": ["Flutter upwards joyfully"]
            }
        ]
    },
    {
        "number": 17,
        "id": "video_17",
        "title": "Happy Birthday Party Song",
        "category": "Celebrations & Milestones",
        "lead_character_id": "barnaby_bear",
        "secondary_character_id": "penny_bunny",
        "target_age": "1-6 years",
        "bpm": 120,
        "tempo": "Celebratory 120 BPM",
        "educational_goals": ["Celebrating birthdays and growth", "Kindness and sharing joy", "Blowing out candles"],
        "hook": "Blow out the candles, make a happy wish, birthday party with your favorite dish!",
        "visual_theme": "Party garden with confetti, tiered strawberry cake, colorful balloons, and party hats",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Happy Birthday, special friend! Barnaby and Penny are here!", "Look at the colorful cake and balloons!", "Let's sing our Birthday Song! [Horn!]"],
                "action_cues": ["Hold birthday present", "Point to cake"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Another year older, taller every day,",
                    "Laughing and smiling in every single way!",
                    "Put on your party hat, spin all around,",
                    "Happiest birthday anywhere to be found!"
                ],
                "action_cues": ["Measure height with hand", "Spin in circle"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Happy Birthday to you, hip hip hooray! [Cheer!]",
                    "It's your extra special celebration day!",
                    "Blow out the candles, make a big wish, [Whoosh!]",
                    "Sweet hugs and love on your birthday dish!"
                ],
                "action_cues": ["Cheer with hands up", "Blow candles motion"]
            },
            {
                "type": "Outro",
                "lines": ["Hooray for you! Have the best birthday ever!", "All your TinyTots friends love you!", "Happy Birthday! Bye-bye! [Chime]"],
                "action_cues": ["Blow party horn", "Wave both hands"]
            }
        ]
    },
    {
        "number": 18,
        "id": "video_18",
        "title": "Please and Thank You Song",
        "category": "Social Manners & Kindness",
        "lead_character_id": "penny_bunny",
        "target_age": "1-5 years",
        "bpm": 112,
        "tempo": "Warm 112 BPM",
        "educational_goals": ["Polite vocabulary (Please, Thank You, You're Welcome)", "Sharing and empathy"],
        "hook": "Two magic words that make the whole world smile, please and thank you go the extra mile!",
        "visual_theme": "Cozy tea party meadow with miniature teapot, carrot cupcakes, and friendly wooden table",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Hello polite friends! Penny Bunny here!", "Do you know the two magic words?", "They make everybody feel warm and loved! [Chime]"],
                "action_cues": ["Curtsy gently", "Hold hands over heart"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "When you want a yummy apple off the plate,",
                    "Say 'Please' so kindly, you don't even have to wait!",
                    "When somebody shares a toy with you today,",
                    "Say 'Thank You very much!' in a happy way!"
                ],
                "action_cues": ["Polite hand gesture", "Smile and nod"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Please and Thank You, the magic words to say,",
                    "Spreading little sparkles every single day! [Sparkle!]",
                    "Kindness in your heart, a smile on your face,",
                    "Making our world a happier, sweeter place!"
                ],
                "action_cues": ["Flutter fingers like sparkles", "Big warm smile"]
            },
            {
                "type": "Outro",
                "lines": ["Thank you for being so polite and kind!", "Penny Bunny sends you big bunny hugs!", "Have a magical day! Bye-bye! [Chime]"],
                "action_cues": ["Blow sweet kiss", "Wave goodbye"]
            }
        ]
    },
    {
        "number": 19,
        "id": "video_19",
        "title": "Good Morning Sunshine",
        "category": "Morning Routine & Awakening",
        "lead_character_id": "sunny",
        "target_age": "0-4 years",
        "bpm": 116,
        "tempo": "Warm & Gentle 116 BPM",
        "educational_goals": ["Positive awakening attitude", "Stretching muscles", "Greeting the day with joy"],
        "hook": "Rise and shine, the day is new, Sunny brings a golden smile to you!",
        "visual_theme": "Sunrise horizon with pink dawn clouds, singing bluebirds on a fence, and blossoming daisies",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Cock-a-doodle-doo! Good morning! It's Sunny!", "Wake up, wake up, little sleepyhead!", "The sun is rising in the sky! [Chime]"],
                "action_cues": ["Rise from horizon", "Stretch arms wide"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "Stretch your arms up high to the morning light,",
                    "Wiggle your tiny toes, say goodbye to the night!",
                    "The little birds are singing in the leafy tree, [Chirp!]",
                    "Ready for an adventure with you and me!"
                ],
                "action_cues": ["Big yawn and stretch", "Wiggle toes and hands"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Good morning sunshine, hello bright blue day,",
                    "Put on your happy smile, come on out to play! [Giggle]",
                    "Today is full of wonders waiting to be found,",
                    "Joy and happiness all around!"
                ],
                "action_cues": ["Sunray sparkle gesture", "Clap cheerfully"]
            },
            {
                "type": "Outro",
                "lines": ["Have the most wonderful day today!", "Sunny will be shining over you all day long!", "Good morning, friends! Bye-bye! [Chime]"],
                "action_cues": ["Warm golden glow", "Wave goodbye"]
            }
        ]
    },
    {
        "number": 20,
        "id": "video_20",
        "title": "The Little Ocean Explorers",
        "category": "Science & Marine Life",
        "lead_character_id": "pip_bird",
        "secondary_character_id": "zara_zebra",
        "target_age": "2-5 years",
        "bpm": 118,
        "tempo": "Lively 118 BPM",
        "educational_goals": ["Ocean life (Dolphin, sea turtle, starfish, octopus)", "Submarine navigation"],
        "hook": "Down in the yellow submarine so deep, waving to the friendly fish that leap!",
        "visual_theme": "Bioluminescent coral reef with purple sea anemones, sea turtles, bubbles, and yellow submarine",
        "sections": [
            {
                "type": "Intro",
                "lines": ["Dive dive dive! Captain Pip and Zara are exploring the ocean!", "Look through the submarine porthole!", "Let's meet our sea friends! [Bubble!]"],
                "action_cues": ["Periscope looking gesture", "Pop imaginary bubbles"]
            },
            {
                "type": "Verse 1",
                "lines": [
                    "A friendly little dolphin jumping in the spray, [Splash!]",
                    "A wise sea turtle paddling on his way!",
                    "Five-armed starfish resting on the sand,",
                    "Underwater beauty in a magical land!"
                ],
                "action_cues": ["Dolphin dive hand motion", "Swimming paddle arms"]
            },
            {
                "type": "Chorus",
                "lines": [
                    "Bubble bubble pop, in the ocean blue, [Pop!]",
                    "Swimming with the fishies, learning something new!",
                    "Splashing with our flippers, dancing with the tide,",
                    "On our sunny submarine ocean ride!"
                ],
                "action_cues": ["Pop bubbles with fingers", "Wiggle body like swimming fish"]
            },
            {
                "type": "Outro",
                "lines": ["Surface the submarine! What an amazing ocean dive!", "Pip and Zara loved exploring with you!", "Swim back soon! Bye-bye! [Chime]"],
                "action_cues": ["Submarine horn beep", "Wave goodbye"]
            }
        ]
    }
]

class Curriculum20Manager:
    """Manages the 20-video preschool curriculum catalog."""

    @classmethod
    def get_catalog(cls) -> List[Dict[str, Any]]:
        return SONG_CATALOG_20

    @classmethod
    def get_song_by_number(cls, num: int) -> Optional[Dict[str, Any]]:
        for s in SONG_CATALOG_20:
            if s["number"] == num:
                return s
        return None

    @classmethod
    def get_song_by_id(cls, song_id: str) -> Optional[Dict[str, Any]]:
        for s in SONG_CATALOG_20:
            if s["id"].lower() == song_id.lower():
                return s
        return None

    @classmethod
    def get_song_by_title(cls, title: str) -> Optional[Dict[str, Any]]:
        norm = title.strip().lower()
        for s in SONG_CATALOG_20:
            if s["title"].lower() in norm or norm in s["title"].lower():
                return s
        return None

catalog_manager = Curriculum20Manager()
