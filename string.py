import re

def binary_to_ascii(binary_input):
    """ Converts a binary string to ASCII text """
    if isinstance(binary_input, bytes):
        binary_input = ''.join(f'{byte:08b}' for byte in binary_input)
    binary_input = binary_input.strip().replace(' ', '')  # sanitize
    chars = [chr(int(binary_input[i:i+8], 2)) for i in range(0, len(binary_input), 8)]
    return ''.join(chars)

def escape_path(path):
    """ Escapes special characters in a file path """
    return (
        path.replace(':', '-')
            .replace('\\', '/')
            .replace(' ', '%20')
            .replace('[', '%5B')
            .replace(']', '%5D')
            .replace('<', '%3C')
            .replace('>', '%3E')
    )

def process_and_inject(original_binary, inject_binary, inject_after=1):
    """
    Converts binary input to path, escapes it, splits it, injects a new binary segment,
    and returns the final reconstructed path.
    """
    # Convert both to ASCII
    original_ascii = binary_to_ascii(original_binary)
    inject_ascii = binary_to_ascii(inject_binary)

    # Escape and split
    escaped_original = escape_path(original_ascii)
    original_parts = re.split(r'[/\\\-_:.]', escaped_original)
    original_parts = [p for p in original_parts if p]

    # Inject new part
    if inject_after < 0 or inject_after > len(original_parts):
        inject_after = len(original_parts)
    new_parts = original_parts[:inject_after] + [inject_ascii] + original_parts[inject_after:]

    # Reconstruct
    reconstructed_path = '/'.join(new_parts)

    return {
        'original_ascii': original_ascii,
        'inject_ascii': inject_ascii,
        'original_parts': original_parts,
        'injected_parts': new_parts,
        'final_path': reconstructed_path
    }

# ==== Example ====

# Binary for: "src/utils/math.js"
original_binary = ''.join(format(ord(c), '08b') for c in "src/utils/math.js")

# Binary for: "injected"
inject_binary = ''.join(format(ord(c), '08b') for c in "injected")

result = process_and_inject(original_binary, inject_binary, inject_after=1)

print("== Results ==")
for k, v in result.items():
    print(f"{k}: {v}")
