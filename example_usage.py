#!/usr/bin/env python3
"""
MIDI Recorder 使用例

他のPythonスクリプトからMidiRecorderクラスを使用する方法を示します。
"""

import time
import threading
from midi_recorder import MidiRecorder


def example_usage():
    """MidiRecorderの使用例"""
    print("=== MIDI Recorder 使用例 ===")
    
    recorder = MidiRecorder()
    
    devices = recorder.list_midi_devices()
    print(f"利用可能なMIDIデバイス: {devices}")
    
    if not devices:
        print("MIDIデバイスが見つかりません。仮想MIDIデバイスまたは物理MIDIデバイスを接続してください。")
        return
    
    device_index = 0
    print(f"デバイス {device_index} を使用: {devices[device_index]}")
    
    if recorder.start_recording(device_index):
        print("録音開始。10秒間MIDIノートを受信します...")
        
        for i in range(10):
            time.sleep(1)
            notes = recorder.get_recorded_notes()
            count = recorder.get_note_count()
            print(f"経過時間: {i+1}秒, 記録されたノート: {notes}, 数: {count}")
        
        recorder.stop_recording()
        
        final_notes = recorder.get_recorded_notes()
        print(f"\n最終的に記録されたノート: {final_notes}")
        
        recorder.clear_notes()
        print(f"クリア後のノート: {recorder.get_recorded_notes()}")


def background_monitoring_example():
    """バックグラウンドでMIDI録音を監視する例"""
    print("\n=== バックグラウンド監視例 ===")
    
    recorder = MidiRecorder()
    devices = recorder.list_midi_devices()
    
    if not devices:
        print("MIDIデバイスが見つかりません。")
        return
    
    device_index = 0
    
    def monitor_notes():
        """ノートを監視するバックグラウンド関数"""
        previous_notes = []
        while recorder.is_recording:
            current_notes = recorder.get_recorded_notes()
            if current_notes != previous_notes:
                print(f"ノートが更新されました: {current_notes}")
                previous_notes = current_notes.copy()
            time.sleep(0.5)
    
    if recorder.start_recording(device_index):
        monitor_thread = threading.Thread(target=monitor_notes, daemon=True)
        monitor_thread.start()
        
        print("5秒間バックグラウンドで監視します...")
        time.sleep(5)
        
        recorder.stop_recording()
        print("監視終了")


if __name__ == "__main__":
    try:
        example_usage()
        background_monitoring_example()
    except KeyboardInterrupt:
        print("\n例の実行が中断されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
