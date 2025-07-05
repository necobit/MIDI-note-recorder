#!/usr/bin/env python3
"""
MIDI Note Recorder

MIDIを受信してその音符を一時的に記録するためのPythonスクリプト
他のPythonスクリプトにデータを渡せるようなデータ構造にしてください。
必要なデータはノートナンバーのみです。
受信したノートオンを受信した順に8個記録します。
他のPythonスクリプトから要求されたらノートナンバーを渡します。
起動時にMIDI入力を受けるデバイスを選択できるようにします。
"""

import rtmidi
import threading
import time
from collections import deque
from typing import List, Optional


class MidiRecorder:
    def __init__(self):
        self.midi_in = None
        self.note_buffer = deque(maxlen=8)
        self.is_recording = False
        self.lock = threading.Lock()
        
    def list_midi_devices(self) -> List[str]:
        """利用可能なMIDI入力デバイスのリストを取得"""
        midi_in = rtmidi.MidiIn()
        devices = []
        for i in range(midi_in.get_port_count()):
            devices.append(midi_in.get_port_name(i))
        midi_in.close_port()
        del midi_in
        return devices
    
    def select_midi_device(self) -> Optional[int]:
        """MIDI入力デバイスを選択"""
        devices = self.list_midi_devices()
        
        if not devices:
            print("利用可能なMIDI入力デバイスが見つかりません。")
            return None
        
        print("\n利用可能なMIDI入力デバイス:")
        for i, device in enumerate(devices):
            print(f"{i}: {device}")
        
        while True:
            try:
                choice = input(f"\nデバイスを選択してください (0-{len(devices)-1}): ")
                device_index = int(choice)
                if 0 <= device_index < len(devices):
                    return device_index
                else:
                    print(f"0から{len(devices)-1}の間の数字を入力してください。")
            except ValueError:
                print("有効な数字を入力してください。")
            except KeyboardInterrupt:
                print("\n終了します。")
                return None
    
    def midi_callback(self, message, data):
        """MIDIメッセージを受信したときのコールバック関数"""
        midi_message, delta_time = message
        
        if len(midi_message) >= 3:
            status = midi_message[0]
            note_number = midi_message[1]
            velocity = midi_message[2]
            
            if (status & 0xF0) == 0x90 and velocity > 0:
                with self.lock:
                    self.note_buffer.append(note_number)
                print(f"ノートオン受信: {note_number}")
    
    def start_recording(self, device_index: int) -> bool:
        """MIDI録音を開始"""
        try:
            self.midi_in = rtmidi.MidiIn()
            self.midi_in.open_port(device_index)
            self.midi_in.set_callback(self.midi_callback)
            self.is_recording = True
            print(f"MIDI録音を開始しました。デバイス: {self.midi_in.get_port_name(device_index)}")
            print("ノートオンイベントを待機中... (Ctrl+Cで終了)")
            return True
        except Exception as e:
            print(f"MIDI録音の開始に失敗しました: {e}")
            return False
    
    def stop_recording(self):
        """MIDI録音を停止"""
        if self.midi_in:
            self.midi_in.close_port()
            self.midi_in = None
        self.is_recording = False
        print("MIDI録音を停止しました。")
    
    def get_recorded_notes(self) -> List[int]:
        """記録されたノートナンバーのリストを取得"""
        with self.lock:
            return list(self.note_buffer)
    
    def clear_notes(self):
        """記録されたノートをクリア"""
        with self.lock:
            self.note_buffer.clear()
        print("記録されたノートをクリアしました。")
    
    def get_note_count(self) -> int:
        """記録されたノートの数を取得"""
        with self.lock:
            return len(self.note_buffer)


def main():
    """メイン関数"""
    recorder = MidiRecorder()
    
    device_index = recorder.select_midi_device()
    if device_index is None:
        return
    
    if not recorder.start_recording(device_index):
        return
    
    try:
        while True:
            time.sleep(0.1)
            notes = recorder.get_recorded_notes()
            if notes:
                print(f"\r現在記録されているノート: {notes} (計{len(notes)}個)", end="", flush=True)
    except KeyboardInterrupt:
        print("\n")
        recorder.stop_recording()
        final_notes = recorder.get_recorded_notes()
        print(f"最終的に記録されたノート: {final_notes}")


if __name__ == "__main__":
    main()
