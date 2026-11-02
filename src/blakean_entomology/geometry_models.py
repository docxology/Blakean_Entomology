"""Original-codepoint geometry, separate from contextual reading judgments."""

from typing import Annotated, ClassVar, Literal, Self

from blake.methods.installed_models import GitCommit
from blake.methods.intervals import (
    Interval,
    count_overlapping_pairs,
    interval_measure,
    interval_support_at_least,
    interval_union,
)
from blake.methods.models import Digest, EvidenceError
from blake.studies import StudyHit
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .composition import ChannelName as Channel
from .models import CorpusPin, Decision

Count = Annotated[int, Field(ge=0, strict=True)]


class GeometryModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True, extra="forbid", strict=True, revalidate_instances="always"
    )


class GeometryRequest(GeometryModel):
    schema_version: Literal[1] = 1
    corpus_pin: CorpusPin
    run_sha256: Digest
    decisions_sha256: Digest
    windows_sha256: Digest
    vocabulary_sha256: Digest
    sdk_commit: GitCommit | None = None
    illustrative_source_ids: tuple[str, ...] = Field(default=(), max_length=3)
    window_pairs: tuple[tuple[str, str], ...] = Field(default=(), max_length=2)
    coordinate_space: Literal["original Passage.text Python codepoints"] = (
        "original Passage.text Python codepoints"
    )


class DocumentedWindow(GeometryModel):
    batch_id: str = Field(min_length=1)
    hit: StudyHit
    window_start: Count
    window_end: Count
    window_sha256: Digest
    text: str = Field(min_length=1)

    @model_validator(mode="after")
    def extent(self) -> Self:
        if self.window_start >= self.window_end or len(self.text) != (
            self.window_end - self.window_start
        ):
            raise EvidenceError("geometry_window_extent", self.batch_id)
        return self


class SpanMeasure(GeometryModel):
    records: Count
    summed_codepoints: Count
    union_codepoints: Count
    overlap_codepoints: Count
    overlapping_pairs: Count
    source_components: Count

    @property
    def excess_codepoints(self) -> int:
        return self.summed_codepoints - self.union_codepoints

    @classmethod
    def from_intervals(cls, records: tuple[Interval, ...]) -> Self:
        """Measure a single original source frame through the public arithmetic."""
        components = interval_union(records)
        return cls(
            records=len(records),
            summed_codepoints=sum(s.end - s.start for s in records),
            union_codepoints=interval_measure(components),
            overlap_codepoints=interval_measure(interval_support_at_least(records)),
            overlapping_pairs=count_overlapping_pairs(records),
            source_components=len(components),
        )

    @model_validator(mode="after")
    def bounds(self) -> Self:
        if (
            self.union_codepoints > self.summed_codepoints
            or self.overlap_codepoints > self.union_codepoints
            or self.overlapping_pairs > self.records * (self.records - 1) // 2
            or self.source_components > self.records
        ):
            raise EvidenceError("geometry_measure_bounds", "Inconsistent support measures")
        return self


class HitLocation(GeometryModel):
    hit_id: Digest
    term_id: str
    channel: Channel
    interval: Interval
    decision: Decision | None


class WindowLocation(GeometryModel):
    batch_id: str
    hit_id: Digest
    interval: Interval


class SourceGeometry(GeometryModel):
    passage_id: str
    work_id: str
    title: str
    role: str
    plane: str
    author_id: str
    text_sha256: Digest
    codepoints: Annotated[int, Field(gt=0, strict=True)]
    measure: SpanMeasure
    reviewed_hits: Count
    reviewed_union_codepoints: Count
    unreviewed_union_codepoints: Count
    documented_window_events: Count
    documented_window_codepoints: Count | None
    reviewed_without_documented_window: Count
    hits: tuple[HitLocation, ...]
    windows: tuple[WindowLocation, ...]

    @model_validator(mode="after")
    def source_support(self) -> Self:
        hits = {h.hit_id: h for h in self.hits}
        selected = tuple(h.interval for h in self.hits if h.decision is not None)
        unselected = tuple(h.interval for h in self.hits if h.decision is None)
        known = {w.hit_id for w in self.windows}
        reading = tuple(w.interval for w in self.windows)
        if (
            len(hits) != len(self.hits)
            or any(
                s.start >= s.end or s.end > self.codepoints
                for s in (*reading, *(h.interval for h in self.hits))
            )
            or any(
                w.hit_id not in hits
                or hits[w.hit_id].decision is None
                or not w.interval.start
                <= hits[w.hit_id].interval.start
                < hits[w.hit_id].interval.end
                <= w.interval.end
                for w in self.windows
            )
            or self.measure != SpanMeasure.from_intervals(tuple(h.interval for h in self.hits))
            or self.reviewed_hits != len(selected)
            or self.reviewed_union_codepoints != interval_measure(selected)
            or self.unreviewed_union_codepoints != interval_measure(unselected)
            or self.documented_window_events != len(self.windows)
            or self.documented_window_codepoints != (interval_measure(reading) if reading else None)
            or self.reviewed_without_documented_window
            != sum(h.decision is not None and h.hit_id not in known for h in self.hits)
        ):
            raise EvidenceError("geometry_source_support", self.passage_id)
        return self


class CohortGeometry(GeometryModel):
    role: str
    plane: str
    author_id: str
    source_units: Count
    work_groups: Count
    codepoints: Count
    measure: SpanMeasure
    pooled_occupancy: Annotated[float, Field(ge=0, le=1)] | None
    equal_unit_occupancy: Annotated[float, Field(ge=0, le=1)] | None
    equal_work_occupancy: Annotated[float, Field(ge=0, le=1)] | None


class ChannelGeometry(GeometryModel):
    channel: Channel
    measure: SpanMeasure


class ChannelIntersection(GeometryModel):
    left: Channel
    right: Channel
    codepoints: Count


class GeometryReport(GeometryModel):
    schema_version: Literal[1] = 1
    coordinate_space: Literal["original Passage.text Python codepoints"] = (
        "original Passage.text Python codepoints"
    )
    run_sha256: Digest
    candidate_hits: Count
    reviewed_hits: Count
    unreviewed_hits: Count
    documented_window_events: Count
    sources: tuple[SourceGeometry, ...]
    cohorts: tuple[CohortGeometry, ...]
    primary: CohortGeometry
    primary_channels: tuple[ChannelGeometry, ...]
    channel_intersections: tuple[ChannelIntersection, ...]
    illustrative_source_ids: tuple[str, ...] = ()
    window_pairs: tuple[tuple[str, str], ...] = ()
    scope: str = (
        "Declared match support and documented reading-window subtotal, retaining source "
        "copies and zero-hit units. Missing window custody is unavailable, never zero "
        "reading. Geometry creates no decisions, animal census or independent scenes."
    )

    @model_validator(mode="after")
    def reconcile(self) -> Self:
        if (
            not self.sources
            or len({s.passage_id for s in self.sources}) != len(self.sources)
            or self.candidate_hits != sum(s.measure.records for s in self.sources)
            or self.reviewed_hits != sum(s.reviewed_hits for s in self.sources)
            or self.reviewed_hits + self.unreviewed_hits != self.candidate_hits
            or self.documented_window_events
            != sum(s.documented_window_events for s in self.sources)
            or sum(c.source_units for c in self.cohorts) != len(self.sources)
        ):
            raise EvidenceError("geometry_report_membership", self.run_sha256)
        windows = {w.batch_id: source.passage_id for source in self.sources for w in source.windows}
        if (
            len(set(self.illustrative_source_ids)) != len(self.illustrative_source_ids)
            or not set(self.illustrative_source_ids).issubset(s.passage_id for s in self.sources)
            or len(set(self.window_pairs)) != len(self.window_pairs)
            or any(
                a == b or a not in windows or b not in windows or windows[a] != windows[b]
                for a, b in self.window_pairs
            )
        ):
            raise EvidenceError(
                "geometry_figure_selection", "Require declared same-source witnesses"
            )
        return self
