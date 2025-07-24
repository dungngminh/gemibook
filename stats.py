import re

def count_words(text):
    """Counts the number of words in a given string."""
    words = text.split()
    return len(words)

def count_characters(text):
    """Counts the frequency of each character in a given string."""
    text = text.lower()
    chars = {}
    for char in text:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1
    return chars

def get_sorted_character_report(chars):
    """Converts a character dictionary to a sorted list of dictionaries."""
    char_list = []
    for char, count in chars.items():
        if char.isalpha():
            char_list.append({"char": char, "num": count})
    char_list.sort(key=lambda x: x["num"], reverse=True)
    return char_list

def count_word_frequency(text, num_words=10):
    """Counts the frequency of each word in a given string and returns the most common ones."""
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_words[:num_words]

def calculate_average_word_length(text):
    """Calculates the average word length in a given string."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)