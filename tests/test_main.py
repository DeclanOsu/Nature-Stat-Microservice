import time
import pytest
from main import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestGetNature:
    def test_returns_correct_data_for_stat_modifying_nature(self, client):
        r = client.get("/natures/adamant")
        assert r.status_code == 200
        body = r.get_json()
        assert body["name"] == "adamant"
        assert body["boosted_stat"] == "attack"
        assert body["lowered_stat"] == "special_attack"
        assert body["modifiers"]["attack"] == pytest.approx(1.1)
        assert body["modifiers"]["special_attack"] == pytest.approx(0.9)
        assert body["modifiers"]["hp"] == pytest.approx(1.0)
        assert body["modifiers"]["defense"] == pytest.approx(1.0)
        assert body["modifiers"]["special_defense"] == pytest.approx(1.0)
        assert body["modifiers"]["speed"] == pytest.approx(1.0)

    def test_case_insensitive(self, client):
        for variant in ("Timid", "TIMID", "timid", "tImId"):
            r = client.get(f"/natures/{variant}")
            assert r.status_code == 200
            assert r.get_json()["name"] == "timid"

    def test_neutral_nature_all_ones(self, client):
        r = client.get("/natures/hardy")
        assert r.status_code == 200
        body = r.get_json()
        assert body["boosted_stat"] == "neutral"
        assert body["lowered_stat"] == "neutral"
        for value in body["modifiers"].values():
            assert value == pytest.approx(1.0)

    def test_all_five_neutral_natures(self, client):
        for name in ("hardy", "docile", "serious", "bashful", "quirky"):
            r = client.get(f"/natures/{name}")
            assert r.status_code == 200
            body = r.get_json()
            assert body["boosted_stat"] == "neutral"
            assert body["lowered_stat"] == "neutral"

    def test_unknown_nature_returns_400(self, client):
        r = client.get("/natures/fakemon")
        assert r.status_code == 400
        body = r.get_json()
        assert "error" in body
        assert "message" in body

    def test_numeric_name_returns_400(self, client):
        r = client.get("/natures/12345")
        assert r.status_code == 400

    @pytest.mark.parametrize("name,boosted,lowered", [
        ("lonely",   "attack",          "defense"),
        ("brave",    "attack",          "speed"),
        ("adamant",  "attack",          "special_attack"),
        ("naughty",  "attack",          "special_defense"),
        ("bold",     "defense",         "attack"),
        ("relaxed",  "defense",         "speed"),
        ("impish",   "defense",         "special_attack"),
        ("lax",      "defense",         "special_defense"),
        ("timid",    "speed",           "attack"),
        ("hasty",    "speed",           "defense"),
        ("jolly",    "speed",           "special_attack"),
        ("naive",    "speed",           "special_defense"),
        ("modest",   "special_attack",  "attack"),
        ("mild",     "special_attack",  "defense"),
        ("quiet",    "special_attack",  "speed"),
        ("rash",     "special_attack",  "special_defense"),
        ("calm",     "special_defense", "attack"),
        ("gentle",   "special_defense", "defense"),
        ("sassy",    "special_defense", "speed"),
        ("careful",  "special_defense", "special_attack"),
    ])
    def test_stat_modifying_natures(self, client, name, boosted, lowered):
        r = client.get(f"/natures/{name}")
        assert r.status_code == 200
        body = r.get_json()
        assert body["boosted_stat"] == boosted
        assert body["lowered_stat"] == lowered
        assert body["modifiers"][boosted] == pytest.approx(1.1)
        assert body["modifiers"][lowered] == pytest.approx(0.9)

    def test_response_under_200ms(self, client):
        start = time.monotonic()
        client.get("/natures/adamant")
        assert (time.monotonic() - start) * 1000 < 200


class TestListNatures:
    def test_returns_all_25(self, client):
        r = client.get("/natures")
        assert r.status_code == 200
        body = r.get_json()
        assert body["count"] == 25
        assert len(body["natures"]) == 25

    def test_each_entry_has_required_fields(self, client):
        r = client.get("/natures")
        for nature in r.get_json()["natures"]:
            assert "name" in nature
            assert "boosted_stat" in nature
            assert "lowered_stat" in nature
            assert "modifiers" in nature
            for stat in ("hp", "attack", "defense", "special_attack", "special_defense", "speed"):
                assert stat in nature["modifiers"]

    def test_exactly_5_neutral_natures(self, client):
        r = client.get("/natures")
        neutrals = [n for n in r.get_json()["natures"] if n["boosted_stat"] == "neutral"]
        assert len(neutrals) == 5

    def test_response_under_200ms(self, client):
        start = time.monotonic()
        client.get("/natures")
        assert (time.monotonic() - start) * 1000 < 200


class TestHealth:
    def test_returns_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.get_json()["status"] == "ok"
