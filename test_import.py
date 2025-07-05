#!/usr/bin/env python3
"""
Test script to verify MidiRecorder import and basic functionality
"""

try:
    from midi_recorder import MidiRecorder
    print("✓ MidiRecorder import successful")
    
    recorder = MidiRecorder()
    print("✓ MidiRecorder instance created")
    
    devices = recorder.list_midi_devices()
    print(f"✓ Available MIDI devices: {devices}")
    print(f"✓ Device count: {len(devices)}")
    
    notes = recorder.get_recorded_notes()
    print(f"✓ Initial notes: {notes}")
    
    count = recorder.get_note_count()
    print(f"✓ Initial note count: {count}")
    
    recorder.clear_notes()
    print("✓ Clear notes successful")
    
    print("✓ All API tests passed successfully!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    exit(1)
except Exception as e:
    print(f"✗ Error during testing: {e}")
    exit(1)
