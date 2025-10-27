#!/usr/bin/env python3
"""
Utility to remove emojis from text
"""

import re

def remove_emojis(text):
    """Remove all emojis from text"""
    if not text:
        return text

    # Remove emojis using regex pattern
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FAFF"  # chess symbols
        "]+",
        flags=re.UNICODE
    )

    # Also remove common text emojis
    text_emojis = ['✅', '❌', '🎯', '📊', '🔥', '💡', '⚡', '🚀', '✨', '📝', '🎉', '🎬', '📡', '📋', '📈', '🔗', '🎨', '🗑️', '⏳', '⚠️']

    text = emoji_pattern.sub('', text)

    for emoji in text_emojis:
        text = text.replace(emoji, '')

    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text
