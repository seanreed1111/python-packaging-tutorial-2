"""Karaoke filter implementation with Cython optimizations."""

import numpy as np


def vocal_removal(left_channel, right_channel):
    """
    Remove vocals by subtracting stereo channels.
    
    Args:
        left_channel: numpy array of left channel samples
        right_channel: numpy array of right channel samples
    
    Returns:
        numpy array with vocals removed
    """
    # Ensure channels are same length
    min_length = min(len(left_channel), len(right_channel))
    left = left_channel[:min_length]
    right = right_channel[:min_length]
    
    # Subtract right from left to remove center-panned vocals
    return left - right


def vocal_isolation(left_channel, right_channel):
    """
    Isolate vocals by adding stereo channels and reducing instruments.
    
    Args:
        left_channel: numpy array of left channel samples  
        right_channel: numpy array of right channel samples
    
    Returns:
        numpy array with vocals isolated
    """
    # Ensure channels are same length
    min_length = min(len(left_channel), len(right_channel))
    left = left_channel[:min_length]
    right = right_channel[:min_length]
    
    # Add channels to enhance center-panned vocals
    return (left + right) * 0.5


def dynamic_vocal_removal(left_channel, right_channel, threshold=0.3):
    """
    Dynamically remove vocals based on correlation between channels.
    
    Args:
        left_channel: numpy array of left channel samples
        right_channel: numpy array of right channel samples  
        threshold: correlation threshold for vocal removal
    
    Returns:
        numpy array with adaptive vocal removal
    """
    min_length = min(len(left_channel), len(right_channel))
    left = left_channel[:min_length]
    right = right_channel[:min_length]
    
    # Window size for correlation analysis
    window_size = 1024
    output = np.zeros(min_length)
    
    for i in range(0, min_length, window_size):
        end_idx = min(i + window_size, min_length)
        left_window = left[i:end_idx]
        right_window = right[i:end_idx]
        
        # Calculate correlation
        if len(left_window) > 1:
            correlation = np.corrcoef(left_window, right_window)[0, 1]
            
            # If high correlation, likely vocal content - remove it
            if abs(correlation) > threshold:
                output[i:end_idx] = left_window - right_window
            else:
                # Keep original stereo image for instruments
                output[i:end_idx] = (left_window + right_window) * 0.5
        else:
            output[i:end_idx] = left_window
    
    return output
