#!/usr/bin/env python3
"""
Generate synthetic data for Part 2 of the Advanced RAG assignment.
Creates:
- CSV file with 1000 rows of daily product sales data
- Unstructured text files with product descriptions and reviews
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# Categories and products
CATEGORIES = {
    "Electronics": [
        ("ELEC001", "Wireless Bluetooth Headphones", 79.99),
        ("ELEC002", "USB-C Fast Charger", 24.99),
        ("ELEC003", "Portable Power Bank 20000mAh", 49.99),
        ("ELEC004", "Smart Watch Pro", 199.99),
    ],
    "Home & Kitchen": [
        ("HOME001", "Stainless Steel Coffee Maker", 89.99),
        ("HOME002", "Non-Stick Frying Pan Set", 45.99),
        ("HOME003", "Air Fryer 5.5L", 129.99),
    ],
    "Sports & Outdoors": [
        ("SPRT001", "Yoga Mat Premium", 34.99),
        ("SPRT002", "Resistance Bands Set", 19.99),
        ("SPRT003", "Hiking Backpack 40L", 79.99),
        ("SPRT004", "Camping Tent 4-Person", 149.99),
    ],
    "Beauty & Personal Care": [
        ("BEAU001", "Vitamin C Serum", 28.99),
        ("BEAU002", "Hair Dryer Professional", 59.99),
        ("BEAU003", "Electric Toothbrush", 49.99),
    ],
    "Clothing": [
        ("CLTH001", "Running Shoes Men", 89.99),
        ("CLTH002", "Winter Jacket Women", 129.99),
        ("CLTH003", "Cotton T-Shirt Pack (3)", 29.99),
        ("CLTH004", "Denim Jeans Classic", 54.99),
    ],
    "Books": [
        ("BOOK001", "Python Programming Guide", 44.99),
        ("BOOK002", "The Art of Cooking", 32.99),
        ("BOOK003", "Mystery Novel Collection", 24.99),
    ],
    "Toys & Games": [
        ("TOYS001", "Building Blocks Set 500pc", 39.99),
        ("TOYS002", "Board Game Strategy", 34.99),
        ("TOYS003", "Remote Control Car", 49.99),
    ],
    "Office Supplies": [
        ("OFFC001", "Ergonomic Office Chair", 249.99),
        ("OFFC002", "LED Desk Lamp", 39.99),
        ("OFFC003", "Notebook Set Premium", 18.99),
        ("OFFC004", "Wireless Mouse", 29.99),
    ],
    "Pet Supplies": [
        ("PETS001", "Dog Food Premium 10kg", 54.99),
        ("PETS002", "Cat Scratching Post", 44.99),
        ("PETS003", "Pet Carrier Medium", 39.99),
    ],
    "Food & Grocery": [
        ("FOOD001", "Organic Coffee Beans 1kg", 24.99),
        ("FOOD002", "Protein Bars Box (12)", 29.99),
        ("FOOD003", "Green Tea Collection", 19.99),
    ],
}

REGIONS = ["North", "South", "East", "West", "Central"]


def _generate_sales_csv(
    output_path: Path,
    num_rows: int = 1000
) -> None:
    """Generate CSV file with daily product sales data."""

    # Flatten products list
    all_products = []
    for category, products in CATEGORIES.items():
        for product_id, product_name, base_price in products:
            all_products.append({
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "base_price": base_price,
            })

    # Generate date range (last 90 days)
    end_date = datetime(2024, 12, 31)
    start_date = end_date - timedelta(days=89)

    rows = []
    for _ in range(num_rows):
        product = random.choice(all_products)

        # Random date in range
        days_offset = random.randint(0, 89)
        sale_date = start_date + timedelta(days=days_offset)

        # Units sold (weighted by product popularity)
        base_units = random.randint(1, 50)
        if product["category"] in ["Electronics", "Clothing"]:
            base_units = int(base_units * 1.5)

        # Price variation (occasional discounts)
        price = product["base_price"]
        if random.random() < 0.2:  # 20% chance of discount
            price = round(price * random.uniform(0.8, 0.95), 2)

        rows.append({
            "date": sale_date.strftime("%Y-%m-%d"),
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "units_sold": base_units,
            "unit_price": price,
            "total_revenue": round(base_units * price, 2),
            "region": random.choice(REGIONS),
        })

    # Sort by date
    rows.sort(key=lambda x: x["date"])

    # Write CSV
    fieldnames = [
        "date",
        "product_id",
        "product_name",
        "category",
        "units_sold",
        "unit_price",
        "total_revenue",
        "region",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {num_rows} sales records in {output_path}")


def _generate_product_pages(
    output_dir: Path
) -> None:
    """Generate unstructured text files with product descriptions and reviews."""

    product_content = {
        "ELEC001": """
========================================
WIRELESS BLUETOOTH HEADPHONES - PRODUCT PAGE
========================================

Product: Wireless Bluetooth Headphones
Brand: SoundMax Pro
Price: $79.99
SKU: ELEC001
Category: Electronics

PRODUCT DESCRIPTION:
Experience crystal-clear audio with our premium Wireless Bluetooth Headphones.
Featuring advanced noise-cancellation technology and 40-hour battery life, these
headphones are perfect for commuting, working from home, or enjoying your favorite
music without interruption.

Key Features:
- Active Noise Cancellation (ANC) with transparency mode
- Bluetooth 5.2 for stable connectivity up to 30ft range
- 40-hour battery life, quick charge (10 min = 3 hours playback)
- Premium memory foam ear cushions for all-day comfort
- Foldable design with carrying case included
- Built-in microphone for calls and voice assistant

Technical Specifications:
- Driver size: 40mm
- Frequency response: 20Hz - 20kHz
- Impedance: 32 ohms
- Weight: 254g

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Sarah M. (Verified Purchase) - 5 stars
"Best headphones I've ever owned! The noise cancellation is incredible - I can't
hear my noisy neighbors anymore. Battery lasts forever and they're super comfortable
even during long work sessions. Worth every penny!"

Review 2 - Mike T. (Verified Purchase) - 4 stars
"Great sound quality and the ANC works well. Only giving 4 stars because the
Bluetooth occasionally drops when my phone is in my back pocket. Otherwise fantastic
value for the price."

Review 3 - Jennifer L. (Verified Purchase) - 5 stars
"I use these for my daily 2-hour commute and they've been a game changer. The
transparency mode is perfect for announcements on the train. Very impressed with
build quality."

Review 4 - David R. (Verified Purchase) - 3 stars
"Sound is good but they feel a bit tight on my head. After about 2 hours I need
to take a break. The noise cancellation is decent but not as good as the premium
brands. Good for the price though."

Review 5 - Amanda K. (Verified Purchase) - 5 stars
"Bought these for my son's birthday and he absolutely loves them. Great for
gaming and music. The microphone quality is surprisingly good for video calls too."

Average Rating: 4.4/5 (2,847 reviews)
----------------------------------------
""",

        "HOME003": """
========================================
AIR FRYER 5.5L - PRODUCT PAGE
========================================

Product: Air Fryer 5.5L
Brand: KitchenPro Elite
Price: $129.99
SKU: HOME003
Category: Home & Kitchen

PRODUCT DESCRIPTION:
Transform your cooking with the KitchenPro Elite Air Fryer. This 5.5-liter capacity
air fryer uses rapid air circulation technology to cook food with up to 85% less oil
than traditional frying methods. Perfect for families, it can prepare meals for 4-6
people in minutes.

Key Features:
- 5.5L large capacity basket (fits a whole chicken)
- 8 preset cooking programs (fries, chicken, steak, fish, shrimp, cake, pizza, vegetables)
- Temperature range: 80°C to 200°C (175°F to 400°F)
- 60-minute timer with auto shut-off
- Digital LED touchscreen display
- Dishwasher-safe removable basket and pan
- Cool-touch exterior with non-slip base
- Recipe book included with 50+ recipes

Technical Specifications:
- Power: 1700W
- Voltage: 120V/60Hz
- Dimensions: 14" x 11" x 13"
- Weight: 12.5 lbs
- Cord length: 3 feet

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Patricia W. (Verified Purchase) - 5 stars
"This air fryer has completely changed how I cook! Made the crispiest french fries
I've ever had at home. My kids now prefer my homemade chicken nuggets over fast food.
Easy to clean and the presets work perfectly."

Review 2 - Robert H. (Verified Purchase) - 5 stars
"Finally replaced my old deep fryer and couldn't be happier. Everything comes out
crispy without the guilt. Made salmon last night and it was restaurant quality.
The 5.5L size is perfect for our family of 4."

Review 3 - Lisa G. (Verified Purchase) - 4 stars
"Great product overall. Takes a bit of learning to get temperatures right for
different foods. Wish the cord was longer - had to rearrange my counter. But the
food quality is excellent and cleanup is a breeze."

Review 4 - James C. (Verified Purchase) - 5 stars
"I was skeptical about air fryers but this one converted me. Made wings for game
day and they were incredible. The basket size is generous - I can fit 2 lbs of wings
easily. Highly recommend!"

Review 5 - Maria S. (Verified Purchase) - 4 stars
"Good air fryer, heats up quickly and cooks evenly. The only downside is it's a
bit loud during operation. But the results are worth it - everything is so crispy!"

Average Rating: 4.6/5 (5,234 reviews)
----------------------------------------
""",

        "SPRT001": """
========================================
YOGA MAT PREMIUM - PRODUCT PAGE
========================================

Product: Yoga Mat Premium
Brand: ZenFlex
Price: $34.99
SKU: SPRT001
Category: Sports & Outdoors

PRODUCT DESCRIPTION:
Elevate your yoga practice with the ZenFlex Premium Yoga Mat. Made from eco-friendly
TPE material, this mat provides the perfect balance of cushioning and stability. The
dual-layer construction offers superior grip on both sides, ensuring your mat stays
in place on any surface.

Key Features:
- Eco-friendly TPE material, free of PVC, latex, and toxic chemicals
- Extra thick 6mm cushioning for joint protection
- Double-sided non-slip texture
- Lightweight (2.5 lbs) and easy to carry
- Includes carrying strap
- Dimensions: 72" x 24" (183cm x 61cm)
- Available in 8 colors
- Closed-cell construction prevents sweat absorption
- Easy to clean with damp cloth

Best For:
- Yoga (all styles including hot yoga)
- Pilates
- Floor exercises
- Meditation
- Stretching

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Emily R. (Verified Purchase) - 5 stars
"Finally found the perfect yoga mat! The thickness is just right - my knees don't
hurt during kneeling poses anymore. The grip is amazing even when I sweat during
hot yoga. Love the sage green color too!"

Review 2 - Michael B. (Verified Purchase) - 4 stars
"Good quality mat for the price. Took a few days for the initial smell to go away
but now it's fine. Grip is excellent and it hasn't stretched or torn after 6 months
of daily use."

Review 3 - Priya K. (Verified Purchase) - 5 stars
"As a yoga instructor, I've tried dozens of mats. This one offers excellent value.
My students always ask about it. The carrying strap is a nice bonus. Will definitely
buy another when this one wears out."

Review 4 - Tom J. (Verified Purchase) - 5 stars
"Use this for my daily stretching routine and occasional yoga. The cushioning is
perfect for my hardwood floors. Very happy with the purchase. Cleaning is easy -
just wipe it down and let it air dry."

Review 5 - Sophia L. (Verified Purchase) - 4 stars
"Great mat overall! Only issue is it's slightly slippery when completely dry. Once
I warm up a bit and have some moisture on my hands, the grip is perfect. Beautiful
purple color exactly as pictured."

Average Rating: 4.5/5 (3,112 reviews)
----------------------------------------
""",

        "BEAU001": """
========================================
VITAMIN C SERUM - PRODUCT PAGE
========================================

Product: Vitamin C Serum
Brand: GlowLab Skincare
Price: $28.99
SKU: BEAU001
Category: Beauty & Personal Care

PRODUCT DESCRIPTION:
Reveal brighter, more youthful skin with GlowLab's Vitamin C Serum. This powerful
antioxidant formula combines 20% Vitamin C (L-Ascorbic Acid) with Vitamin E and
Hyaluronic Acid to reduce dark spots, fine lines, and sun damage while hydrating
and protecting your skin.

Key Ingredients:
- 20% L-Ascorbic Acid (Vitamin C) - brightens and evens skin tone
- Vitamin E - enhances antioxidant protection
- Hyaluronic Acid - deep hydration and plumping
- Ferulic Acid - stabilizes vitamins C and E, boosts effectiveness
- Aloe Vera - soothes and calms skin

Benefits:
- Reduces appearance of dark spots and hyperpigmentation
- Minimizes fine lines and wrinkles
- Boosts collagen production
- Protects against environmental damage
- Brightens dull, tired-looking skin
- Suitable for all skin types

How to Use:
1. Cleanse face thoroughly
2. Apply 3-4 drops to face and neck
3. Gently pat until absorbed
4. Follow with moisturizer
5. Use SPF during daytime (Vitamin C increases sun sensitivity)
Best used in morning routine for antioxidant protection throughout the day.

Size: 1 fl oz (30ml)
Shelf Life: Use within 3 months of opening

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Nicole T. (Verified Purchase) - 5 stars
"I've been using this serum for 8 weeks and the results are incredible! My dark
spots from sun damage have faded significantly. My skin looks so much brighter and
more even. I've tried expensive brands and this works just as well!"

Review 2 - Rachel M. (Verified Purchase) - 5 stars
"This serum has transformed my skin! I'm 45 and people keep asking what I'm using.
The texture is perfect - not sticky at all. Absorbs quickly and layers well under
makeup. Worth every penny."

Review 3 - Ashley P. (Verified Purchase) - 4 stars
"Good serum with visible results. The only reason I'm not giving 5 stars is because
it has a slight orange tint that concerned me at first (apparently normal for
Vitamin C). Otherwise, love the results after 6 weeks of use."

Review 4 - Kim H. (Verified Purchase) - 3 stars
"Decent product but caused some irritation initially. Had to start with every other
day application. Now my skin has adjusted and I see improvement in brightness. If
you have sensitive skin, introduce it slowly."

Review 5 - Danielle F. (Verified Purchase) - 5 stars
"I've repurchased this 3 times already! It's my holy grail product. My acne scars
have faded and my skin glows. The dropper makes it easy to apply. Just make sure to
store it in a cool, dark place."

Average Rating: 4.3/5 (8,567 reviews)
----------------------------------------
""",

        "CLTH001": """
========================================
RUNNING SHOES MEN - PRODUCT PAGE
========================================

Product: Running Shoes Men
Brand: StrideMax Athletics
Price: $89.99
SKU: CLTH001
Category: Clothing

PRODUCT DESCRIPTION:
Engineered for performance and comfort, the StrideMax Running Shoes are designed
for runners of all levels. Featuring responsive cushioning and a breathable mesh
upper, these shoes provide the perfect blend of support and flexibility for your
daily runs or marathon training.

Key Features:
- Responsive foam midsole for energy return
- Breathable engineered mesh upper
- Reinforced heel counter for stability
- Rubber outsole with multi-directional traction pattern
- Padded collar and tongue for comfort
- Reflective details for visibility in low light
- Removable insole (compatible with orthotics)
- Weight: 9.8 oz (size 10)

Available Sizes: 7-14 (including half sizes)
Available Colors: Black/White, Navy/Red, Grey/Lime, All Black

Best For:
- Road running
- Treadmill workouts
- Daily training
- Casual athleisure wear

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Jason K. (Verified Purchase) - 5 stars
"These shoes are amazing for the price! I've run 200+ miles in them and they still
feel great. The cushioning is perfect for my daily 5K runs. True to size and the
breathability keeps my feet cool. Highly recommend!"

Review 2 - Mark D. (Verified Purchase) - 4 stars
"Solid running shoes. Good cushioning and support for my flat feet. The only issue
is they run slightly narrow - I have wide feet and had to go up half a size. Once I
got the right fit, they've been great for my marathon training."

Review 3 - Chris L. (Verified Purchase) - 5 stars
"Just finished a half marathon in these and zero complaints. No blisters, no hot
spots, just comfortable miles. The traction was excellent even on wet pavement.
Will definitely buy another pair when these wear out."

Review 4 - Steven R. (Verified Purchase) - 5 stars
"Best value running shoes I've owned. Compare favorably to shoes twice the price.
The foam cushioning bounces back nicely and hasn't compressed after 3 months of
regular use. The reflective details are a nice safety touch."

Review 5 - Brian T. (Verified Purchase) - 4 stars
"Good everyday training shoe. Not quite enough support for my long runs (15+ miles)
but perfect for shorter distances and speedwork. Love the Navy/Red color combo.
Looks great and performs well."

Average Rating: 4.4/5 (4,521 reviews)
----------------------------------------
""",

        "BOOK001": """
========================================
PYTHON PROGRAMMING GUIDE - PRODUCT PAGE
========================================

Product: Python Programming Guide
Author: Dr. Sarah Mitchell
Price: $44.99
SKU: BOOK001
Category: Books

PRODUCT DESCRIPTION:
Master Python programming from beginner to advanced with this comprehensive guide.
Written by Dr. Sarah Mitchell, a computer science professor with 20 years of
teaching experience, this book takes you on a journey from your first line of code
to building real-world applications.

Book Details:
- Pages: 650
- Format: Paperback (Hardcover also available)
- Publisher: TechBooks Publishing
- Publication Date: January 2024
- Edition: 3rd Edition (Updated for Python 3.12)
- ISBN: 978-1234567890

What You'll Learn:
- Python fundamentals (variables, data types, control structures)
- Object-oriented programming concepts
- File handling and data processing
- Working with databases (SQLite, PostgreSQL)
- Web development with Flask and Django
- Data analysis with Pandas and NumPy
- Machine learning basics with scikit-learn
- Best practices and coding standards
- 200+ practice exercises with solutions

Includes:
- Downloadable code examples
- Access to online video tutorials
- Chapter quizzes
- Real-world project walkthroughs

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Alex C. (Verified Purchase) - 5 stars
"This book took me from zero programming knowledge to building my own web app in
3 months. The explanations are clear, and the exercises really reinforce the
concepts. Dr. Mitchell has a gift for making complex topics accessible."

Review 2 - Jennifer W. (Verified Purchase) - 5 stars
"As a self-taught programmer, I had gaps in my knowledge. This book filled them
all. The OOP section finally made inheritance click for me. The projects at the end
of each chapter are practical and relevant. Highly recommend!"

Review 3 - Daniel K. (Verified Purchase) - 4 stars
"Great content and well-structured. The only reason for 4 stars is some of the
advanced chapters move a bit fast. But for beginners, the first 2/3 of the book
is absolutely perfect. Worth the investment."

Review 4 - Michelle P. (Verified Purchase) - 5 stars
"I'm a teacher and I use this book for my high school programming class. Students
love it! The examples are engaging and the progression is logical. The online
resources are an excellent bonus."

Review 5 - Ryan H. (Verified Purchase) - 4 stars
"Solid programming book. Covers a lot of ground. Some sections feel rushed,
especially machine learning - that topic really deserves its own book. But as an
all-in-one Python guide, it's excellent value."

Average Rating: 4.6/5 (2,234 reviews)
----------------------------------------
""",

        "TOYS001": """
========================================
BUILDING BLOCKS SET 500PC - PRODUCT PAGE
========================================

Product: Building Blocks Set 500pc
Brand: CreativeBricks
Price: $39.99
SKU: TOYS001
Category: Toys & Games

PRODUCT DESCRIPTION:
Unleash your child's creativity with the CreativeBricks 500-Piece Building Blocks
Set! Compatible with all major brick brands, this set includes a wide variety of
shapes, sizes, and colors to bring any imagination to life. Perfect for children
ages 4 and up.

Set Contents:
- 500 building blocks in 15 different colors
- Multiple shapes: standard bricks, plates, slopes, wheels, windows, doors
- 4 mini-figure bases
- 2 large base plates (10" x 10")
- Idea booklet with 20 building projects
- Sturdy storage container with handle

Features:
- Compatible with LEGO and other major brands
- Made from non-toxic ABS plastic
- Rounded edges for safety
- Easy-to-follow instruction booklet
- Encourages STEM learning and spatial reasoning
- Perfect for solo play or group activities

Age Recommendation: 4+ years
Small parts - not suitable for children under 3

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Karen M. (Verified Purchase) - 5 stars
"Bought this for my 6-year-old's birthday and he's obsessed! He plays with it for
hours every day. The quality is excellent - fits perfectly with our existing LEGO
collection. Great value compared to name brands."

Review 2 - John D. (Verified Purchase) - 5 stars
"As a parent on a budget, this set is a lifesaver. My kids don't notice any
difference from the expensive brands. The variety of pieces is great and the
storage container keeps everything organized. Will buy again!"

Review 3 - Laura S. (Verified Purchase) - 4 stars
"Good quality blocks at a great price. The only minor issue is a few pieces
didn't fit as tightly as name-brand blocks. But 95% of the pieces are perfect.
My daughter loves building houses and castles."

Review 4 - Michael R. (Verified Purchase) - 5 stars
"Perfect gift for my nephew. He's 5 and this was the perfect starting set. The
idea booklet gave him inspiration and now he's creating his own designs. Great
for developing creativity and fine motor skills."

Review 5 - Susan T. (Verified Purchase) - 4 stars
"Nice set with lots of pieces. Wish there were more specialized pieces like wheels
and windows. But for the price, you can't beat it. My kids have been playing with
these for months and they're still in great condition."

Average Rating: 4.5/5 (3,890 reviews)
----------------------------------------
""",

        "OFFC001": """
========================================
ERGONOMIC OFFICE CHAIR - PRODUCT PAGE
========================================

Product: Ergonomic Office Chair
Brand: ComfortZone Pro
Price: $249.99
SKU: OFFC001
Category: Office Supplies

PRODUCT DESCRIPTION:
Transform your workspace with the ComfortZone Pro Ergonomic Office Chair. Designed
in collaboration with orthopedic specialists, this chair provides all-day comfort
and support for professionals who spend long hours at their desk. Say goodbye to
back pain and hello to productivity!

Key Features:
- Adjustable lumbar support (height and depth)
- 4D adjustable armrests (height, width, depth, angle)
- Breathable mesh back for temperature regulation
- High-density foam seat cushion
- Adjustable headrest with neck support
- Seat height adjustment (gas lift)
- Seat depth adjustment
- Tilt tension control with lock
- 360-degree swivel
- Heavy-duty base with smooth-rolling casters
- Weight capacity: 300 lbs

Dimensions:
- Seat width: 20"
- Seat depth: 17-20" (adjustable)
- Back height: 24"
- Overall height: 45-52"

Certifications:
- BIFMA certified
- Greenguard certified (low emissions)

Warranty: 5 years

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Robert P. (Verified Purchase) - 5 stars
"After years of back pain from cheap office chairs, I finally invested in this
one. Game changer! The lumbar support is incredible and I can work 10+ hours
without discomfort. Assembly took about 45 minutes but instructions were clear."

Review 2 - Amanda L. (Verified Purchase) - 5 stars
"Working from home required a better chair - this exceeded expectations. The mesh
back keeps me cool during summer, and the armrests adjust every which way. It's
like they designed it for my body specifically. Worth every penny!"

Review 3 - David M. (Verified Purchase) - 4 stars
"Solid chair with great features. The only downside is the headrest doesn't quite
reach the right position for me (I'm 6'4"). But the lumbar and seat are perfect.
Still a huge upgrade from my previous chair."

Review 4 - Sarah K. (Verified Purchase) - 5 stars
"I'm a software developer and sit for 8-10 hours daily. This chair has eliminated
my chronic lower back pain. The adjustability is fantastic - took me a few days to
find my perfect settings but now it's perfection."

Review 5 - Paul H. (Verified Purchase) - 4 stars
"Great quality chair. Feels premium and looks professional in my home office.
Assembly was straightforward. Only wish is that the seat cushion was a bit softer -
it's quite firm, though I suppose that's better for support."

Average Rating: 4.6/5 (1,876 reviews)
----------------------------------------
""",

        "PETS001": """
========================================
DOG FOOD PREMIUM 10KG - PRODUCT PAGE
========================================

Product: Dog Food Premium 10kg
Brand: HealthyPaws Nutrition
Price: $54.99
SKU: PETS001
Category: Pet Supplies

PRODUCT DESCRIPTION:
Give your furry friend the nutrition they deserve with HealthyPaws Premium Dog
Food. Made with real chicken as the first ingredient and packed with wholesome
vegetables, this formula supports overall health, shiny coats, and strong muscles
for dogs of all breeds and sizes.

Key Ingredients:
- Real deboned chicken (35%)
- Brown rice and oatmeal for digestible carbohydrates
- Sweet potatoes and carrots for fiber
- Salmon oil for omega fatty acids
- Glucosamine and chondroitin for joint health
- Probiotics for digestive health
- No artificial colors, flavors, or preservatives
- No corn, wheat, or soy

Nutritional Highlights:
- Protein: 28%
- Fat: 16%
- Fiber: 4%
- Omega-6: 2.5%
- Omega-3: 0.5%

Suitable For:
- Adult dogs (1-7 years)
- All breeds and sizes
- Dogs with sensitive stomachs

Feeding Guidelines:
- Small dogs (10-20 lbs): 1-1.5 cups daily
- Medium dogs (20-50 lbs): 1.5-2.5 cups daily
- Large dogs (50-100 lbs): 2.5-4 cups daily

Package Size: 10kg (22 lbs)

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Jessica T. (Verified Purchase) - 5 stars
"My golden retriever has never been healthier! His coat is so shiny and he has so
much energy. He used to have digestive issues but since switching to this food,
no more problems. He absolutely loves the taste too!"

Review 2 - Mark W. (Verified Purchase) - 5 stars
"Finally found a dog food my picky eater loves! My french bulldog has allergies
and this food doesn't trigger them. The ingredient list is actually readable -
real food, not mystery fillers. Great quality."

Review 3 - Linda C. (Verified Purchase) - 4 stars
"Good quality dog food. My lab mix enjoys it and his stools are more consistent
now. A bit pricey but you get what you pay for. The bag could use a better reseal
mechanism though - had to transfer to a container."

Review 4 - Steve B. (Verified Purchase) - 5 stars
"Our vet recommended a higher quality food and this fit the bill. Two months in
and our 8-year-old border collie has more energy than ever. Her joints seem less
stiff too - probably the glucosamine. Highly recommend!"

Review 5 - Emily R. (Verified Purchase) - 4 stars
"Solid dog food with quality ingredients. My corgi loves it. Only giving 4 stars
because the kibble size is a bit large for smaller dogs - I have to break some
pieces for my small pup. Otherwise excellent product."

Average Rating: 4.5/5 (6,432 reviews)
----------------------------------------
""",

        "FOOD001": """
========================================
ORGANIC COFFEE BEANS 1KG - PRODUCT PAGE
========================================

Product: Organic Coffee Beans 1kg
Brand: Mountain Peak Roasters
Price: $24.99
SKU: FOOD001
Category: Food & Grocery

PRODUCT DESCRIPTION:
Start your morning with the rich, smooth taste of Mountain Peak Organic Coffee
Beans. Sourced from high-altitude farms in Colombia and Ethiopia, our beans are
100% organic, fair trade certified, and roasted in small batches to ensure
maximum freshness and flavor.

Coffee Profile:
- Roast Level: Medium
- Flavor Notes: Dark chocolate, caramel, hints of citrus
- Body: Full
- Acidity: Medium-bright
- Aroma: Rich and inviting

Sourcing:
- 50% Colombian Arabica (Huila region)
- 50% Ethiopian Arabica (Yirgacheffe)
- Altitude: 1,500-2,000 meters
- Harvest: Current season

Certifications:
- USDA Organic
- Fair Trade Certified
- Rainforest Alliance
- Non-GMO Project Verified

Package Details:
- Weight: 1kg (2.2 lbs) whole beans
- Packaging: Resealable bag with one-way valve
- Roasted: Within 2 weeks of shipping
- Best by: 6 months from roast date

Brewing Recommendations:
- Grind fresh before brewing for best results
- Water temperature: 195-205°F
- Ratio: 1:16 (coffee to water)
- Works great with all brewing methods

CUSTOMER REVIEWS:
----------------------------------------

Review 1 - Coffee Lover (Verified Purchase) - 5 stars
"This is the best coffee I've had outside of a specialty cafe! The chocolate notes
are prominent and the finish is so smooth. No bitterness at all. I've subscribed
for monthly delivery - that's how much I love it."

Review 2 - Nancy G. (Verified Purchase) - 5 stars
"My husband is very picky about coffee and he approves! Great for French press and
pour-over. The beans are fresh and aromatic. Love that it's organic and fair trade.
Feels good to enjoy quality coffee ethically."

Review 3 - Tom R. (Verified Purchase) - 4 stars
"Really good coffee, fresh roast, nice flavor profile. I prefer a darker roast
personally but this medium roast is excellent for what it is. The citrus notes
are subtle and pleasant. Will order again."

Review 4 - Maria P. (Verified Purchase) - 5 stars
"Makes the perfect espresso! The crema is beautiful and the taste is balanced.
I've tried many organic coffees and this is by far the best. The resealable bag
keeps it fresh. Highly recommend for espresso lovers!"

Review 5 - Jake H. (Verified Purchase) - 4 stars
"Solid everyday coffee. Fresh, flavorful, and smooth. My only minor gripe is I
wish they offered a dark roast option. But for medium roast fans, this is
excellent. Fast shipping too - arrived within 3 days."

Average Rating: 4.6/5 (4,123 reviews)
----------------------------------------
""",
    }

    for product_id, content in product_content.items():
        output_path = output_dir / f"{product_id}_product_page.txt"
        with open(output_path, "w") as f:
            f.write(content.strip())
        print(f"Generated product page: {output_path}")


def main() -> None:
    """Main function to generate all data."""
    base_dir = Path(__file__).parent.parent / "data"

    # Generate CSV
    csv_path = base_dir / "structured" / "daily_sales.csv"
    _generate_sales_csv(csv_path, num_rows=1000)

    # Generate product pages
    unstructured_dir = base_dir / "unstructured"
    _generate_product_pages(unstructured_dir)

    print("\nData generation complete!")
    print(f"CSV file: {csv_path}")
    print(f"Product pages: {unstructured_dir}")


if __name__ == "__main__":
    main()
