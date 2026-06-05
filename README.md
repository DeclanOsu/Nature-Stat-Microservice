# nature-stat-modifier-service

Returns stat multipliers for all 25 Pokemon natures. Part of the Pokemon damage calculator backend.

## Endpoints

### `GET /natures/<name>`

Case-insensitive. Returns the stat modifiers for a single nature.

```
GET /natures/adamant
```

```json
{
    "name": "adamant",
    "boosted_stat": "attack",
    "lowered_stat": "special_attack",
    "modifiers": {
        "hp": 1.0,
        "attack": 1.1,
        "defense": 1.0,
        "special_attack": 0.9,
        "special_defense": 1.0,
        "speed": 1.0
    }
}
```

Neutral natures return `"neutral"` for both stat fields and `1.0` for all modifiers.

Returns `400` with an error message if the nature name is not recognised.

---

### `GET /natures`

Returns all 25 natures. Useful for populating a dropdown.

```json
{
    "count": 25,
    "natures": [
        {
            "name": "adamant",
            "boosted_stat": "attack",
            "lowered_stat": "special_attack",
            "modifiers": { "hp": 1.0, "attack": 1.1, ... }
        },
        ...
    ]
}
```

---

### `GET /health`

```json
{ "status": "ok", "service": "nature-stat-modifier" }
```

---

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Runs on port `3001` by default.

## Tests

```bash
pytest
```

## Structure

```
nature-service/
+-- main.py
+-- requirements.txt
+-- pytest.ini
+-- data/
|   `-- natures.py
`-- tests/
    `-- test_main.py
```
