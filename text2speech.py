#!/usr/bin/env python3
"""
Text-to-Speech CLI using Coqui XTTS-v2
Converts text input to MP3 audio files.
"""

import click
import torch
from pathlib import Path
from TTS.api import TTS


@click.command()
@click.argument('text', type=str, required=False)
@click.option(
    '-f', '--file',
    type=click.Path(exists=True),
    default=None,
    help='Read text from a file instead of command line argument'
)
@click.option(
    '-o', '--output',
    type=click.Path(),
    default='output.mp3',
    help='Output MP3 file path (default: output.mp3)'
)
@click.option(
    '-s', '--speaker-wav',
    type=click.Path(exists=True),
    default=None,
    help='Path to a reference speaker audio file for voice cloning (optional)'
)
@click.option(
    '-l', '--language',
    type=click.Choice([
        'zh-cn',  # Chinese (Simplified)
        'en',     # English
        'es',     # Spanish
        'fr',     # French
        'de',     # German
        'it',     # Italian
        'pt',     # Portuguese
        'pl',     # Polish
        'tr',     # Turkish
        'ru',     # Russian
        'nl',     # Dutch
        'cs',     # Czech
        'ar',     # Arabic
        'ja',     # Japanese
        'hu',     # Hungarian
        'ko'      # Korean
    ]),
    default='zh-cn',
    help='Language code (default: zh-cn for Chinese)',
    show_default=True
)
@click.option(
    '--device',
    type=click.Choice(['auto', 'cpu', 'mps', 'cuda']),
    default='auto',
    help='Device to run the model on (default: auto)'
)
def main(text, file, output, speaker_wav, language, device):
    """
    Convert TEXT to MP3 audio file using Coqui XTTS-v2.

    Examples:

        text2speech "你好，世界！"

        text2speech "Hello, world!" -l en -o greeting.mp3

        text2speech -f input.txt -o output.mp3

        text2speech "你好！" -s reference_voice.wav
    """
    try:
        # Validate input
        if not text and not file:
            raise click.UsageError("Please provide text as an argument or use --file to read from a file")

        if text and file:
            raise click.UsageError("Please provide either text argument OR --file option, not both")

        # Read text from file if --file is provided
        if file:
            click.echo(f"Reading text from file: {file}")
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read().strip()

            if not text:
                raise click.UsageError("The input file is empty")

        # Show a preview of the text (truncated if too long)
        text_preview = text[:50] + '...' if len(text) > 50 else text
        click.echo(f"Text to convert: '{text_preview}'")
        # Determine the best device for Mac M3
        # Note: MPS has compatibility issues with current XTTS-v2 + transformers versions
        # Using CPU for stability
        if device == 'auto':
            device = 'cpu'
            click.echo("Using CPU (for compatibility with XTTS-v2)")
            if torch.backends.mps.is_available():
                click.echo("Note: MPS detected but using CPU due to current compatibility issues")
        elif device == 'mps':
            click.echo("Warning: MPS may have compatibility issues with XTTS-v2")
            click.echo("Consider using --device cpu if you encounter errors")

        click.echo(f"Initializing XTTS-v2 model on {device}...")

        # Initialize TTS with XTTS-v2 model
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        click.echo(f"Generating speech with language: {language}")

        # Convert output path to absolute path
        output_path = Path(output).resolve()

        # Generate speech
        if speaker_wav:
            click.echo(f"Using speaker reference: {speaker_wav}")
            tts.tts_to_file(
                text=text,
                file_path=str(output_path),
                speaker_wav=speaker_wav,
                language=language
            )
        else:
            # For XTTS-v2, use a consistent default reference audio
            click.echo("Using default voice (for consistent results, provide a reference with -s)")

            # Use the predefined default voice
            default_voice_path = Path(__file__).parent / "voices" / "11_0_audio_20250922_000846_0_intro.mp3"

            if not default_voice_path.exists():
                raise click.UsageError(f"Default voice file not found: {default_voice_path}")

            temp_wav_path = str(default_voice_path)

            # Try with current device first
            try:
                tts.tts_to_file(
                    text=text,
                    file_path=str(output_path),
                    speaker_wav=temp_wav_path,
                    language=language
                )
            except RuntimeError as e:
                # If MPS fails with attention mask error, fall back to CPU
                if "attention_mask" in str(e) and device == "mps":
                    click.echo("MPS compatibility issue detected, falling back to CPU...")
                    tts = tts.to("cpu")
                    tts.tts_to_file(
                        text=text,
                        file_path=str(output_path),
                        speaker_wav=temp_wav_path,
                        language=language
                    )
                else:
                    raise

        click.echo(f"✓ Audio saved to: {output_path}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
