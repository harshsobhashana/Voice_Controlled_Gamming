🎙️ Voice-Controlled Chess 🎮
Voice-Controlled Chess is a single-player chess engine that works based on voice commands given by the user. The opponent is an AI player that makes moves using the Minimax and Alpha-Beta Pruning algorithms.

📦 Modules & Libraries Used
To install the required dependencies, use the following commands:
=> pip install pygame speech_recognition pyaudio playsound
⚠️ For PyAudio installation, use:
=> pip install pipwin
=> pipwin install pyaudio

📂 Main Files
♟️ Chess.py
Contains valid moves logic for a chess game.
Uses bitboard representation for the chessboard.
Implements AI move generation using the Minimax and Alpha-Beta Pruning algorithms.
🖥️ Gui.py
Allows you to control board size and difficulty level.
Provides keyboard shortcuts for different in-game actions.

🕹️ How to Play
This is a single-player chess game where you play against an AI opponent. Your piece color (White or Black) is assigned randomly.

🎮 Game Controls
▶ Start the Game: Click anywhere on the board with your mouse.
♟️ Make a Move:
Use the format 2836, where:
28 → Original position (Column 2, Row 8)
36 → New position (Column 3, Row 6)
Alternatively, you can use chess notation (e.g., B8C6 for B8 → C6).
If the move is invalid, you will be asked to retry.
⌨️ Keyboard Shortcuts
🎨 Change Board Color → Press C
💡 Hint for Next Move → Press H
❌ Quit the Game → Press Q
📜 View Move List → Press P or D
📊 Evaluate Score → Press E
🔙 Undo Last Move → Press U
♟️ Enjoy playing Voice-Controlled Chess! 🎙️🎮♞
