"""Tests — Region-Codec Save v5 (M24 Phase 2)."""

from __future__ import annotations

from game_core.region_codec import (
    NO_PAYLOAD_OFFSET,
    SLOT_FLAG_DISCOVERED,
    SLOT_FLAG_HAS_PAYLOAD,
    SLOT_FLAG_MODIFIED,
    ChunkModificationBlob,
    RegionFile,
    SlotEntry,
    SuppressionRecord,
    TileOverrideRecord,
    decode_chunk_modification,
    decode_region_file,
    encode_chunk_modification,
    encode_region_file,
)
from game_core.world_coords import REGION_CHUNKS, REGION_SLOT_COUNT, chunk_to_region
from game_core.world_gen import KEY_STONE


def _empty_region(rx: int = 0, rz: int = 0) -> RegionFile:
    return RegionFile(region_rx=rx, region_rz=rz)


def test_encode_decode_empty_region() -> None:
    raw = encode_region_file(_empty_region())
    result = decode_region_file(raw)
    assert result.error is None
    assert result.region is not None
    assert all(slot.flags == 0 for slot in result.region.slots)


def test_discovered_only_slot() -> None:
    region = _empty_region()
    slots = list(region.slots)
    slots[0] = SlotEntry(flags=SLOT_FLAG_DISCOVERED)
    region = RegionFile(region_rx=0, region_rz=0, slots=tuple(slots))
    result = decode_region_file(encode_region_file(region))
    assert result.region is not None
    assert result.region.slots[0].flags == SLOT_FLAG_DISCOVERED
    assert result.region.slots[0].payload == b""


def test_modified_slot_with_payload_roundtrip() -> None:
    blob = ChunkModificationBlob(
        tile_overrides=(
            TileOverrideRecord(layer=0, local_tx=3, local_tz=4, tile_key=KEY_STONE),
        ),
        suppressions=(
            SuppressionRecord(wx=10, wz=11, decoration_id="trees/apple/summer/apple_1"),
        ),
    )
    payload = encode_chunk_modification(blob)
    decoded_blob = decode_chunk_modification(payload)
    assert decoded_blob.tile_overrides == blob.tile_overrides
    assert decoded_blob.suppressions == blob.suppressions

    region = _empty_region()
    slots = list(region.slots)
    slots[5] = SlotEntry(
        flags=SLOT_FLAG_DISCOVERED | SLOT_FLAG_MODIFIED | SLOT_FLAG_HAS_PAYLOAD,
        payload=payload,
    )
    region = RegionFile(region_rx=1, region_rz=-1, slots=tuple(slots))
    raw = encode_region_file(region)
    result = decode_region_file(raw)
    assert result.error is None
    assert result.region is not None
    assert result.region.region_rx == 1
    assert result.region.region_rz == -1
    slot = result.region.slots[5]
    assert slot.flags & SLOT_FLAG_HAS_PAYLOAD
    assert decode_chunk_modification(slot.payload) == blob


def test_header_crc_failure() -> None:
    raw = bytearray(encode_region_file(_empty_region()))
    raw[20] ^= 0xFF
    result = decode_region_file(bytes(raw))
    assert result.region is None
    assert result.error == "header crc mismatch"


def test_payload_crc_failure() -> None:
    region = _empty_region()
    slots = list(region.slots)
    payload = encode_chunk_modification(
        ChunkModificationBlob(tile_overrides=(TileOverrideRecord(0, 1, 2, KEY_STONE),))
    )
    slots[1] = SlotEntry(
        flags=SLOT_FLAG_DISCOVERED | SLOT_FLAG_MODIFIED | SLOT_FLAG_HAS_PAYLOAD,
        payload=payload,
    )
    raw = bytearray(encode_region_file(RegionFile(0, 0, tuple(slots))))
    raw[-10] ^= 0xFF
    result = decode_region_file(bytes(raw))
    assert result.region is None
    assert result.error == "payload crc mismatch"


def test_negative_region_coordinates() -> None:
    cx, cz = -9, 3
    rx, rz, slot_cx, slot_cz, slot_index = chunk_to_region(cx, cz)
    region = _empty_region(rx=rx, rz=rz)
    slots = list(region.slots)
    slots[slot_index] = SlotEntry(flags=SLOT_FLAG_DISCOVERED)
    region = RegionFile(region_rx=rx, region_rz=rz, slots=tuple(slots))
    result = decode_region_file(encode_region_file(region))
    assert result.region is not None
    assert result.region.region_rx == rx
    assert result.region.region_rz == rz
    assert result.region.slots[slot_index].flags == SLOT_FLAG_DISCOVERED
    assert slot_cx == (-9) - rx * REGION_CHUNKS
    assert NO_PAYLOAD_OFFSET == 0xFFFFFFFF
