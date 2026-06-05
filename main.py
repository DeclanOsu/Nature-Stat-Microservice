"""
Nature stat modifier service.

GET /health
GET /natures
GET /natures/<name>
"""

from flask import Flask, jsonify
from data.natures import NATURES, build_modifiers

app = Flask(__name__)


def format_nature(name: str, entry: dict) -> dict:
    return {
        "name": name,
        "boosted_stat": entry["boosted_stat"],
        "lowered_stat": entry["lowered_stat"],
        "modifiers": build_modifiers(entry),
    }


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "nature-stat-modifier"})


@app.get("/natures")
def list_natures():
    """Returns all 25 natures with their modifier info."""
    natures = [format_nature(name, entry) for name, entry in NATURES.items()]
    return jsonify({"count": len(natures), "natures": natures})


@app.get("/natures/<name>")
def get_nature(name: str):
    """
    Returns modifier info for a single nature.

    400 if the nature name is not recognised.
    """
    normalised = name.strip().lower()
    entry = NATURES.get(normalised)

    if entry is None:
        return jsonify({
            "error": "Invalid nature",
            "message": (
                f'"{name}" is not a recognised nature. '
                "Call GET /natures for the full list."
            ),
        }), 400

    return jsonify(format_nature(normalised, entry))


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": str(e)}), 404


if __name__ == "__main__":
    app.run(port=3001, debug=False)
