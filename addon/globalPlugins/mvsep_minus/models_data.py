# -*- coding: utf-8 -*-
"""
MVSEP Models Metadata - Original International Model Names (No Translation).
Standard model names as defined by MVSEP and AI research teams.
"""

# Minus / Vocal Separation Models (Original Names)
MINUS_MODELS = [
    ("40", "BS Roformer (Vocal / Instrumental) ⭐ Best Quality"),
    ("48", "MelBand Roformer (Vocal / Instrumental)"),
    ("46", "SCNet (Vocal / Instrumental)"),
    ("25", "MDX23C (Vocal / Instrumental)"),
    ("27", "Demucs4 Vocals 2023 (Vocal / Instrumental)"),
    ("43", "Multichannel BS (Vocal / Instrumental)"),
    ("23", "MDX B (Vocal / Instrumental)"),
    ("9", "UVR VR (Vocal / Music)"),
    ("49", "Karaoke (Lead / Backing Vocals)"),
    ("12", "MDX-B Karaoke (Lead / Backing Vocals)"),
    ("22", "Reverb Removal (De-reverb)"),
    ("57", "Male / Female Voice Separation"),
]

# All MVSEP Models (Original International Names)
ALL_MODELS = [
    # Vocal & Instrumental Minus Models
    ("40", "BS Roformer (Vocal / Instrumental)"),
    ("48", "MelBand Roformer (Vocal / Instrumental)"),
    ("46", "SCNet (Vocal / Instrumental)"),
    ("25", "MDX23C (Vocal / Instrumental)"),
    ("27", "Demucs4 Vocals 2023 (Vocal / Instrumental)"),
    ("43", "Multichannel BS (Vocal / Instrumental)"),
    ("23", "MDX B (Vocal / Instrumental)"),
    ("9", "UVR VR (Vocal / Music)"),
    ("49", "Karaoke (Lead / Backing Vocals)"),
    ("12", "MDX-B Karaoke (Lead / Backing Vocals)"),
    ("22", "Reverb Removal (De-reverb)"),
    ("57", "Male / Female Voice Separation"),
    # Multi-stem & Instruments
    ("63", "BS Roformer SW (6 Stems: Vocal, Bass, Drums, Guitar, Piano, Other)"),
    ("20", "Demucs4 HT (4 Stems: Vocal, Drums, Bass, Other)"),
    ("44", "Drums (Drums / Music)"),
    ("41", "Bass (Bass / Music)"),
    ("31", "Guitar (Guitar / Music)"),
    ("29", "Piano (Piano / Music)"),
    ("88", "Synth (Synthesizer / Other)"),
    ("106", "Keys (Keys / Other)"),
    ("52", "Bowed Strings (Strings / Other)"),
    ("54", "Wind (Wind Instruments / Other)"),
    ("107", "Brass (Brass / Other)"),
    ("65", "Violin (Violin / Other)"),
    ("70", "Cello (Cello / Other)"),
    ("66", "Acoustic Guitar"),
    ("81", "Electric Guitar"),
    ("105", "Percussion (Percussion / Other)"),
    ("37", "DrumSep (Kick, Snare, Cymbals, Toms, Hi-Hat)"),
    # Enhancement & Voice Tools
    ("47", "DeNoise (Noise Reduction)"),
    ("34", "Crowd Removal (Crowd Noise Removal)"),
    ("51", "Apollo Enhancer (Audio Quality Enhancer)"),
    ("59", "AudioSR (Super Resolution)"),
    ("53", "Medley Vox (Multiple Singers Separation)"),
    ("111", "SATB Choir (Soprano, Alto, Tenor, Bass)"),
]

DEFAULT_FAVORITES = ["40", "48", "49", "25", "22"]


def get_minus_models_list():
    """Returns list of (id, original_name) for minus models."""
    return list(MINUS_MODELS)


def get_all_models_list():
    """Returns list of (id, original_name) for all models."""
    return list(ALL_MODELS)


def get_model_title(model_id):
    """Find title for a model ID."""
    for m_id, name in MINUS_MODELS:
        if str(m_id) == str(model_id):
            return name
    for m_id, name in ALL_MODELS:
        if str(m_id) == str(model_id):
            return name
    return f"Model {model_id}"
