"""
Create a string of chars from char code 32 to 127,
in 12 rows and 8 columns with a blank last entry.

This should be screenshotted (e.g. chars.png)
and used with analyze_chars.py.
"""

def insert_new_lines(input, interval):
    """Insert new lines into the given string at every 'interval' chars."""
    return '\n'.join(input[i:i+interval] for i in range(0, len(input), interval))


all_chars = ''.join([chr(i) for i in range(33, 128)])

print(insert_new_lines(all_chars, 8))
