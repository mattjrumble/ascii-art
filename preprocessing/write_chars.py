# Create a string of chars from char code 32 to 127,
# in 12 rows and 8 columns with a blank last entry.

# This should be screenshotted (e.g. chars.png)
# and used with analyze_chars.py.

output = ''

for i in range(32, 128):
    output += chr(i)
    if i % 8 == 0:
        output += '\n'
        
print(output)