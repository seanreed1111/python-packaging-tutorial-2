# Sound Processing Library

A high-performance audio processing library built with Cython for maximum speed.

## Features

- **Audio Effects**: Echo, reverse, surround sound effects
- **Audio Filters**: Vocal removal/isolation, synthesis, vocoding
- **Format Support**: WAV file reading and writing
- **Cython Acceleration**: Optimized for performance-critical audio processing

## Installation

### Development Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd python_packaging_tutorial_2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Build the Cython extensions:
```bash
python setup.py build_ext --inplace
```

### Building a Distribution

To build a wheel distribution:
```bash
python -m build --wheel
```

To build and install the package in one step:
```bash
pip install .
```

## Usage

### Basic Example

```python
import numpy as np
from sound.effects import echo
from sound.filters import karaoke
from sound.formats import waveread

# Load audio data
samples, sample_rate, header = waveread.load_wave_file("input.wav")

# Apply echo effect
echo_samples = echo.apply_echo(samples, delay_samples=4000, decay_factor=0.6)

# Apply vocal removal for karaoke
if samples.ndim == 2:  # Stereo
    karaoke_samples = karaoke.vocal_removal(samples[:, 0], samples[:, 1])
```

### Effects Examples

```python
from sound.effects import echo, reverse

# Generate test signal
test_signal = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100))

# Apply effects
echo_signal = echo.apply_echo(test_signal)
reverse_signal = reverse.reverse_audio(test_signal)
```

## Development

### Project Structure

```
sound/
├── __init__.py
├── effects/          # Audio effects
│   ├── echo.py
│   ├── reverse.py
│   └── surround.py
├── filters/          # Audio filters
│   ├── karaoke.py
│   ├── synth.py
│   └── vocoder.py
└── formats/          # File format handling
    ├── waveread.py
    └── wavewrite.py
```

### Building with Cython

The package automatically compiles Python modules to Cython extensions for better performance. The setup.py configuration handles:

- Compiler optimizations (`-O3`, `-ffast-math`)
- NumPy integration
- Cython compiler directives for maximum speed
- Organized build output:
  - Generated C files: `build/cython/`
  - HTML annotation files: `build/annotations/`
  - Coverage reports: `build/annotations/coverage.xml`

### Build Directory Structure

```
build/
├── cython/          # Generated C source files
│   ├── sound/
│   │   ├── effects/
│   │   ├── filters/
│   │   └── formats/
├── annotations/     # Cython HTML annotation files
│   ├── *.html      # Per-module optimization reports
│   └── coverage.xml # Coverage analysis
└── lib*/           # Compiled extension modules
```

### Cleaning Build Files

To remove all generated files and start fresh:

```bash
python clean.py
```

This removes:
- All build directories (`build/`, `dist/`, `sound.egg-info/`)
- Generated C files (`*.c`)
- Compiled extensions (`*.so`, `*.pyd`)
- HTML annotation files (`*.html`)
- Python cache files

### Performance

The Cython compilation provides significant performance improvements for:
- Tight loops in audio processing
- NumPy array operations
- Mathematical computations

## License

MIT License 