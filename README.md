# Text-to-Speech CLI

A command-line application to convert text to MP3 using Coqui XTTS-v2, optimized for Mac M3.

## Features

- Convert text or text files to high-quality MP3 audio
- **Chinese (Simplified) as default language**
- Support for 16 languages with easy selection
- Voice cloning with reference audio
- Read from text files or command line
- Optimized for Mac M3 with Metal Performance Shaders (MPS)
- Built with `uv` for fast dependency management

## Prerequisites

- Mac M3 (or compatible Mac with Apple Silicon)
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

1. Clone or navigate to this directory
2. Run the setup script:

```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Verify PyTorch MPS support for Mac M3

## Usage

### Activate the environment

```bash
source .venv/bin/activate
```

### Basic usage

Convert Chinese text to MP3 (default language):

```bash
text2speech "你好，世界！"
```

### Read from text file

```bash
text2speech -f example.txt -o chinese_audio.mp3
```

### Custom output file

```bash
text2speech "你好，欢迎使用语音合成工具！" -o greeting.mp3
```

### Specify different language

```bash
# English
text2speech "Hello, world!" -l en -o english.mp3

# French
text2speech "Bonjour le monde!" -l fr -o french.mp3

# Japanese
text2speech "こんにちは、世界！" -l ja -o japanese.mp3
```

### Voice cloning

Use a reference audio file to clone a voice:

```bash
text2speech "你好，这是我的声音克隆！" -s reference_speaker.wav -o cloned.mp3
```

### Using with uv (without activation)

```bash
uv run text2speech "你好！"
```

## Command Options

```
Usage: text2speech [OPTIONS] [TEXT]

Arguments:
  TEXT                        Text to convert to speech (optional if using --file)

Options:
  -f, --file PATH             Read text from a file instead of command line
  -o, --output PATH           Output MP3 file path (default: output.mp3)
  -s, --speaker-wav PATH      Reference speaker audio file for voice cloning
  -l, --language [zh-cn|en|es|fr|de|it|pt|pl|tr|ru|nl|cs|ar|ja|hu|ko]
                              Language code (default: zh-cn)
  --device [auto|cpu|mps|cuda]
                              Device to run the model (default: auto)
  --help                      Show this message and exit
```

You must provide either TEXT argument or --file option (not both).

## Supported Languages

XTTS-v2 supports 16 languages (use `-l` flag):

- **Chinese Simplified (zh-cn)** - Default
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Polish (pl)
- Turkish (tr)
- Russian (ru)
- Dutch (nl)
- Czech (cs)
- Arabic (ar)
- Japanese (ja)
- Hungarian (hu)
- Korean (ko)

## Performance on Mac M3

This app is optimized to use Metal Performance Shaders (MPS) on Mac M3, providing GPU acceleration for faster text-to-speech generation compared to CPU-only processing.

## Troubleshooting

### MPS not available

If MPS is not detected, the app will fall back to CPU. To verify MPS support:

```bash
python -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"
```

### First run is slow

The first run downloads the XTTS-v2 model (~2GB), which may take some time. Subsequent runs will be much faster.

## Project Structure

```
.
├── pyproject.toml      # Project configuration and dependencies
├── text2speech.py      # Main CLI application
├── setup.sh            # Setup script
├── .python-version     # Python version for uv
├── example.txt         # Example Chinese text file
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Examples

### Chinese Text Examples

```bash
# Direct text
text2speech "今天天气很好。"

# From file
text2speech -f example.txt -o story.mp3

# With custom voice
text2speech "你好！" -s my_voice.wav -o custom_voice.mp3
```

### Multi-language Examples

```bash
# English
text2speech "Welcome to text-to-speech!" -l en

# Spanish
text2speech "Hola, ¿cómo estás?" -l es

# Japanese
text2speech "今日はいい天気ですね。" -l ja

# Korean
text2speech "안녕하세요, 반갑습니다!" -l ko
```

## License

This project uses Coqui XTTS-v2, which is licensed under the Coqui Public Model License.
