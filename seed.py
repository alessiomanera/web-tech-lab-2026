"""
seed.py
-------
Database seeding script.
Drops all existing tables and populates the SQLite database with
the Top 12 Curated Italian Cultural Experiences, museums, exhibitions,
and sample user profiles. Uses raw sqlite3 with parameterized queries.
"""
import json
import os
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash

# We need a Flask app context to use database.get_db()
from app import create_app
from database import get_db


def seed_db():
    """
    Initializes the database schema and loads 12 rich Italian cultural experiences
    with durations, transparent base pricing, included perks, and customizable add-ons.
    """
    app = create_app()
    with app.app_context():
        db = get_db()

        print("Wiping existing database and recreating schema...")
        # Drop tables in correct order (children first)
        db.executescript("""
            DROP TABLE IF EXISTS tickets;
            DROP TABLE IF EXISTS exhibitions;
            DROP TABLE IF EXISTS experiences;
            DROP TABLE IF EXISTS museums;
            DROP TABLE IF EXISTS users;
        """)

        # Re-create tables from schema.sql
        schema_path = os.path.join(app.root_path, 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            db.executescript(f.read())

        # ---------------------------------------------------------
        # 1. Create Core Italian Museums & Cultural Sites
        # ---------------------------------------------------------
        museums_data = [
            ("Galleria degli Uffizi",
             "The world's foremost repository of Renaissance masterworks, showcasing Botticelli, Leonardo da Vinci, Michelangelo, and Caravaggio.",
             "Piazzale degli Uffizi 6, 50122 Florence", "Florence",
             "/static/images/museums/museum-01-uffizi.jpg"),
            ("Parco Archeologico del Colosseo",
             "The monumental epicenter of the Roman Empire, encompassing the Flavian Amphitheater, the Roman Forum, and Palatine Hill.",
             "Piazza del Colosseo 1, 00184 Rome", "Rome",
             "/static/images/museums/museum-02-colosseum.jpg"),
            ("Palazzo Ducale di Venezia",
             "The majestic Gothic seat of the Serenissima Republic, featuring the Doge's private apartments, Grand Council chamber, and the Bridge of Sighs.",
             "Piazza San Marco 1, 30124 Venice", "Venice",
             "/static/images/museums/museum-03-doges-palace.jpg"),
            ("Museo Egizio di Torino",
             "The oldest Egyptian museum in the world and second in importance only to Cairo, housing over 40,000 priceless antiquities.",
             "Via Accademia delle Scienze 6, 10123 Turin", "Turin",
             "/static/images/museums/museum-04-museo-egizio.jpg"),
            ("Cenacolo Vinciano",
             "The sacred refectory of Santa Maria delle Grazie hosting Leonardo da Vinci's immortal masterpiece, The Last Supper.",
             "Piazza di Santa Maria delle Grazie 2, 20123 Milan", "Milan",
             "/static/images/museums/museum-05-cenacolo.jpg"),
            ("Parco Archeologico di Pompei",
             "An astonishing ancient Roman city frozen in time by the 79 AD eruption of Mount Vesuvius, featuring intact villas, frescoes, and streets.",
             "Via Plinio 26, 80045 Pompeii (Naples)", "Naples",
             "/static/images/museums/museum-06-pompeii.jpg"),
            ("Galleria Borghese",
             "A magnificent villa set in Roman parklands, showcasing Bernini's sensational marble sculptures and key canvases by Caravaggio, Titian, and Raphael.",
             "Piazzale Scipione Borghese 5, 00197 Rome", "Rome",
             "/static/images/museums/museum-07-borghese.jpg"),
            ("Galleria dell'Accademia",
             "The legendary sanctuary of Florentine Renaissance sculpture, home to Michelangelo's original colossal David and unfinished Slaves.",
             "Via Ricasoli 58/60, 50122 Florence", "Florence",
             "/static/images/museums/museum-08-accademia.jpg"),
            ("Collezione Peggy Guggenheim",
             "Venice's premier museum for 20th-century European and American avant-garde art, housed in Peggy Guggenheim's historic Grand Canal palace.",
             "Dorsoduro 701, 30123 Venice", "Venice",
             "/static/images/museums/museum-09-guggenheim.jpg"),
            ("Pinacoteca di Brera",
             "Milan's landmark public gallery of classical art, boasting masterpieces by Caravaggio, Hayez, Mantegna, and Raphael.",
             "Via Brera 28, 20121 Milan", "Milan",
             "/static/images/museums/museum-10-brera.jpg"),
        ]

        db.executemany(
            "INSERT INTO museums (name, description, location, city, image_url) VALUES (?, ?, ?, ?, ?)",
            museums_data
        )
        db.commit()
        print(f"Added {len(museums_data)} baseline museums.")

        # ---------------------------------------------------------
        # 2. Populate the Top 12 Curated Italian Experiences
        # ---------------------------------------------------------
        standard_addons = json.dumps([
            {"id": "audio", "name": "Spatial Audio Guide (Smartphone App)", "price": 5.0},
            {"id": "docent", "name": "Small-Group Art Historian Docent (60 min)", "price": 18.0},
            {"id": "catalog", "name": "Official High-Resolution Exhibition Book", "price": 15.0},
            {"id": "priority", "name": "VIP Instant Fast-Track Entrance", "price": 7.0}
        ])

        # Each tuple: (museum_id, title, tagline, city, theme, duration_minutes,
        #               base_price, badge, is_featured, included_items_json,
        #               available_addons_json, description, highlights, image_url)
        experiences_data = [
            # 1. Florence - Uffizi
            (1, "Renaissance Masterpieces & Botticelli Immersion",
             "Fast-track access to the Birth of Venus, Primavera, and Leonardo's Annunciation with a curated highlights route.",
             "Florence", "Renaissance Art", 120, 26.0, "Best Seller", 1,
             json.dumps(["Skip-the-line Admission to Galleria degli Uffizi",
                         "Dedicated Reserved Time-Slot Entry",
                         "Digital High-Resolution Curated Route Map",
                         "Access to all temporary exhibitions in the gallery"]),
             standard_addons,
             "Experience the pinnacle of Florentine Renaissance art without the friction of endless queues. This curated package guides you chronologically through Giotto, Botticelli's iconic halls, Leonardo da Vinci's early genius, Raphael, and Caravaggio's dramatic chiaroscuro.",
             "Botticelli's Birth of Venus, Caravaggio's Medusa, Leonardo's Adoration of the Magi, Arno River panorama from the upper corridor.",
             "/static/images/experiences/exp-01-florence-uffizi.jpg"),
            # 2. Rome - Colosseum
            (2, "Imperial Colosseum, Forum & Gladiators Underground",
             "Comprehensive archaeological journey exploring the arena floor, Roman Forum temples, and Palatine Hill emperors' palaces.",
             "Rome", "Ancient Archaeology", 180, 32.0, "Top Rated", 1,
             json.dumps(["Colosseum Arena Floor & Tier Access",
                         "Roman Forum & Palatine Hill Combined Entry",
                         "Full Day Imperial Passport",
                         "Interactive 3D Reconstruction App"]),
             standard_addons,
             "Walk the footsteps of gladiators and Roman emperors. This all-inclusive archaeological pass grants access to the restricted arena floor, the monumental triumphal arches, and the legendary Senate House in the Roman Forum.",
             "Gladiator Arena Gate, Curia Julia (Roman Senate), Arch of Constantine, Palatine Panoramic View.",
             "/static/images/experiences/exp-02-rome-colosseum.jpg"),
            # 3. Venice - Doge's Palace
            (3, "Secret Itineraries of the Doges & Bridge of Sighs",
             "Explore the hidden torture chambers, Casanova's prison cell, and the dazzling Golden Staircase of the Venetian Republic.",
             "Venice", "Venetian Secrets", 120, 30.0, "Exclusive Access", 1,
             json.dumps(["Full Palazzo Ducale Admission & Bridge of Sighs Crossing",
                         "Access to Museo Correr & Biblioteca Marciana",
                         "Exclusive Secret Itineraries Path",
                         "Digital Venice Lagoon Historical Guide"]),
             standard_addons,
             "Unravel the political intrigue and maritime dominance of Venice. Cross the Bridge of Sighs into the New Prisons, marvel at Tintoretto's colossal Paradise in the Grand Council Chamber, and admire the gilded Renaissance ceilings.",
             "Tintoretto's Il Paradiso, Bridge of Sighs crossing, Piombi Inquisitors' cells, Golden Staircase.",
             "/static/images/experiences/exp-03-venice-doges-palace.jpg"),
            # 4. Turin - Museo Egizio
            (4, "Pharaohs, Mummies & Golden Papyrus Quest",
             "Discover the tomb of Kha, the monumental Sphinx gallery, and three millennia of ancient Nile civilization.",
             "Turin", "Egyptian Antiquities", 120, 20.0, "Family Favorite", 1,
             json.dumps(["Full Access to all 4 Floors of Museo Egizio",
                         "Statuary Gallery by Dante Ferretti",
                         "Tomb of Kha & Merit Intact Artifacts",
                         "Interactive Family Nile Explorer Booklet"]),
             standard_addons,
             "Immerse yourself in the world's most evocative collection of Egyptian antiquities outside Cairo. Walk through mirror-lined statuary halls illuminated like sacred temples, decipher ancient papyrus scrolls, and inspect intact burial chambers.",
             "Colossal Statue of Ramesses II, Intact Tomb of Kha and Merit, Book of the Dead Papyrus, Statuary Gallery.",
             "/static/images/experiences/exp-04-turin-museo-egizio.jpg"),
            # 5. Milan - Last Supper
            (5, "Leonardo's Last Supper & Renaissance Genius",
             "Rare, climate-controlled intimate viewing of Da Vinci's world-altering fresco in the Dominican refectory.",
             "Milan", "Renaissance Art", 60, 35.0, "Ultra Rare Slot", 0,
             json.dumps(["Guaranteed 15-minute Direct Cenacolo Viewing Window",
                         "Entry to Santa Maria delle Grazie Basilica",
                         "Digital Leonardo Geometry & Color Analysis Dossier",
                         "Quiet Audio Listening Device"]),
             standard_addons,
             "A once-in-a-lifetime encounter with Leonardo da Vinci's masterpiece. Limited to strictly small batches of visitors, this experience lets you examine the emotional turbulence of Christ's apostles and Leonardo's groundbreaking linear perspective.",
             "Leonardo da Vinci's Il Cenacolo (1495-1498), Donato Montorfano's Crucifixion fresco, Bramante Cloister.",
             "/static/images/experiences/exp-05-milan-last-supper.jpg"),
            # 6. Naples - Pompeii
            (6, "Pompeii Villa Frescoes & Lost Roman Civilization",
             "Step into ancient Roman homes, amphitheaters, and thermal baths perfectly preserved beneath volcanic ash.",
             "Naples", "Ancient Archaeology", 180, 22.0, "UNESCO Heritage", 0,
             json.dumps(["Full Day Pompeii Archaeological Park Entry",
                         "Access to Villa of the Mysteries Frescoes",
                         "Thermopolium & Forum Access",
                         "Offline GPS Archaeological Walking Map"]),
             standard_addons,
             "Explore the world's most poignant archaeological site. Witness brilliant cinnabar red frescoes in the Villa of Mysteries, inspect intact Roman bakeries and fast-food bars (Thermopolia), and gaze at Mount Vesuvius looming on the horizon.",
             "Villa dei Misteri Dionysian frieze, House of the Faun, Roman Amphitheater, plaster casts of victims.",
             "/static/images/experiences/exp-06-naples-pompeii.jpg"),
            # 7. Rome - Galleria Borghese
            (7, "Galleria Borghese & Caravaggio in Private",
             "Strictly capacity-controlled villa experience surrounded by Bernini's Apollo and Daphne and master canvases by Titian.",
             "Rome", "High Baroque", 120, 28.0, "Curated Gem", 0,
             json.dumps(["Timed 2-Hour Exclusive Villa Admission",
                         "Access to 20 Sculpted & Painted Halls",
                         "Full Borghese Park Botanical Route",
                         "Bernini Marble Sculpture Analysis Guide"]),
             standard_addons,
             "Widely regarded as the world's most intimate high-end museum experience. Marvel at Bernini turning cold marble into soft skin and sprouting leaves in Apollo and Daphne, and inspect six foundational masterworks by Caravaggio.",
             "Bernini's Apollo and Daphne, Pluto and Persephone, Caravaggio's Boy with a Basket of Fruit, Canova's Paolina Borghese.",
             "/static/images/experiences/exp-07-rome-galleria-borghese.jpg"),
            # 8. Florence - Accademia
            (8, "Michelangelo's David & The Anatomy of Marble",
             "Gaze upon the supreme icon of male beauty, Michelangelo's colossal David, and the dramatic unfinished Slaves.",
             "Florence", "Renaissance Art", 90, 22.0, "Essential Icon", 0,
             json.dumps(["Priority Skip-the-Line Admission to Galleria dell'Accademia",
                         "Tribune of David Direct Access",
                         "Hall of Prisoners (Prigioni) Sculptures",
                         "Museum of Historical Musical Instruments Entry"]),
             standard_addons,
             "Witness the statue that defined the Renaissance. Stand beneath the 17-foot David, carved from a single flawed block of Carrara marble, and observe the unfinished 'Slaves' struggling to free themselves from stone.",
             "Michelangelo's David (1504), The Prisoners / Slaves series, Stradivari 1690 Medici cello, Giambologna plaster cast.",
             "/static/images/experiences/exp-08-florence-accademia.jpg"),
            # 9. Venice - Peggy Guggenheim
            (9, "Peggy Guggenheim Avant-Garde & Canal Sculptures",
             "Explore surrealism, cubism, and abstract expressionism inside an eccentric 18th-century palace on Venice's Grand Canal.",
             "Venice", "Contemporary Avant-Garde", 90, 20.0, "Modern Vision", 0,
             json.dumps(["Full Collection & Sculpture Garden Admission",
                         "Grand Canal Panoramic Balcony Access",
                         "Hannelore B. Schulhof Collection",
                         "Curated 20th Century Movements Guide"]),
             standard_addons,
             "The ultimate antidote to Venice's ancient architecture. Wander through light-filled rooms containing Pollock drip paintings, Picasso cubist studies, Magritte surrealist skies, and Marino Marini sculptures overlooking gondolas on the Grand Canal.",
             "Magritte's Empire of Light, Pollock's Alchemy, Ernst, Kandinsky, and Peggy Guggenheim's garden tomb.",
             "/static/images/experiences/exp-09-venice-peggy-guggenheim.jpg"),
            # 10. Milan - Pinacoteca di Brera
            (10, "Pinacoteca di Brera & Masterpieces of Italian Painting",
             "Stroll through Milan's artistic soul in the bohemian Brera district, witnessing Hayez's The Kiss and Mantegna's Dead Christ.",
             "Milan", "Classical Masterpieces", 120, 18.0, "Romantic Classic", 0,
             json.dumps(["Full Day Brera Gallery Admission",
                         "Access to Botanical Garden of Brera",
                         "Transparent Restoration Lab Viewing",
                         "Brera Masterpiece Route Brochure"]),
             standard_addons,
             "Nestled in Milan's most romantic neighborhood, the Brera Pinacoteca displays northern Italy's greatest triumphs in perspective, chiaroscuro, and emotional drama, from Renaissance altarpieces to 19th-century Romanticism.",
             "Francesco Hayez's The Kiss, Andrea Mantegna's Dead Christ, Raphael's Marriage of the Virgin, Caravaggio's Supper at Emmaus.",
             "/static/images/experiences/exp-10-milan-pinacoteca-brera.jpg"),
            # 11. Rome - Vatican Museums
            (2, "Vatican Museums, Raphael Rooms & Sistine Chapel",
             "Journey across 7 kilometers of papal galleries culminating in Michelangelo's breathtaking Sistine Chapel ceiling.",
             "Rome", "High Renaissance & Papal Splendor", 180, 35.0, "World Phenomenon", 0,
             json.dumps(["Skip-the-Line Vatican Galleries Admission",
                         "Raphael Rooms (School of Athens)",
                         "Sistine Chapel Viewing",
                         "Gallery of Maps & Tapestries Corridor"]),
             standard_addons,
             "The summit of Western religious art. Gaze up at Michelangelo's Creation of Adam and The Last Judgment in the Sistine Chapel, explore Raphael's philosophical School of Athens, and marvel at the golden Cartographic corridors.",
             "Sistine Chapel ceiling, Raphael's School of Athens, Laocoön and His Sons, Bramante spiral staircase.",
             "/static/images/experiences/exp-11-rome-vatican-sistine.jpg"),
            # 12. Naples - MANN
            (6, "National Archaeological Museum & The Farnese Marbles",
             "Encounter the monumental Farnese Hercules, Alexander Mosaic from Pompeii, and secret Roman erotic artifacts.",
             "Naples", "Ancient Archaeology", 120, 20.0, "Antiquity Epic", 0,
             json.dumps(["Full MANN Museum Entry",
                         "Farnese Classical Sculpture Collection",
                         "Pompeian Mosaics & Frescoes Hall",
                         "Secret Cabinet (Gabinetto Segreto) Access"]),
             standard_addons,
             "One of the world's most important classical antiquity museums, housing the colossal marbles discovered in the Baths of Caracalla and the delicate mosaics rescued from the ruins of Pompeii and Herculaneum.",
             "Alexander Mosaic from House of the Faun, Farnese Bull colossal marble, Farnese Hercules, Roman bronze statues.",
             "/static/images/experiences/exp-12-naples-mann.jpg"),
        ]

        db.executemany(
            """INSERT INTO experiences
               (museum_id, title, tagline, city, theme, duration_minutes,
                base_price, badge, is_featured, included_items_json,
                available_addons_json, description, highlights, image_url)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            experiences_data
        )
        db.commit()
        print(f"Added all {len(experiences_data)} curated Italian cultural experiences!")

        # ---------------------------------------------------------
        # 3. Create Sample Exhibitions & Seed User
        # ---------------------------------------------------------
        now = datetime.now(timezone.utc)
        exhibitions_data = [
            (1, "Botticelli: Line, Gold, and Melancholy",
             "A temporary monographic exhibition bringing together rare drawings and sacred panels from international collections.",
             (now - timedelta(days=15)).isoformat(),
             (now + timedelta(days=75)).isoformat()),
            (2, "Gladiators: Heroes of the Colosseum",
             "Archaeological armor, weapons, and interactive digital reconstructions of gladiatorial combats.",
             (now - timedelta(days=5)).isoformat(),
             (now + timedelta(days=120)).isoformat()),
        ]

        db.executemany(
            """INSERT INTO exhibitions (museum_id, title, description, start_date, end_date)
               VALUES (?, ?, ?, ?, ?)""",
            exhibitions_data
        )

        # Sample Demo User with an initial Markdown Taste Profile
        demo_prefs = """### Cultural Taste Profile
- **Primary Interests:** Renaissance Art, Roman Archaeology, Sculpture
- **Visit Pacing:** Moderate (1.5 – 2 hours per site)
- **Group Style:** Traveling solo or with a partner
- **Preferred Perks:** Audio guides, skip-the-line priority access
- **Favorite Cities:** Florence, Rome, Venice"""

        db.execute(
            "INSERT INTO users (name, email, password_hash, preferences) VALUES (?, ?, ?, ?)",
            ("Alessio Manera", "alessio@example.com",
             generate_password_hash("password123"), demo_prefs)
        )

        db.commit()
        print("Database successfully seeded with Top 12 Experiences and demo user!")


if __name__ == '__main__':
    seed_db()
