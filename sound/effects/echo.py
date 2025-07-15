"""Echo effect implementation with Cython optimizations."""

import numpy as np


def apply_echo(samples, delay_samples=8000, decay_factor=0.5):
    """
    Apply echo effect to audio samples.
    
    Args:
        samples: numpy array of audio samples
        delay_samples: number of samples to delay for echo
        decay_factor: how much to decay the echo (0.0 to 1.0)
    
    Returns:
        numpy array with echo effect applied
    """
    if len(samples) == 0:
        return samples
    
    # Create output buffer with extra space for echo tail
    output_length = len(samples) + delay_samples
    output = np.zeros(output_length, dtype=samples.dtype)
    
    # Copy original samples
    output[:len(samples)] = samples
    
    # Add delayed echo
    for i in range(len(samples)):
        echo_pos = i + delay_samples
        if echo_pos < output_length:
            output[echo_pos] += samples[i] * decay_factor
    
    return output


def multi_echo(samples, delays=None, decays=None):
    """
    Apply multiple echo effects with different delays and decay factors.
    
    Args:
        samples: numpy array of audio samples
        delays: list of delay amounts in samples
        decays: list of decay factors for each echo
    
    Returns:
        numpy array with multiple echo effects applied
    """
    if delays is None:
        delays = [4000, 8000, 12000]
    if decays is None:
        decays = [0.6, 0.4, 0.2]
    
    output = samples.copy()
    
    for delay, decay in zip(delays, decays):
        output = apply_echo(output, delay, decay)
    
    return output
