#!/usr/bin/env python3
"""
Simple player for recorded 16-step JSON patterns.

JSON schema (produced by midi_recorder.export_pattern_json):
{
  "steps_total": 16,
  "tempo": <optional int BPM>,
  "pattern": [
    {"note": <int|null>, "len": <int>},  # length in steps (1..4) at note start; 0 elsewhere
    ... (16 items total) ...
  ]
}
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import List, Tuple

import rtmidi  # type: ignore


def list_output_ports() -> List[str]:
    midi = rtmidi.MidiOut()
    names = [midi.get_port_name(i) for i in range(midi.get_port_count())]
    del midi
    return names


def choose_output_port(index: int | None) -> rtmidi.MidiOut:
    midi = rtmidi.MidiOut()
    ports = list_output_ports()
    if not ports:
        raise RuntimeError("利用可能なMIDI出力ポートがありません。仮想デバイス等を用意してください。")
    if index is None:
        print("利用可能なMIDI出力ポート:")
        for i, name in enumerate(ports):
            print(f"  [{i}] {name}")
        while True:
            try:
                sel = int(input(f"ポート番号を選択 (0-{len(ports)-1}): ").strip())
            except Exception:
                continue
            if 0 <= sel < len(ports):
                index = sel
                break
    assert index is not None
    midi.open_port(int(index))
    print(f"MIDI出力: {ports[int(index)]}")
    return midi


def load_pattern(path: Path) -> Tuple[int, List[dict]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    steps_total = int(obj.get("steps_total", 16))
    pattern = obj.get("pattern") or []
    return steps_total, pattern


def build_events(pattern: List[dict], tempo: int, channel: int, velocity: int) -> List[Tuple[float, List[int]]]:
    """Return list of (time_sec_from_zero, midi_message)."""
    # 16分音符 = 60/tempo/4 秒
    step_sec = 60.0 / max(1, int(tempo)) / 4.0
    ch = max(0, min(15, int(channel)))
    vel = max(1, min(127, int(velocity)))
    events: List[Tuple[float, List[int]]] = []
    t = 0.0
    for step in pattern:
        note = step.get("note")
        length = int(step.get("len", 0))
        if isinstance(note, int) and length > 0:
            note_num = max(0, min(127, int(note)))
            on = [0x90 + ch, note_num, vel]
            off = [0x80 + ch, note_num, 0]
            events.append((t, on))
            events.append((t + step_sec * length, off))
        t += step_sec
    # 時刻順にソート
    events.sort(key=lambda x: x[0])
    return events


def play(events: List[Tuple[float, List[int]]], midi: rtmidi.MidiOut) -> None:
    start = time.monotonic()
    for when, msg in events:
        now = time.monotonic() - start
        wait = when - now
        if wait > 0:
            time.sleep(wait)
        midi.send_message(msg)


def main() -> None:
    ap = argparse.ArgumentParser(description="16ステップJSONの簡易MIDI再生")
    ap.add_argument("json", type=Path, help="入力JSON (recorded-pattern.json)")
    ap.add_argument("--midi-port", type=int, default=None, help="MIDI出力ポート番号（未指定は対話選択）")
    ap.add_argument("--tempo", type=int, default=None, help="BPMを上書き（未指定はJSONのtempo、無ければ120）")
    ap.add_argument("--channel", type=int, default=0, help="MIDIチャンネル 0-15 (default 0)")
    ap.add_argument("--velocity", type=int, default=100, help="ベロシティ 1-127 (default 100)")
    ap.add_argument("--loops", type=int, default=1, help="再生回数 (default 1)")
    ap.add_argument("--list-ports", action="store_true", help="出力ポート一覧を表示して終了")
    args = ap.parse_args()

    if args.list_ports:
        ports = list_output_ports()
        if ports:
            print("利用可能なMIDI出力ポート:")
            for i, name in enumerate(ports):
                print(f"  [{i}] {name}")
        else:
            print("MIDI出力ポートが見つかりません")
        return

    steps_total, pattern = load_pattern(args.json)
    # tempo決定
    tempo_in = None
    try:
        obj = json.loads(args.json.read_text(encoding="utf-8"))
        if isinstance(obj.get("tempo"), int):
            tempo_in = int(obj["tempo"])
    except Exception:
        pass
    tempo = int(args.tempo or tempo_in or 120)

    midi = choose_output_port(args.midi_port)
    try:
        for n in range(max(1, int(args.loops))):
            events = build_events(pattern, tempo=tempo, channel=args.channel, velocity=args.velocity)
            print(f"再生 {n+1}/{args.loops}: tempo={tempo} BPM, steps={steps_total}, events={len(events)}")
            play(events, midi)
    finally:
        try:
            midi.close_port()
        except Exception:
            pass


if __name__ == "__main__":
    main()

