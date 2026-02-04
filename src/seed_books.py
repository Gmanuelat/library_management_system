"""
Seed script to add 100 books to the library database.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Database
from author_manager import AuthorManager
from book_manager import BookManager

AUTHORS = [
    ("Jane Austen", 1775, "British"),
    ("Charles Dickens", 1812, "British"),
    ("Mark Twain", 1835, "American"),
    ("Leo Tolstoy", 1828, "Russian"),
    ("Fyodor Dostoevsky", 1821, "Russian"),
    ("Ernest Hemingway", 1899, "American"),
    ("Virginia Woolf", 1882, "British"),
    ("Gabriel Garcia Marquez", 1927, "Colombian"),
    ("Haruki Murakami", 1949, "Japanese"),
    ("Toni Morrison", 1931, "American"),
    ("George Orwell", 1903, "British"),
    ("Franz Kafka", 1883, "Czech"),
    ("J.R.R. Tolkien", 1892, "British"),
    ("Agatha Christie", 1890, "British"),
    ("Stephen King", 1947, "American"),
    ("Isaac Asimov", 1920, "American"),
    ("Ray Bradbury", 1920, "American"),
    ("Margaret Atwood", 1939, "Canadian"),
    ("Chinua Achebe", 1930, "Nigerian"),
    ("Jorge Luis Borges", 1899, "Argentine"),
]

# (title, isbn, year, genre, copies, author_index)
BOOKS = [
    ("Pride and Prejudice", "978-0141439518", 1813, "Romance", 3, 0),
    ("Sense and Sensibility", "978-0141439662", 1811, "Romance", 2, 0),
    ("Emma", "978-0141439587", 1815, "Romance", 2, 0),
    ("Mansfield Park", "978-0141439808", 1814, "Romance", 1, 0),
    ("Persuasion", "978-0141439686", 1817, "Romance", 2, 0),
    ("Northanger Abbey", "978-0141439792", 1817, "Gothic Parody", 2, 0),
    ("Oliver Twist", "978-0141439747", 1838, "Fiction", 3, 1),
    ("Great Expectations", "978-0141439563", 1861, "Fiction", 4, 1),
    ("A Tale of Two Cities", "978-0141439600", 1859, "Historical Fiction", 3, 1),
    ("David Copperfield", "978-0140439441", 1850, "Fiction", 2, 1),
    ("Bleak House", "978-0141439723", 1853, "Fiction", 1, 1),
    ("A Christmas Carol", "978-0141324524", 1843, "Novella", 4, 1),
    ("The Pickwick Papers", "978-0140436112", 1837, "Comedy", 1, 1),
    ("The Adventures of Tom Sawyer", "978-0143107330", 1876, "Adventure", 4, 2),
    ("Adventures of Huckleberry Finn", "978-0142437179", 1884, "Adventure", 5, 2),
    ("A Connecticut Yankee in King Arthur's Court", "978-0140430820", 1889, "Satire", 2, 2),
    ("The Prince and the Pauper", "978-0140436693", 1881, "Historical Fiction", 2, 2),
    ("Life on the Mississippi", "978-0140390506", 1883, "Travel", 1, 2),
    ("War and Peace", "978-0143039990", 1869, "Historical Fiction", 2, 3),
    ("Anna Karenina", "978-0143035008", 1877, "Romance", 3, 3),
    ("The Death of Ivan Ilyich", "978-0553210354", 1886, "Fiction", 2, 3),
    ("Resurrection", "978-0140444056", 1899, "Fiction", 1, 3),
    ("Hadji Murad", "978-1614272458", 1912, "Novella", 1, 3),
    ("Crime and Punishment", "978-0143058144", 1866, "Psychological Fiction", 4, 4),
    ("The Brothers Karamazov", "978-0374528379", 1880, "Philosophical Fiction", 3, 4),
    ("The Idiot", "978-0140447927", 1869, "Fiction", 2, 4),
    ("Notes from Underground", "978-0679734529", 1864, "Novella", 2, 4),
    ("Demons", "978-0140447514", 1872, "Political Fiction", 1, 4),
    ("The Gambler", "978-0140441161", 1867, "Novella", 2, 4),
    ("The Old Man and the Sea", "978-0684801223", 1952, "Fiction", 5, 5),
    ("A Farewell to Arms", "978-0684801469", 1929, "War Fiction", 3, 5),
    ("For Whom the Bell Tolls", "978-0684803357", 1940, "War Fiction", 2, 5),
    ("The Sun Also Rises", "978-0743297332", 1926, "Fiction", 3, 5),
    ("A Moveable Feast", "978-0684833637", 1964, "Memoir", 2, 5),
    ("Mrs Dalloway", "978-0156628709", 1925, "Modernist", 2, 6),
    ("To the Lighthouse", "978-0156907392", 1927, "Modernist", 2, 6),
    ("Orlando", "978-0156701600", 1928, "Fantasy", 1, 6),
    ("The Waves", "978-0156949606", 1931, "Experimental", 1, 6),
    ("A Room of One's Own", "978-0156787338", 1929, "Essay", 3, 6),
    ("One Hundred Years of Solitude", "978-0060883287", 1967, "Magical Realism", 5, 7),
    ("Love in the Time of Cholera", "978-0307389732", 1985, "Romance", 3, 7),
    ("Chronicle of a Death Foretold", "978-1400034710", 1981, "Mystery", 2, 7),
    ("The Autumn of the Patriarch", "978-0060919283", 1975, "Political Fiction", 1, 7),
    ("Norwegian Wood", "978-0375704024", 1987, "Romance", 4, 8),
    ("Kafka on the Shore", "978-1400079278", 2002, "Magical Realism", 3, 8),
    ("1Q84", "978-0307593313", 2009, "Science Fiction", 2, 8),
    ("The Wind-Up Bird Chronicle", "978-0679775430", 1994, "Surrealist", 2, 8),
    ("Colorless Tsukuru Tazaki", "978-0385352109", 2013, "Fiction", 3, 8),
    ("Beloved", "978-1400033416", 1987, "Historical Fiction", 4, 9),
    ("Song of Solomon", "978-1400033423", 1977, "Fiction", 3, 9),
    ("The Bluest Eye", "978-0307278449", 1970, "Fiction", 2, 9),
    ("Sula", "978-1400033430", 1973, "Fiction", 2, 9),
    ("1984", "978-0451524935", 1949, "Dystopian", 6, 10),
    ("Animal Farm", "978-0451526342", 1945, "Political Satire", 5, 10),
    ("Homage to Catalonia", "978-0156421171", 1938, "Memoir", 2, 10),
    ("Down and Out in Paris and London", "978-0156262248", 1933, "Memoir", 1, 10),
    ("The Metamorphosis", "978-0553213690", 1915, "Absurdist", 4, 11),
    ("The Trial", "978-0805209990", 1925, "Absurdist", 3, 11),
    ("The Castle", "978-0805211061", 1926, "Absurdist", 2, 11),
    ("Amerika", "978-0805210644", 1927, "Fiction", 1, 11),
    ("The Hobbit", "978-0547928227", 1937, "Fantasy", 6, 12),
    ("The Fellowship of the Ring", "978-0547928210", 1954, "Fantasy", 5, 12),
    ("The Two Towers", "978-0547928203", 1954, "Fantasy", 5, 12),
    ("The Return of the King", "978-0547928197", 1955, "Fantasy", 5, 12),
    ("The Silmarillion", "978-0544338012", 1977, "Fantasy", 2, 12),
    ("Murder on the Orient Express", "978-0062693662", 1934, "Mystery", 4, 13),
    ("And Then There Were None", "978-0062073471", 1939, "Mystery", 5, 13),
    ("The Murder of Roger Ackroyd", "978-0062073563", 1926, "Mystery", 3, 13),
    ("Death on the Nile", "978-0062073556", 1937, "Mystery", 3, 13),
    ("The ABC Murders", "978-0062073587", 1936, "Mystery", 2, 13),
    ("The Shining", "978-0307743657", 1977, "Horror", 4, 14),
    ("It", "978-1501142970", 1986, "Horror", 3, 14),
    ("Carrie", "978-0307743664", 1974, "Horror", 3, 14),
    ("The Stand", "978-0307743688", 1978, "Post-Apocalyptic", 2, 14),
    ("Misery", "978-1501143106", 1987, "Thriller", 3, 14),
    ("Pet Sematary", "978-1501156700", 1983, "Horror", 2, 14),
    ("Foundation", "978-0553293357", 1951, "Science Fiction", 4, 15),
    ("I, Robot", "978-0553382563", 1950, "Science Fiction", 3, 15),
    ("Foundation and Empire", "978-0553293371", 1952, "Science Fiction", 2, 15),
    ("Second Foundation", "978-0553293364", 1953, "Science Fiction", 2, 15),
    ("The Caves of Steel", "978-0553293401", 1954, "Science Fiction", 2, 15),
    ("Fahrenheit 451", "978-1451673319", 1953, "Dystopian", 5, 16),
    ("The Martian Chronicles", "978-1451678192", 1950, "Science Fiction", 3, 16),
    ("Something Wicked This Way Comes", "978-1501167713", 1962, "Dark Fantasy", 2, 16),
    ("Dandelion Wine", "978-0380977260", 1957, "Fiction", 2, 16),
    ("The Illustrated Man", "978-1451678185", 1951, "Science Fiction", 2, 16),
    ("The Handmaid's Tale", "978-0385490818", 1985, "Dystopian", 5, 17),
    ("Oryx and Crake", "978-0385721677", 2003, "Science Fiction", 2, 17),
    ("The Blind Assassin", "978-0385720953", 2000, "Fiction", 2, 17),
    ("Alias Grace", "978-0385490443", 1996, "Historical Fiction", 2, 17),
    ("The Testaments", "978-0385543781", 2019, "Dystopian", 3, 17),
    ("Things Fall Apart", "978-0385474542", 1958, "Fiction", 4, 18),
    ("No Longer at Ease", "978-0385474559", 1960, "Fiction", 2, 18),
    ("Arrow of God", "978-0385014809", 1964, "Fiction", 1, 18),
    ("A Man of the People", "978-0385086165", 1966, "Political Fiction", 1, 18),
    ("Ficciones", "978-0802130303", 1944, "Short Stories", 3, 19),
    ("The Aleph", "978-0142437889", 1949, "Short Stories", 2, 19),
    ("Labyrinths", "978-0811216999", 1962, "Short Stories", 2, 19),
    ("The Book of Sand", "978-0140059755", 1975, "Short Stories", 1, 19),
    ("Doctor Brodie's Report", "978-0140037951", 1970, "Short Stories", 1, 19),
]


def seed_database():
    db = Database()
    if not db.connect():
        print("Failed to connect to database!")
        return False

    db.create_tables()

    author_mgr = AuthorManager(db)
    book_mgr = BookManager(db)

    # Insert authors
    print("\n--- Adding Authors ---")
    author_ids = []
    for name, birth_year, nationality in AUTHORS:
        aid = author_mgr.add_author(name, birth_year, nationality)
        author_ids.append(aid)
    print(f"\nAdded {len(author_ids)} authors")

    # Insert 100 books
    print("\n--- Adding 100 Books ---")
    added = 0
    for title, isbn, year, genre, copies, author_idx in BOOKS:
        author_id = author_ids[author_idx] if author_idx < len(author_ids) else None
        if book_mgr.add_book(title, isbn, year, genre, copies, author_id):
            added += 1

    print(f"\nDone: {added} books added, {author_mgr.get_author_count()} authors, {book_mgr.get_book_count()} books total.")
    db.close()
    return True


if __name__ == "__main__":
    seed_database()
