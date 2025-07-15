"""Wave file reading with Cython optimizations."""

import numpy as np
import struct


def read_wave_header(file_data):
    """
    Parse WAV file header.
    
    Args:
        file_data: bytes of WAV file data
    
    Returns:
        dict with header information
    """
    if len(file_data) < 44:
        raise ValueError("Invalid WAV file: too short")
    
    # Parse RIFF header
    riff_header = file_data[:12]
    if riff_header[:4] != b'RIFF' or riff_header[8:12] != b'WAVE':
        raise ValueError("Invalid WAV file: missing RIFF/WAVE header")
    
    file_size = struct.unpack('<I', riff_header[4:8])[0]
    
    # Parse fmt chunk
    fmt_chunk = file_data[12:36]
    if fmt_chunk[:4] != b'fmt ':
        raise ValueError("Invalid WAV file: missing fmt chunk")
    
    fmt_size = struct.unpack('<I', fmt_chunk[4:8])[0]
    audio_format = struct.unpack('<H', fmt_chunk[8:10])[0]
    channels = struct.unpack('<H', fmt_chunk[10:12])[0]
    sample_rate = struct.unpack('<I', fmt_chunk[12:16])[0]
    byte_rate = struct.unpack('<I', fmt_chunk[16:20])[0]
    block_align = struct.unpack('<H', fmt_chunk[20:22])[0]
    bits_per_sample = struct.unpack('<H', fmt_chunk[22:24])[0]
    
    # Find data chunk
    offset = 12 + 8 + fmt_size
    while offset < len(file_data) - 8:
        chunk_id = file_data[offset:offset+4]
        chunk_size = struct.unpack('<I', file_data[offset+4:offset+8])[0]
        
        if chunk_id == b'data':
            data_offset = offset + 8
            data_size = chunk_size
            break
        
        offset += 8 + chunk_size
    else:
        raise ValueError("Invalid WAV file: missing data chunk")
    
    return {
        'file_size': file_size,
        'audio_format': audio_format,
        'channels': channels,
        'sample_rate': sample_rate,
        'byte_rate': byte_rate,
        'block_align': block_align,
        'bits_per_sample': bits_per_sample,
        'data_offset': data_offset,
        'data_size': data_size
    }


def read_wave_samples(file_data, header_info):
    """
    Read audio samples from WAV file data.
    
    Args:
        file_data: bytes of WAV file data
        header_info: header information dict
    
    Returns:
        numpy array of audio samples
    """
    data_start = header_info['data_offset']
    data_size = header_info['data_size']
    bits_per_sample = header_info['bits_per_sample']
    channels = header_info['channels']
    
    audio_data = file_data[data_start:data_start + data_size]
    
    # Convert based on bit depth
    if bits_per_sample == 16:
        samples = np.frombuffer(audio_data, dtype=np.int16)
        samples = samples.astype(np.float32) / 32768.0
    elif bits_per_sample == 24:
        # 24-bit samples need special handling
        num_samples = len(audio_data) // 3
        samples = np.zeros(num_samples, dtype=np.float32)
        
        for i in range(num_samples):
            byte_offset = i * 3
            # Convert 3 bytes to signed 24-bit integer
            sample_bytes = audio_data[byte_offset:byte_offset + 3]
            if len(sample_bytes) == 3:
                # Little-endian 24-bit to 32-bit signed
                sample_int = struct.unpack('<I', sample_bytes + b'\x00')[0]
                if sample_int >= 2**23:
                    sample_int -= 2**24
                samples[i] = sample_int / (2**23)
    elif bits_per_sample == 32:
        samples = np.frombuffer(audio_data, dtype=np.float32)
    else:
        raise ValueError(f"Unsupported bit depth: {bits_per_sample}")
    
    # Reshape for multichannel
    if channels > 1:
        samples = samples.reshape(-1, channels)
    
    return samples


def load_wave_file(filename):
    """
    Load a complete WAV file.
    
    Args:
        filename: path to WAV file
    
    Returns:
        tuple of (samples, sample_rate, header_info)
    """
    with open(filename, 'rb') as f:
        file_data = f.read()
    
    header_info = read_wave_header(file_data)
    samples = read_wave_samples(file_data, header_info)
    
    return samples, header_info['sample_rate'], header_info
