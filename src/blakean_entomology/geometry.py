"""Group original source coordinates before calling the shared support methods."""

from collections import defaultdict
from fractions import Fraction
from typing import Final

from blake.methods.intervals import (
    Interval,
    interval_intersection,
    interval_measure,
)
from blake.methods.runs import digest
from blake.studies import StudyHit, StudySpec
from blake.text_search.models import Passage

from .composition import CHANNELS
from .composition import ChannelName as Channel
from .geometry_inputs import validate_geometry_inputs
from .geometry_models import (
    ChannelGeometry,
    ChannelIntersection,
    CohortGeometry,
    DocumentedWindow,
    GeometryReport,
    HitLocation,
    SourceGeometry,
    SpanMeasure,
    WindowLocation,
)
from .models import ReviewDecision

PRIMARY: Final = ("primary", "reading", "william-blake-1757-1827")
CHANNEL_ORDER: Final[tuple[Channel, ...]] = ("name_family", "broad_label", "associated", "motion")


def sum_measures(measures: tuple[SpanMeasure, ...]) -> SpanMeasure:
    """Add already source-local measures; offsets never cross source frames."""
    return SpanMeasure(
        records=sum(m.records for m in measures),
        summed_codepoints=sum(m.summed_codepoints for m in measures),
        union_codepoints=sum(m.union_codepoints for m in measures),
        overlap_codepoints=sum(m.overlap_codepoints for m in measures),
        overlapping_pairs=sum(m.overlapping_pairs for m in measures),
        source_components=sum(m.source_components for m in measures),
    )


def cohort_geometry(
    sources: tuple[SourceGeometry, ...], facets: tuple[str, str, str]
) -> CohortGeometry:
    """Keep zero-hit units in the declared unit/recorded-work weighting policy."""
    lengths = sum(s.codepoints for s in sources)
    work: defaultdict[str, list[Fraction]] = defaultdict(list)
    for source in sources:
        work[source.work_id].append(Fraction(source.measure.union_codepoints, source.codepoints))
    ratios = tuple(value for values in work.values() for value in values)
    measure = sum_measures(tuple(s.measure for s in sources))
    return CohortGeometry(
        role=facets[0],
        plane=facets[1],
        author_id=facets[2],
        source_units=len(sources),
        work_groups=len(work),
        codepoints=lengths,
        measure=measure,
        pooled_occupancy=float(Fraction(measure.union_codepoints, lengths)) if lengths else None,
        equal_unit_occupancy=float(sum(ratios, Fraction()) / len(ratios)) if ratios else None,
        equal_work_occupancy=float(
            sum((sum(v, Fraction()) / len(v) for v in work.values()), Fraction()) / len(work)
        )
        if work
        else None,
    )


def _source_geometry(
    passage: Passage,
    hits: tuple[StudyHit, ...],
    decisions: tuple[ReviewDecision, ...],
    windows: tuple[DocumentedWindow, ...],
) -> SourceGeometry:
    labels = {d.hit_id: d.decision for d in decisions}
    locations = tuple(
        HitLocation(
            hit_id=h.hit_id,
            term_id=h.term_id,
            channel=CHANNELS[h.group],
            interval=Interval(start=h.start, end=h.end),
            decision=labels.get(h.hit_id),
        )
        for h in hits
    )
    spans = tuple(h.interval for h in locations)
    read_ids = {w.hit.hit_id for w in windows}
    selected = tuple(h.interval for h in locations if h.decision is not None)
    unselected = tuple(h.interval for h in locations if h.decision is None)
    reading = tuple(
        WindowLocation(
            batch_id=w.batch_id,
            hit_id=w.hit.hit_id,
            interval=Interval(start=w.window_start, end=w.window_end),
        )
        for w in windows
    )
    return SourceGeometry(
        passage_id=passage.passage_id,
        work_id=passage.work_id,
        title=passage.title,
        role=passage.text_role,
        plane=passage.source_plane,
        author_id=passage.author_id,
        text_sha256=digest(passage.text.encode()),
        codepoints=len(passage.text),
        measure=SpanMeasure.from_intervals(spans),
        reviewed_hits=len(selected),
        reviewed_union_codepoints=interval_measure(selected),
        unreviewed_union_codepoints=interval_measure(unselected),
        documented_window_events=len(windows),
        documented_window_codepoints=interval_measure(tuple(w.interval for w in reading))
        if windows
        else None,
        reviewed_without_documented_window=sum(
            h.decision is not None and h.hit_id not in read_ids for h in locations
        ),
        hits=locations,
        windows=reading,
    )


def analyze_geometry(
    passages: tuple[Passage, ...],
    hits: tuple[StudyHit, ...],
    decisions: tuple[ReviewDecision, ...],
    windows: tuple[DocumentedWindow, ...],
    spec: StudySpec,
    *,
    run_sha256: str,
    illustrative_source_ids: tuple[str, ...] = (),
    window_pairs: tuple[tuple[str, str], ...] = (),
) -> GeometryReport:
    """Describe one exact candidate/review run without rematching or adding judgments."""
    by_source = validate_geometry_inputs(passages, hits, decisions, windows, spec, run_sha256)
    grouped_hits: defaultdict[str, list[StudyHit]] = defaultdict(list)
    grouped_windows: defaultdict[str, list[DocumentedWindow]] = defaultdict(list)
    for hit in hits:
        grouped_hits[hit.passage_id].append(hit)
    for window in windows:
        grouped_windows[window.hit.passage_id].append(window)
    sources = tuple(
        _source_geometry(
            by_source[key],
            tuple(sorted(grouped_hits[key], key=lambda h: (h.start, h.end, h.hit_id))),
            decisions,
            tuple(sorted(grouped_windows[key], key=lambda w: w.batch_id)),
        )
        for key in sorted(by_source)
    )
    cohorts: defaultdict[tuple[str, str, str], list[SourceGeometry]] = defaultdict(list)
    primary_spans: defaultdict[Channel, list[tuple[Interval, ...]]] = defaultdict(list)
    intersections: defaultdict[tuple[Channel, Channel], int] = defaultdict(int)
    for source in sources:
        key = (source.role, source.plane, source.author_id)
        cohorts[key].append(source)
        if key == PRIMARY:
            local: dict[Channel, tuple[Interval, ...]] = {
                channel: tuple(h.interval for h in source.hits if h.channel == channel)
                for channel in CHANNEL_ORDER
            }
            for channel, spans in local.items():
                primary_spans[channel].append(spans)
                for other in CHANNEL_ORDER:
                    intersections[channel, other] += interval_measure(
                        interval_intersection(spans, local[other])
                    )
    return GeometryReport(
        run_sha256=run_sha256,
        candidate_hits=len(hits),
        reviewed_hits=len(decisions),
        unreviewed_hits=len(hits) - len(decisions),
        documented_window_events=len(windows),
        illustrative_source_ids=illustrative_source_ids,
        window_pairs=window_pairs,
        sources=sources,
        cohorts=tuple(cohort_geometry(tuple(items), key) for key, items in sorted(cohorts.items())),
        primary=cohort_geometry(tuple(cohorts[PRIMARY]), PRIMARY),
        primary_channels=tuple(
            ChannelGeometry(
                channel=channel,
                measure=sum_measures(
                    tuple(SpanMeasure.from_intervals(records) for records in primary_spans[channel])
                ),
            )
            for channel in CHANNEL_ORDER
        ),
        channel_intersections=tuple(
            ChannelIntersection(left=a, right=b, codepoints=intersections[a, b])
            for a in CHANNEL_ORDER
            for b in CHANNEL_ORDER
        ),
    )
