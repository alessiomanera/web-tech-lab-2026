"""
seed.py
-------
Database seeding script.
Drops all existing tables and populates the SQLite database with 
the Top 20 Curated Italian Cultural Experiences, museums, exhibitions, and sample user profiles.
"""
import json
from datetime import datetime, timedelta
from app import create_app
from models import db, Museum, Exhibition, Experience, User
from werkzeug.security import generate_password_hash

def seed_db():
    """
    Initializes the database schema and loads 20 rich Italian cultural experiences
    with durations, transparent base pricing, included perks, and customizable add-ons.
    """
    app = create_app()
    with app.app_context():
        print("Wiping existing database and recreating schema...")
        db.drop_all()
        db.create_all()

        # ---------------------------------------------------------
        # 1. Create Core Italian Museums & Cultural Sites
        # ---------------------------------------------------------
        museums_data = [
            Museum(
                name="Galleria degli Uffizi",
                description="The world's foremost repository of Renaissance masterworks, showcasing Botticelli, Leonardo da Vinci, Michelangelo, and Caravaggio.",
                location="Piazzale degli Uffizi 6, 50122 Florence",
                city="Florence",
                image_url="https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Parco Archeologico del Colosseo",
                description="The monumental epicenter of the Roman Empire, encompassing the Flavian Amphitheater, the Roman Forum, and Palatine Hill.",
                location="Piazza del Colosseo 1, 00184 Rome",
                city="Rome",
                image_url="https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Palazzo Ducale di Venezia",
                description="The majestic Gothic seat of the Serenissima Republic, featuring the Doge's private apartments, Grand Council chamber, and the Bridge of Sighs.",
                location="Piazza San Marco 1, 30124 Venice",
                city="Venice",
                image_url="https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Museo Egizio di Torino",
                description="The oldest Egyptian museum in the world and second in importance only to Cairo, housing over 40,000 priceless antiquities.",
                location="Via Accademia delle Scienze 6, 10123 Turin",
                city="Turin",
                image_url="https://images.unsplash.com/photo-1599839575945-a9e5af0c3fa5?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Cenacolo Vinciano",
                description="The sacred refectory of Santa Maria delle Grazie hosting Leonardo da Vinci's immortal masterpiece, The Last Supper.",
                location="Piazza di Santa Maria delle Grazie 2, 20123 Milan",
                city="Milan",
                image_url="https://images.unsplash.com/photo-1513581166391-887a96ddeafd?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Parco Archeologico di Pompei",
                description="An astonishing ancient Roman city frozen in time by the 79 AD eruption of Mount Vesuvius, featuring intact villas, frescoes, and streets.",
                location="Via Plinio 26, 80045 Pompeii (Naples)",
                city="Naples",
                image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Galleria Borghese",
                description="A magnificent villa set in Roman parklands, showcasing Bernini's sensational marble sculptures and key canvases by Caravaggio, Titian, and Raphael.",
                location="Piazzale Scipione Borghese 5, 00197 Rome",
                city="Rome",
                image_url="https://images.unsplash.com/photo-1548126032-079a0fb0099d?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Galleria dell'Accademia",
                description="The legendary sanctuary of Florentine Renaissance sculpture, home to Michelangelo's original colossal David and unfinished Slaves.",
                location="Via Ricasoli 58/60, 50122 Florence",
                city="Florence",
                image_url="https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Collezione Peggy Guggenheim",
                description="Venice's premier museum for 20th-century European and American avant-garde art, housed in Peggy Guggenheim's historic Grand Canal palace.",
                location="Dorsoduro 701, 30123 Venice",
                city="Venice",
                image_url="https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=1200&q=80"
            ),
            Museum(
                name="Pinacoteca di Brera",
                description="Milan's landmark public gallery of classical art, boasting masterpieces by Caravaggio, Hayez, Mantegna, and Raphael.",
                location="Via Brera 28, 20121 Milan",
                city="Milan",
                image_url="https://images.unsplash.com/photo-1582555172866-f73bb12a2ab3?auto=format&fit=crop&w=1200&q=80"
            )
        ]

        db.session.add_all(museums_data)
        db.session.commit()
        print(f"Added {len(museums_data)} baseline museums.")

        # ---------------------------------------------------------
        # 2. Populate the Top 20 Curated Italian Experiences
        # ---------------------------------------------------------
        standard_addons = [
            {"id": "audio", "name": "Spatial Audio Guide (Smartphone App)", "price": 5.0},
            {"id": "docent", "name": "Small-Group Art Historian Docent (60 min)", "price": 18.0},
            {"id": "catalog", "name": "Official High-Resolution Exhibition Book", "price": 15.0},
            {"id": "priority", "name": "VIP Instant Fast-Track Entrance", "price": 7.0}
        ]

        experiences_data = [
            # 1. Florence - Uffizi
            Experience(
                museum_id=1,
                title="Renaissance Masterpieces & Botticelli Immersion",
                tagline="Fast-track access to the Birth of Venus, Primavera, and Leonardo's Annunciation with a curated highlights route.",
                city="Florence",
                theme="Renaissance Art",
                duration_minutes=120,
                base_price=26.0,
                badge="Best Seller",
                is_featured=True,
                included_items_json=json.dumps([
                    "Skip-the-line Admission to Galleria degli Uffizi",
                    "Dedicated Reserved Time-Slot Entry",
                    "Digital High-Resolution Curated Route Map",
                    "Access to all temporary exhibitions in the gallery"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Experience the pinnacle of Florentine Renaissance art without the friction of endless queues. This curated package guides you chronologically through Giotto, Botticelli's iconic halls, Leonardo da Vinci's early genius, Raphael, and Caravaggio's dramatic chiaroscuro.",
                highlights="Botticelli's Birth of Venus, Caravaggio's Medusa, Leonardo's Adoration of the Magi, Arno River panorama from the upper corridor.",
                image_url="https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=1200&q=80"
            ),
            # 2. Rome - Colosseum
            Experience(
                museum_id=2,
                title="Imperial Colosseum, Forum & Gladiators Underground",
                tagline="Comprehensive archaeological journey exploring the arena floor, Roman Forum temples, and Palatine Hill emperors' palaces.",
                city="Rome",
                theme="Ancient Archaeology",
                duration_minutes=180,
                base_price=32.0,
                badge="Top Rated",
                is_featured=True,
                included_items_json=json.dumps([
                    "Colosseum Arena Floor & Tier Access",
                    "Roman Forum & Palatine Hill Combined Entry",
                    "Full Day Imperial Passport",
                    "Interactive 3D Reconstruction App"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Walk the footsteps of gladiators and Roman emperors. This all-inclusive archaeological pass grants access to the restricted arena floor, the monumental triumphal arches, and the legendary Senate House in the Roman Forum.",
                highlights="Gladiator Arena Gate, Curia Julia (Roman Senate), Arch of Constantine, Palatine Panoramic View.",
                image_url="https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80"
            ),
            # 3. Venice - Doge's Palace
            Experience(
                museum_id=3,
                title="Secret Itineraries of the Doges & Bridge of Sighs",
                tagline="Explore the hidden torture chambers, Casanova's prison cell, and the dazzling Golden Staircase of the Venetian Republic.",
                city="Venice",
                theme="Venetian Secrets",
                duration_minutes=120,
                base_price=30.0,
                badge="Exclusive Access",
                is_featured=True,
                included_items_json=json.dumps([
                    "Full Palazzo Ducale Admission & Bridge of Sighs Crossing",
                    "Access to Museo Correr & Biblioteca Marciana",
                    "Exclusive Secret Itineraries Path",
                    "Digital Venice Lagoon Historical Guide"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Unravel the political intrigue and maritime dominance of Venice. Cross the Bridge of Sighs into the New Prisons, marvel at Tintoretto's colossal Paradise in the Grand Council Chamber, and admire the gilded Renaissance ceilings.",
                highlights="Tintoretto's Il Paradiso, Bridge of Sighs crossing, Piombi Inquisitors' cells, Golden Staircase.",
                image_url="https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=80"
            ),
            # 4. Turin - Museo Egizio
            Experience(
                museum_id=4,
                title="Pharaohs, Mummies & Golden Papyrus Quest",
                tagline="Discover the tomb of Kha, the monumental Sphinx gallery, and three millennia of ancient Nile civilization.",
                city="Turin",
                theme="Egyptian Antiquities",
                duration_minutes=120,
                base_price=20.0,
                badge="Family Favorite",
                is_featured=True,
                included_items_json=json.dumps([
                    "Full Access to all 4 Floors of Museo Egizio",
                    "Statuary Gallery by Dante Ferretti",
                    "Tomb of Kha & Merit Intact Artifacts",
                    "Interactive Family Nile Explorer Booklet"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Immerse yourself in the world's most evocative collection of Egyptian antiquities outside Cairo. Walk through mirror-lined statuary halls illuminated like sacred temples, decipher ancient papyrus scrolls, and inspect intact burial chambers.",
                highlights="Colossal Statue of Ramesses II, Intact Tomb of Kha and Merit, Book of the Dead Papyrus, Statuary Gallery.",
                image_url="https://images.unsplash.com/photo-1599839575945-a9e5af0c3fa5?auto=format&fit=crop&w=1200&q=80"
            ),
            # 5. Milan - Last Supper
            Experience(
                museum_id=5,
                title="Leonardo's Last Supper & Renaissance Genius",
                tagline="Rare, climate-controlled intimate viewing of Da Vinci's world-altering fresco in the Dominican refectory.",
                city="Milan",
                theme="Renaissance Art",
                duration_minutes=60,
                base_price=35.0,
                badge="Ultra Rare Slot",
                is_featured=False,
                included_items_json=json.dumps([
                    "Guaranteed 15-minute Direct Cenacolo Viewing Window",
                    "Entry to Santa Maria delle Grazie Basilica",
                    "Digital Leonardo Geometry & Color Analysis Dossier",
                    "Quiet Audio Listening Device"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="A once-in-a-lifetime encounter with Leonardo da Vinci's masterpiece. Limited to strictly small batches of visitors, this experience lets you examine the emotional turbulence of Christ's apostles and Leonardo's groundbreaking linear perspective.",
                highlights="Leonardo da Vinci's Il Cenacolo (1495-1498), Donato Montorfano's Crucifixion fresco, Bramante Cloister.",
                image_url="https://images.unsplash.com/photo-1513581166391-887a96ddeafd?auto=format&fit=crop&w=1200&q=80"
            ),
            # 6. Naples - Pompeii
            Experience(
                museum_id=6,
                title="Pompeii Villa Frescoes & Lost Roman Civilization",
                tagline="Step into ancient Roman homes, amphitheaters, and thermal baths perfectly preserved beneath volcanic ash.",
                city="Naples",
                theme="Ancient Archaeology",
                duration_minutes=180,
                base_price=22.0,
                badge="UNESCO Heritage",
                is_featured=False,
                included_items_json=json.dumps([
                    "Full Day Pompeii Archaeological Park Entry",
                    "Access to Villa of the Mysteries Frescoes",
                    "Thermopolium & Forum Access",
                    "Offline GPS Archaeological Walking Map"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Explore the world's most poignant archaeological site. Witness brilliant cinnabar red frescoes in the Villa of Mysteries, inspect intact Roman bakeries and fast-food bars (Thermopolia), and gaze at Mount Vesuvius looming on the horizon.",
                highlights="Villa dei Misteri Dionysian frieze, House of the Faun, Roman Amphitheater, plaster casts of victims.",
                image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80"
            ),
            # 7. Rome - Galleria Borghese
            Experience(
                museum_id=7,
                title="Galleria Borghese & Caravaggio in Private",
                tagline="Strictly capacity-controlled villa experience surrounded by Bernini's Apollo and Daphne and master canvases by Titian.",
                city="Rome",
                theme="High Baroque",
                duration_minutes=120,
                base_price=28.0,
                badge="Curated Gem",
                is_featured=False,
                included_items_json=json.dumps([
                    "Timed 2-Hour Exclusive Villa Admission",
                    "Access to 20 Sculpted & Painted Halls",
                    "Full Borghese Park Botanical Route",
                    "Bernini Marble Sculpture Analysis Guide"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Widely regarded as the world's most intimate high-end museum experience. Marvel at Bernini turning cold marble into soft skin and sprouting leaves in Apollo and Daphne, and inspect six foundational masterworks by Caravaggio.",
                highlights="Bernini's Apollo and Daphne, Pluto and Persephone, Caravaggio's Boy with a Basket of Fruit, Canova's Paolina Borghese.",
                image_url="https://images.unsplash.com/photo-1548126032-079a0fb0099d?auto=format&fit=crop&w=1200&q=80"
            ),
            # 8. Florence - Accademia
            Experience(
                museum_id=8,
                title="Michelangelo’s David & The Anatomy of Marble",
                tagline="Gaze upon the supreme icon of male beauty, Michelangelo's colossal David, and the dramatic unfinished Slaves.",
                city="Florence",
                theme="Renaissance Art",
                duration_minutes=90,
                base_price=22.0,
                badge="Essential Icon",
                is_featured=False,
                included_items_json=json.dumps([
                    "Priority Skip-the-Line Admission to Galleria dell'Accademia",
                    "Tribune of David Direct Access",
                    "Hall of Prisoners (Prigioni) Sculptures",
                    "Museum of Historical Musical Instruments Entry"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Witness the statue that defined the Renaissance. Stand beneath the 17-foot David, carved from a single flawed block of Carrara marble, and observe the unfinished 'Slaves' struggling to free themselves from stone.",
                highlights="Michelangelo's David (1504), The Prisoners / Slaves series, Stradivari 1690 Medici cello, Giambologna plaster cast.",
                image_url="https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80"
            ),
            # 9. Venice - Peggy Guggenheim
            Experience(
                museum_id=9,
                title="Peggy Guggenheim Avant-Garde & Canal Sculptures",
                tagline="Explore surrealism, cubism, and abstract expressionism inside an eccentric 18th-century palace on Venice's Grand Canal.",
                city="Venice",
                theme="Contemporary Avant-Garde",
                duration_minutes=90,
                base_price=20.0,
                badge="Modern Vision",
                is_featured=False,
                included_items_json=json.dumps([
                    "Full Collection & Sculpture Garden Admission",
                    "Grand Canal Panoramic Balcony Access",
                    "Hannelore B. Schulhof Collection",
                    "Curated 20th Century Movements Guide"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="The ultimate antidote to Venice's ancient architecture. Wander through light-filled rooms containing Pollock drip paintings, Picasso cubist studies, Magritte surrealist skies, and Marino Marini sculptures overlooking gondolas on the Grand Canal.",
                highlights="Magritte's Empire of Light, Pollock's Alchemy, Ernst, Kandinsky, and Peggy Guggenheim's garden tomb.",
                image_url="https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=1200&q=80"
            ),
            # 10. Milan - Pinacoteca di Brera
            Experience(
                museum_id=10,
                title="Pinacoteca di Brera & Masterpieces of Italian Painting",
                tagline="Stroll through Milan's artistic soul in the bohemian Brera district, witnessing Hayez's The Kiss and Mantegna's Dead Christ.",
                city="Milan",
                theme="Classical Masterpieces",
                duration_minutes=120,
                base_price=18.0,
                badge="Romantic Classic",
                is_featured=False,
                included_items_json=json.dumps([
                    "Full Day Brera Gallery Admission",
                    "Access to Botanical Garden of Brera",
                    "Transparent Restoration Lab Viewing",
                    "Brera Masterpiece Route Brochure"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Nestled in Milan's most romantic neighborhood, the Brera Pinacoteca displays northern Italy's greatest triumphs in perspective, chiaroscuro, and emotional drama, from Renaissance altarpieces to 19th-century Romanticism.",
                highlights="Francesco Hayez's The Kiss, Andrea Mantegna's Dead Christ, Raphael's Marriage of the Virgin, Caravaggio's Supper at Emmaus.",
                image_url="https://images.unsplash.com/photo-1582555172866-f73bb12a2ab3?auto=format&fit=crop&w=1200&q=80"
            ),
            # 11. Rome - Vatican Museums
            Experience(
                museum_id=2,
                title="Vatican Museums, Raphael Rooms & Sistine Chapel",
                tagline="Journey across 7 kilometers of papal galleries culminating in Michelangelo's breathtaking Sistine Chapel ceiling.",
                city="Rome",
                theme="High Renaissance & Papal Splendor",
                duration_minutes=180,
                base_price=35.0,
                badge="World Phenomenon",
                is_featured=False,
                included_items_json=json.dumps([
                    "Skip-the-Line Vatican Galleries Admission",
                    "Raphael Rooms (School of Athens)",
                    "Sistine Chapel Viewing",
                    "Gallery of Maps & Tapestries Corridor"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="The summit of Western religious art. Gaze up at Michelangelo's Creation of Adam and The Last Judgment in the Sistine Chapel, explore Raphael's philosophical School of Athens, and marvel at the golden Cartographic corridors.",
                highlights="Sistine Chapel ceiling, Raphael's School of Athens, Laocoön and His Sons, Bramante spiral staircase.",
                image_url="https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=1200&q=80"
            ),
            # 12. Naples - MANN
            Experience(
                museum_id=6,
                title="National Archaeological Museum & The Farnese Marbles",
                tagline="Encounter the monumental Farnese Hercules, Alexander Mosaic from Pompeii, and secret Roman erotic artifacts.",
                city="Naples",
                theme="Ancient Archaeology",
                duration_minutes=120,
                base_price=20.0,
                badge="Antiquity Epic",
                is_featured=False,
                included_items_json=json.dumps([
                    "Full MANN Museum Entry",
                    "Farnese Classical Sculpture Collection",
                    "Pompeian Mosaics & Frescoes Hall",
                    "Secret Cabinet (Gabinetto Segreto) Access"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="One of the world's most important classical antiquity museums, housing the colossal marbles discovered in the Baths of Caracalla and the delicate mosaics rescued from the ruins of Pompeii and Herculaneum.",
                highlights="Alexander Mosaic from House of the Faun, Farnese Bull colossal marble, Farnese Hercules, Roman bronze statues.",
                image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80"
            ),
            # 13. Verona - Arena
            Experience(
                museum_id=2,
                title="Roman Arena & Opera Legends Sunset Tour",
                tagline="Explore the 2,000-year-old pink marble Roman amphitheater that transforms into the world's most prestigious open-air opera stage.",
                city="Verona",
                theme="Roman Heritage & Opera",
                duration_minutes=90,
                base_price=16.0,
                badge="Open Air Wonder",
                is_featured=False,
                included_items_json=json.dumps([
                    "Priority Arena di Verona Entry",
                    "Climb to Upper Tier Panorama",
                    "Opera Set Design Exhibition",
                    "Verona Historic Center Audio Trail"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Older than the Colosseum in Rome, Verona's pristine Roman Arena offers breathtaking vistas across the Adige River and Piazza Bra, showcasing how ancient gladiatorial arenas evolve into temples of music.",
                highlights="Ancient Roman internal arches, Arena summit sunset view, Scenographic opera exhibits.",
                image_url="https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=80"
            ),
            # 14. Palermo - Palazzo dei Normanni
            Experience(
                museum_id=1,
                title="Norman Palace & Palatine Chapel Gold Mosaics",
                tagline="Witness the dazzling convergence of Byzantine, Arab, and Norman craftsmanship in Sicily's most glittering royal chapel.",
                city="Palermo",
                theme="Byzantine & Arab-Norman",
                duration_minutes=90,
                base_price=19.0,
                badge="Golden Mosaics",
                is_featured=False,
                included_items_json=json.dumps([
                    "Full Royal Palace & Cappella Palatina Entry",
                    "Royal Apartments of the Kings of Sicily",
                    "Subtropical Royal Gardens Access",
                    "Arab-Norman Architectural Symbol Guide"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="A breathtaking gem of multicultural medieval Europe. Marvel at ceiling-to-floor 24-karat gold mosaics depicting Christ Pantocrator, intricate Islamic muqarnas wooden ceilings, and centuries of Norman royal history.",
                highlights="Christ Pantocrator gold dome mosaic, Islamic carved wooden ceiling, Roger II royal bedroom, Romanesque arches.",
                image_url="https://images.unsplash.com/photo-1548126032-079a0fb0099d?auto=format&fit=crop&w=1200&q=80"
            ),
            # 15. Bologna - Archiginnasio
            Experience(
                museum_id=4,
                title="Medieval Towers, Anatomical Theater & University Lore",
                tagline="Explore Europe's oldest university, the wooden 17th-century Anatomical dissection theater, and 6,000 student heraldic coats of arms.",
                city="Bologna",
                theme="Medieval & Science History",
                duration_minutes=90,
                base_price=15.0,
                badge="Secret University",
                is_featured=False,
                included_items_json=json.dumps([
                    "Archiginnasio Palace & Anatomical Theater Entry",
                    "Stabat Mater Historic Lecture Hall",
                    "Bologna Porticoes Walking Guide",
                    "Heraldic Library Highlights"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Discover the birthplace of modern European higher learning. Step inside the fragrant cedar-wood Anatomical Theater where Galileo's contemporaries dissected human cadavers by candlelight beneath statues of ancient physicians.",
                highlights="Carved wooden Anatomical Theater (1637), Spellati statues, 6,000 student coats of arms, Stabat Mater hall.",
                image_url="https://images.unsplash.com/photo-1582555172866-f73bb12a2ab3?auto=format&fit=crop&w=1200&q=80"
            ),
            # 16. Turin - Musei Reali
            Experience(
                museum_id=4,
                title="Royal Palace of Savoy & The Armory of Kings",
                tagline="Step into royal opulence with glittering state rooms, one of the world's greatest equestrian armories, and Leonardo da Vinci's self-portrait.",
                city="Turin",
                theme="Royal Splendor & Armory",
                duration_minutes=150,
                base_price=22.0,
                badge="Royal Court",
                is_featured=False,
                included_items_json=json.dumps([
                    "Palazzo Reale State Apartments Access",
                    "Royal Armory (Armeria Reale)",
                    "Sabauda Picture Gallery",
                    "Royal Gardens of Andre Le Notre"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Turin was the first capital of unified Italy and the seat of the House of Savoy. Tour the Throne Room, mirror galleries, and the astounding Royal Armory featuring knightly armor forged by medieval armorers.",
                highlights="Armeria Reale knight equestrian gallery, Royal Throne Room, Holy Shroud Chapel architecture, Sabauda Gallery.",
                image_url="https://images.unsplash.com/photo-1599839575945-a9e5af0c3fa5?auto=format&fit=crop&w=1200&q=80"
            ),
            # 17. Florence - Bargello
            Experience(
                museum_id=1,
                title="Bargello Sculpture Treasury & Donatello’s Bronze",
                tagline="The fortress palace housing Donatello’s bronze David, Michelangelo’s early Bacchus, and Renaissance decorative arts.",
                city="Florence",
                theme="Renaissance Sculpture",
                duration_minutes=90,
                base_price=18.0,
                badge="Sculpture Haven",
                is_featured=False,
                included_items_json=json.dumps([
                    "Full Bargello National Museum Entry",
                    "Donatello & Verrocchio Sculptures Hall",
                    "Medici Ivory & Jewelry Collection",
                    "Medieval Courtyard & Prison Walk"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Often overshadowed by the Uffizi, the Bargello is the world's most intimate museum of Renaissance three-dimensional art. Set within a 13th-century fortress, it showcases the masterpieces that sparked the Florentine revolution.",
                highlights="Donatello's Bronze David (1440), Michelangelo's Bacchus, Giambologna's Flying Mercury, Brunelleschi vs Ghiberti competition panels.",
                image_url="https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=1200&q=80"
            ),
            # 18. Milan - Museo del Novecento
            Experience(
                museum_id=5,
                title="Futurism, Boccioni & 20th Century Pioneers",
                tagline="Witness the energetic revolution of Italian modernism with Fontana’s glowing neon and front-row Duomo terrace views.",
                city="Milan",
                theme="Modern & Contemporary",
                duration_minutes=90,
                base_price=15.0,
                badge="Duomo View",
                is_featured=False,
                included_items_json=json.dumps([
                    "Museo del Novecento Permanent Collection Entry",
                    "Lucio Fontana Spatial Neon Room",
                    "Futurism Gallery (Balla, Boccioni, Severini)",
                    "Duomo di Milano Panoramic Terrace Access"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Located right inside Piazza del Duomo, this dynamic museum traces Italy's 20th-century artistic vanguard: Futurism, Metaphysical painting, Spatialism, and Arte Povera, topped off by an unforgettable viewpoint facing the Duomo spires.",
                highlights="Umberto Boccioni's Unique Forms of Continuity in Space, Pellizza da Volpedo's Il Quarto Stato, Lucio Fontana neon ceiling.",
                image_url="https://images.unsplash.com/photo-1513581166391-887a96ddeafd?auto=format&fit=crop&w=1200&q=80"
            ),
            # 19. Venice - Museo Correr
            Experience(
                museum_id=3,
                title="Correr Museum & Napoleonic Royal Rooms",
                tagline="Discover the art, naval conquests, and daily life of Venetian Doges across Empress Sisi's neoclassical imperial apartments.",
                city="Venice",
                theme="Venetian History & Art",
                duration_minutes=100,
                base_price=25.0,
                badge="St. Mark's Square",
                is_featured=False,
                included_items_json=json.dumps([
                    "Museo Correr Full Entry",
                    "Imperial Apartments of Empress Elisabeth (Sisi)",
                    "Canova Marble Sculpture Gallery",
                    "Venetian Navigational Instruments & Coins Collection"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Commanding the western end of Piazza San Marco, the Correr Museum reveals Venice beyond the canals: its naval supremacy, Doge election ballots, coin mints, and stunning Canova statues inside neoclassical ballrooms.",
                highlights="Antonio Canova's Daedalus and Icarus, Empress Sisi's boudoir, Antonello da Messina's Pieta, Venetian globes.",
                image_url="https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=1200&q=80"
            ),
            # 20. Rome - Musei Capitolini
            Experience(
                museum_id=2,
                title="Capitoline Museums & The Foundations of Rome",
                tagline="Explore the world's oldest public museum atop the Capitoline Hill, home to the She-Wolf, Dying Gaul, and Marcus Aurelius bronze.",
                city="Rome",
                theme="Ancient Classical",
                duration_minutes=120,
                base_price=22.0,
                badge="Oldest Museum",
                is_featured=False,
                included_items_json=json.dumps([
                    "Full Capitoline Museums & Tabularium Entry",
                    "Overlook of the Roman Forum from Ancient Archives",
                    "Marcus Aurelius Original Gilded Equestrian Bronze",
                    "Lupa Capitolina Bronze Gallery"
                ]),
                available_addons_json=json.dumps(standard_addons),
                description="Founded in 1471 by Pope Sixtus IV, the Capitoline Museums sit on Michelangelo's famous piazza. Walk through underground tunnels connecting the palaces and gaze out over the entire Roman Forum from the ancient Tabularium.",
                highlights="Lupa Capitolina (Capitoline She-Wolf), The Dying Gaul, Colossus of Constantine marble fragments, Tabularium Forum View.",
                image_url="https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80"
            )
        ]

        db.session.add_all(experiences_data)
        db.session.commit()
        print(f"Added all {len(experiences_data)} curated Italian cultural experiences!")

        # ---------------------------------------------------------
        # 3. Create Sample Exhibitions & Seed User
        # ---------------------------------------------------------
        exh1 = Exhibition(
            museum_id=1,
            title="Botticelli: Line, Gold, and Melancholy",
            description="A temporary monographic exhibition bringing together rare drawings and sacred panels from international collections.",
            start_date=datetime.utcnow() - timedelta(days=15),
            end_date=datetime.utcnow() + timedelta(days=75)
        )
        exh2 = Exhibition(
            museum_id=2,
            title="Gladiators: Heroes of the Colosseum",
            description="Archaeological armor, weapons, and interactive digital reconstructions of gladiatorial combats.",
            start_date=datetime.utcnow() - timedelta(days=5),
            end_date=datetime.utcnow() + timedelta(days=120)
        )
        db.session.add_all([exh1, exh2])

        # Sample Demo User with an initial Markdown Taste Profile
        demo_user = User(
            name="Alessio Manera",
            email="alessio@example.com",
            password_hash=generate_password_hash("password123"),
            preferences="""### Cultural Taste Profile
- **Primary Interests:** Renaissance Art, Roman Archaeology, Sculpture
- **Visit Pacing:** Moderate (1.5 – 2 hours per site)
- **Group Style:** Traveling solo or with a partner
- **Preferred Perks:** Audio guides, skip-the-line priority access
- **Favorite Cities:** Florence, Rome, Venice"""
        )
        db.session.add(demo_user)
        db.session.commit()
        print("Database successfully seeded with Top 20 Experiences and demo user!")

if __name__ == '__main__':
    seed_db()
