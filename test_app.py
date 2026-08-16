from flask import Flask, request, jsonify, send_from_directory, abort

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))



STATIC_DIR = Path(__file__).resolve().parent / "static"

def load_equity_data():
    equity_file = STATIC_DIR / "equity_grid.csv"
    if not equity_file.exists():
        raise FileNotFoundError(f"Equity data file not found: {equity_file}")

    df = pd.read_csv(equity_file)
    equity_map = {row['Hand']: row['Equity'] for _, row in df.iterrows()}
    return equity_map

equity_map = load_equity_data()

def create_app(db_path, grid_path=None, grid_trials=2000):

    app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")
    print(app.static_folder)
    equity_map = load_equity_data()
    @app.route("/")
    def index():
        # return jsonify({"joke": random.choice(["Why did the chicken cross the road?", "To get to the other side!"])})
        return send_from_directory(STATIC_DIR, "index.html")

    @app.get('/api/equity')
    def get_equity():
        try:
            hand = request.args.get('hand', '')
            hand_rev = hand[1] + hand[0] + hand[-1] if len(hand) == 3 else hand
            equity = equity_map.get(hand, equity_map.get(hand_rev, None))
            return jsonify({"hand": hand, "equity": equity})

        except (ValueError, TypeError):
            abort(400, description="Invalid input")

    return app


if __name__ == "__main__":
    flask_app = create_app(str(Path(__file__).resolve().parent))
    flask_app.run(debug=True)
