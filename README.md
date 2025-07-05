# MIDI Note Recorder

MIDI を受信してその音符を一時的に記録するための Python スクリプトです。

## 機能

- MIDI入力デバイスからノートオンイベントを受信
- 受信したノートナンバーを受信順に最大8個まで記録
- 他のPythonスクリプトからデータにアクセス可能なAPI提供
- 起動時のMIDI入力デバイス選択機能
- 仮想環境での動作サポート

## 必要な環境

- Python 3.6以上
- MIDIデバイス（物理デバイスまたは仮想MIDIデバイス）

## セットアップと実行

### 自動セットアップ（推奨）

```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### 手動セットアップ

```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境のアクティベート
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# MIDI Note Recorderの実行
python midi_recorder.py
```

## 使用方法

### スタンドアロン実行

```bash
python midi_recorder.py
```

起動時に利用可能なMIDI入力デバイスが表示され、選択できます。
選択後、MIDIノートオンイベントの受信を開始し、最新の8個のノートナンバーを記録します。

### 他のPythonスクリプトからの使用

```python
from midi_recorder import MidiRecorder

# MidiRecorderインスタンスを作成
recorder = MidiRecorder()

# 利用可能なデバイスを取得
devices = recorder.list_midi_devices()

# デバイスを選択して録音開始
device_index = 0  # 使用するデバイスのインデックス
recorder.start_recording(device_index)

# 記録されたノートを取得
notes = recorder.get_recorded_notes()  # [60, 62, 64, ...] のようなリスト

# 録音停止
recorder.stop_recording()
```

## API リファレンス

### MidiRecorder クラス

#### メソッド

- `list_midi_devices()` → `List[str]`: 利用可能なMIDI入力デバイスのリストを取得
- `select_midi_device()` → `Optional[int]`: 対話的にMIDI入力デバイスを選択
- `start_recording(device_index: int)` → `bool`: 指定されたデバイスで録音を開始
- `stop_recording()`: 録音を停止
- `get_recorded_notes()` → `List[int]`: 記録されたノートナンバーのリストを取得（最新8個）
- `clear_notes()`: 記録されたノートをクリア
- `get_note_count()` → `int`: 記録されたノートの数を取得

#### プロパティ

- `is_recording`: 録音中かどうかを示すブール値

## ファイル構成

- `midi_recorder.py`: メインのMIDI録音スクリプト
- `requirements.txt`: Python依存関係
- `setup_and_run.sh`: 自動セットアップ・実行スクリプト
- `example_usage.py`: 使用例スクリプト
- `README.md`: このファイル

## 使用例

詳細な使用例は `example_usage.py` を参照してください。

```bash
python example_usage.py
```

## 注意事項

- MIDIデバイスが接続されていない場合、利用可能なデバイスが表示されません
- 仮想MIDIデバイス（例：loopMIDI、IAC Driver）を使用してテストできます
- 録音中はCtrl+Cで終了できます
