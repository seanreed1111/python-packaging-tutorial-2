"""Surround sound effect implementation with Cython optimizations."""

import numpy as np


def create_surround_effect(mono_samples, pan_positions=None):
    """
    Create surround sound effect from mono audio.
    
    Args:
        mono_samples: numpy array of mono audio samples
        pan_positions: list of pan positions (-1.0 to 1.0) for each channel
    
    Returns:
        numpy array with multiple channels for surround effect
    """
    if pan_positions is None:
        # Default 5.1 surround positions
        pan_positions = [-0.8, 0.8, 0.0, -0.5, 0.5]  # L, R, C, LS, RS
    
    num_channels = len(pan_positions)
    output = np.zeros((len(mono_samples), num_channels), dtype=mono_samples.dtype)
    
    for ch, pan in enumerate(pan_positions):
        # Apply panning law (constant power)
        if pan <= 0:
            # Left side
            left_gain = 1.0
            right_gain = (pan + 1.0) * 0.5
        else:
            # Right side  
            left_gain = (1.0 - pan) * 0.5
            right_gain = 1.0
        
        # Apply gain based on position
        output[:, ch] = mono_samples * np.sqrt(left_gain * right_gain)
    
    return output


def apply_room_reverb(samples, room_size=0.5, damping=0.3):
    """
    Apply room reverb to create spatial effect.
    
    Args:
        samples: numpy array of audio samples
        room_size: size of simulated room (0.0 to 1.0)
        damping: high frequency damping (0.0 to 1.0)
    
    Returns:
        numpy array with reverb effect applied
    """
    # Calculate delay times based on room size
    delay_times = [
        int(room_size * 1000 + 500),   # Early reflection 1
        int(room_size * 1500 + 800),   # Early reflection 2  
        int(room_size * 2000 + 1200),  # Late reverb 1
        int(room_size * 2500 + 1600),  # Late reverb 2
    ]
    
    # Corresponding gains
    gains = [0.4, 0.3, 0.2, 0.1]
    
    # Apply damping (simple low-pass filter)
    damped_samples = samples.copy()
    if damping > 0:
        for i in range(1, len(damped_samples)):
            damped_samples[i] = (1 - damping) * damped_samples[i] + damping * damped_samples[i-1]
    
    # Create output buffer
    max_delay = max(delay_times)
    output = np.zeros(len(samples) + max_delay, dtype=samples.dtype)
    output[:len(samples)] = samples
    
    # Add reflections
    for delay, gain in zip(delay_times, gains):
        for i in range(len(samples)):
            output_pos = i + delay
            if output_pos < len(output):
                output[output_pos] += damped_samples[i] * gain
    
    return output


def doppler_effect(samples, velocity_factor=1.0):
    """
    Apply Doppler effect to simulate moving sound source.
    
    Args:
        samples: numpy array of audio samples
        velocity_factor: velocity as fraction of sound speed
    
    Returns:
        numpy array with Doppler effect applied
    """
    # Calculate frequency shift factor
    freq_factor = 1.0 / (1.0 + velocity_factor)
    
    # Resample to simulate frequency shift
    original_length = len(samples)
    new_length = int(original_length * freq_factor)
    
    # Create new time indices
    new_indices = np.linspace(0, original_length - 1, new_length)
    
    # Interpolate samples
    output = np.interp(new_indices, np.arange(original_length), samples)
    
    return output
