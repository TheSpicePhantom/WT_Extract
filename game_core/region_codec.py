"""Binärer Region-/Chunk-Codec für Save v5 (M24)."""

from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass, field
from typing import Iterable

from game_core.world_coords import REGION_SLOT_COUNT

REGION_MAGIC = b"WTRE"
REGION_FILE_VERSION = 1
MANIFEST_MAGIC = b"WTW1"
SAVE_VERSION_V5 = 5
CODEC_VERSION_V1 = 1

SLOT_FLAG_DISCOVERED = 1 << 0
SLOT_FLAG_MODIFIED = 1 << 1
SLOT_FLAG_HAS_PAYLOAD = 1 << 2

NO_PAYLOAD_OFFSET = 0xFFFFFFFF

_REGION_HEADER_PREFIX = struct.Struct("<4sHHiib3x")
_SLOT_ENTRY = struct.Struct("<BBII")
_REGION_FOOTER = struct.Struct("<II")

_SECTION_TILE_OVERRIDES = 0x01
_SECTION_SUPPRESSIONS = 0x02

_TILE_OVERRIDE = struct.Struct("<BBHH I")
_SUPPRESSION = struct.Struct("<iiI")


@dataclass(slots=True)
class SlotEntry:
    flags: int = 0
    payload: bytes = b""


@dataclass(slots=True)
class TileOverrideRecord:
    layer: int
    local_tx: int
    local_tz: int
    tile_key: str


@dataclass(slots=True)
class SuppressionRecord:
    wx: int
    wz: int
    decoration_id: str


@dataclass(slots=True)
class ChunkModificationBlob:
    tile_overrides: tuple[TileOverrideRecord, ...] = ()
    suppressions: tuple[SuppressionRecord, ...] = ()


@dataclass(slots=True)
class RegionFile:
    region_rx: int
    region_rz: int
    slots: tuple[SlotEntry, ...] = field(
        default_factory=lambda: tuple(SlotEntry() for _ in range(REGION_SLOT_COUNT))
    )


def _crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def _encode_string_table(strings: Iterable[str]) -> tuple[bytes, dict[str, int]]:
    unique = list(dict.fromkeys(strings))
    table = b"\0".join(s.encode("utf-8") for s in unique) + b"\0"
    index = {s: i for i, s in enumerate(unique)}
    return table, index


def encode_chunk_modification(blob: ChunkModificationBlob) -> bytes:
    sections: list[bytes] = []
    if blob.tile_overrides:
        table, index = _encode_string_table(item.tile_key for item in blob.tile_overrides)
        body = bytearray()
        body.extend(struct.pack("<H", len(blob.tile_overrides)))
        for item in blob.tile_overrides:
            body.extend(
                _TILE_OVERRIDE.pack(
                    item.layer,
                    0,
                    item.local_tx,
                    item.local_tz,
                    index[item.tile_key],
                )
            )
        body.extend(table)
        sections.append(struct.pack("<BH", _SECTION_TILE_OVERRIDES, len(body)) + body)
    if blob.suppressions:
        table, index = _encode_string_table(item.decoration_id for item in blob.suppressions)
        body = bytearray()
        body.extend(struct.pack("<H", len(blob.suppressions)))
        for item in blob.suppressions:
            body.extend(_SUPPRESSION.pack(item.wx, item.wz, index[item.decoration_id]))
        body.extend(table)
        sections.append(struct.pack("<BH", _SECTION_SUPPRESSIONS, len(body)) + body)
    return b"".join(sections)


def decode_chunk_modification(data: bytes) -> ChunkModificationBlob:
    tile_overrides: list[TileOverrideRecord] = []
    suppressions: list[SuppressionRecord] = []
    offset = 0
    while offset + 3 <= len(data):
        section_id, length = struct.unpack_from("<BH", data, offset)
        offset += 3
        body = data[offset : offset + length]
        offset += length
        if section_id == _SECTION_TILE_OVERRIDES:
            (count,) = struct.unpack_from("<H", body, 0)
            pos = 2 + count * _TILE_OVERRIDE.size
            strings: list[str] = []
            while pos < len(body) and body[pos : pos + 1] != b"\0":
                end = body.index(b"\0", pos)
                strings.append(body[pos:end].decode("utf-8"))
                pos = end + 1
            pos = 2
            for _ in range(count):
                layer, _pad, local_tx, local_tz, sid = _TILE_OVERRIDE.unpack_from(body, pos)
                pos += _TILE_OVERRIDE.size
                tile_overrides.append(
                    TileOverrideRecord(
                        layer=layer,
                        local_tx=local_tx,
                        local_tz=local_tz,
                        tile_key=strings[sid],
                    )
                )
        elif section_id == _SECTION_SUPPRESSIONS:
            (count,) = struct.unpack_from("<H", body, 0)
            pos = 2 + count * _SUPPRESSION.size
            strings: list[str] = []
            while pos < len(body) and body[pos : pos + 1] != b"\0":
                end = body.index(b"\0", pos)
                strings.append(body[pos:end].decode("utf-8"))
                pos = end + 1
            pos = 2
            for _ in range(count):
                wx, wz, sid = _SUPPRESSION.unpack_from(body, pos)
                pos += _SUPPRESSION.size
                suppressions.append(
                    SuppressionRecord(wx=wx, wz=wz, decoration_id=strings[sid])
                )
    return ChunkModificationBlob(
        tile_overrides=tuple(tile_overrides),
        suppressions=tuple(suppressions),
    )


def encode_region_file(region: RegionFile) -> bytes:
    if len(region.slots) != REGION_SLOT_COUNT:
        raise ValueError(f"Region requires {REGION_SLOT_COUNT} slots")
    payload_parts: list[bytes] = []
    slot_bytes = bytearray()
    for slot in region.slots:
        if slot.payload:
            if not (slot.flags & SLOT_FLAG_HAS_PAYLOAD):
                raise ValueError("payload present but HAS_PAYLOAD flag missing")
            offset = sum(len(part) for part in payload_parts)
            payload_parts.append(slot.payload)
            slot_bytes.extend(
                _SLOT_ENTRY.pack(slot.flags, 0, offset, len(slot.payload))
            )
        elif slot.flags:
            slot_bytes.extend(_SLOT_ENTRY.pack(slot.flags, 0, NO_PAYLOAD_OFFSET, 0))
        else:
            slot_bytes.extend(_SLOT_ENTRY.pack(0, 0, NO_PAYLOAD_OFFSET, 0))
    payload_blob = b"".join(payload_parts)
    header_len = _REGION_HEADER_PREFIX.size + len(slot_bytes)
    header = bytearray()
    header.extend(
        _REGION_HEADER_PREFIX.pack(
            REGION_MAGIC,
            REGION_FILE_VERSION,
            header_len,
            region.region_rx,
            region.region_rz,
            REGION_SLOT_COUNT,
        )
    )
    header.extend(slot_bytes)
    payload_crc = _crc32(payload_blob)
    header_crc = _crc32(bytes(header))
    footer = _REGION_FOOTER.pack(payload_crc, header_crc)
    return bytes(header) + payload_blob + footer


@dataclass(frozen=True, slots=True)
class RegionDecodeResult:
    region: RegionFile | None
    error: str | None = None


def decode_region_file(data: bytes) -> RegionDecodeResult:
    min_size = _REGION_HEADER_PREFIX.size + REGION_SLOT_COUNT * _SLOT_ENTRY.size + _REGION_FOOTER.size
    if len(data) < min_size:
        return RegionDecodeResult(None, "region file too short")
    payload_crc, header_crc = _REGION_FOOTER.unpack_from(data, len(data) - _REGION_FOOTER.size)
    magic, version, header_len, rx, rz, slot_count = _REGION_HEADER_PREFIX.unpack_from(data, 0)
    if magic != REGION_MAGIC:
        return RegionDecodeResult(None, "bad region magic")
    if version != REGION_FILE_VERSION:
        return RegionDecodeResult(None, f"unsupported region version {version}")
    if slot_count != REGION_SLOT_COUNT:
        return RegionDecodeResult(None, "unexpected slot count")
    if header_len > len(data) - _REGION_FOOTER.size:
        return RegionDecodeResult(None, "invalid header length")
    header = data[:header_len]
    if _crc32(header) != header_crc:
        return RegionDecodeResult(None, "header crc mismatch")
    payload_blob = data[header_len : len(data) - _REGION_FOOTER.size]
    if _crc32(payload_blob) != payload_crc:
        return RegionDecodeResult(None, "payload crc mismatch")
    slots: list[SlotEntry] = []
    offset = _REGION_HEADER_PREFIX.size
    for _ in range(REGION_SLOT_COUNT):
        flags, _reserved, payload_offset, payload_length = _SLOT_ENTRY.unpack_from(header, offset)
        offset += _SLOT_ENTRY.size
        payload = b""
        if payload_offset != NO_PAYLOAD_OFFSET:
            payload = payload_blob[payload_offset : payload_offset + payload_length]
        slots.append(SlotEntry(flags=flags, payload=payload))
    return RegionDecodeResult(RegionFile(region_rx=rx, region_rz=rz, slots=tuple(slots)))
