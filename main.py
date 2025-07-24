"""
BookBot - Text Analysis Tool
Main entry point for the program
"""

import sys
from stats import count_words, count_characters, get_sorted_character_report


def get_book_text(path):
    """
    Read and return the contents of a text file.
    
    Args:
        path (str): Path to the text file
        
    Returns:
        str: Contents of the file
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    """
    Main function that orchestrates the book analysis.
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <book_path>")
        sys.exit(1)

    book_path = sys.argv[1]
    
    text = get_book_text(book_path)
    
    word_count = count_words(text)
    char_count = count_characters(text)
    char_report = get_sorted_character_report(char_count)

    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {book_path}...")
    print("----------- Word Count ----------")
    print(f"Found {word_count} total words")
    print("--------- Character Count ---------")
    for item in char_report:
        print(f"'{item['char']}': {item['num']}")
    print("============= END ===============")


if __name__ == "__main__":
    main()