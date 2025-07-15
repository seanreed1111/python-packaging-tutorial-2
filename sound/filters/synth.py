"""Synthesis filter implementation with Cython optimizations."""

import numpy as np


def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """
    Generate a sine wave.
    
    Args:
        frequency: frequency in Hz
        duration: duration in seconds
        sample_rate: sample rate in Hz
        amplitude: amplitude (0.0 to 1.0)
    
    Returns:
        numpy array of sine wave samples
    """
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t)


def generate_sawtooth_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """
    Generate a sawtooth wave.
    
    Args:
        frequency: frequency in Hz
        duration: duration in seconds
        sample_rate: sample rate in Hz
        amplitude: amplitude (0.0 to 1.0)
    
    Returns:
        numpy array of sawtooth wave samples
    """
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    
    # Generate sawtooth using phase accumulation
    phase = (frequency * t) % 1.0
    return amplitude * (2 * phase - 1)


def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=0.5, duty_cycle=0.5):
    """
    Generate a square wave.
    
    Args:
        frequency: frequency in Hz
        duration: duration in seconds
        sample_rate: sample rate in Hz
        amplitude: amplitude (0.0 to 1.0)
        duty_cycle: duty cycle (0.0 to 1.0)
    
    Returns:
        numpy array of square wave samples
    """
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    
    # Generate square wave
    phase = (frequency * t) % 1.0
    return amplitude * np.where(phase < duty_cycle, 1.0, -1.0)


def apply_adsr_envelope(samples, attack_time=0.1, decay_time=0.1, sustain_level=0.7, release_time=0.2, sample_rate=44100):
    """
    Apply ADSR (Attack, Decay, Sustain, Release) envelope to samples.
    
    Args:
        samples: numpy array of audio samples
        attack_time: attack time in seconds
        decay_time: decay time in seconds  
        sustain_level: sustain level (0.0 to 1.0)
        release_time: release time in seconds
        sample_rate: sample rate in Hz
    
    Returns:
        numpy array with ADSR envelope applied
    """
    total_samples = len(samples)
    envelope = np.zeros(total_samples)
    
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    
    # Calculate sustain samples
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples
    if sustain_samples < 0:
        sustain_samples = 0
        # Adjust other phases if note is too short
        total_env_samples = attack_samples + decay_samples + release_samples
        if total_env_samples > total_samples:
            scale_factor = total_samples / total_env_samples
            attack_samples = int(attack_samples * scale_factor)
            decay_samples = int(decay_samples * scale_factor)
            release_samples = total_samples - attack_samples - decay_samples
    
    current_pos = 0
    
    # Attack phase
    if attack_samples > 0:
        envelope[current_pos:current_pos + attack_samples] = np.linspace(0, 1, attack_samples)
        current_pos += attack_samples
    
    # Decay phase
    if decay_samples > 0:
        envelope[current_pos:current_pos + decay_samples] = np.linspace(1, sustain_level, decay_samples)
        current_pos += decay_samples
    
    # Sustain phase
    if sustain_samples > 0:
        envelope[current_pos:current_pos + sustain_samples] = sustain_level
        current_pos += sustain_samples
    
    # Release phase
    if release_samples > 0:
        envelope[current_pos:current_pos + release_samples] = np.linspace(sustain_level, 0, release_samples)
    
    return samples * envelope


def low_pass_filter(samples, cutoff_freq, sample_rate=44100, resonance=1.0):
    """
    Apply a simple low-pass filter.
    
    Args:
        samples: numpy array of audio samples
        cutoff_freq: cutoff frequency in Hz
        sample_rate: sample rate in Hz
        resonance: filter resonance (1.0 = no resonance)
    
    Returns:
        numpy array with low-pass filter applied
    """
    # Calculate filter coefficient
    dt = 1.0 / sample_rate
    rc = 1.0 / (2 * np.pi * cutoff_freq)
    alpha = dt / (rc + dt)
    
    # Apply filter
    output = np.zeros_like(samples)
    if len(samples) > 0:
        output[0] = samples[0] * alpha
        
        for i in range(1, len(samples)):
            output[i] = alpha * samples[i] + (1 - alpha) * output[i-1]
            
            # Add resonance by feeding back some of the output
            if resonance > 1.0:
                feedback = output[i] * (resonance - 1.0) * 0.1
                output[i] = np.clip(output[i] + feedback, -1.0, 1.0)
    
    return output
