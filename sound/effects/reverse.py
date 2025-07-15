"""Reverse effect implementation with Cython optimizations."""

import numpy as np


def reverse_audio(samples):
    """
    Reverse audio samples completely.
    
    Args:
        samples: numpy array of audio samples
    
    Returns:
        numpy array with samples in reverse order
    """
    return samples[::-1]


def reverse_segments(samples, segment_length=1024):
    """
    Reverse audio in segments for a stuttering effect.
    
    Args:
        samples: numpy array of audio samples
        segment_length: length of each segment to reverse
    
    Returns:
        numpy array with segments reversed
    """
    output = samples.copy()
    
    for i in range(0, len(samples), segment_length):
        end_idx = min(i + segment_length, len(samples))
        output[i:end_idx] = samples[i:end_idx][::-1]
    
    return output


def gate_reverse(samples, threshold=0.1, gate_length=512):
    """
    Apply reverse effect only when audio is above threshold.
    
    Args:
        samples: numpy array of audio samples
        threshold: minimum amplitude to trigger reverse
        gate_length: length of reverse segments
    
    Returns:
        numpy array with conditional reverse effect
    """
    output = samples.copy()
    
    for i in range(0, len(samples), gate_length):
        end_idx = min(i + gate_length, len(samples))
        segment = samples[i:end_idx]
        
        # Check if segment exceeds threshold
        if np.max(np.abs(segment)) > threshold:
            output[i:end_idx] = segment[::-1]
    
    return output
