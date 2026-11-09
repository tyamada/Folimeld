"""Summarize the three fresh-process runs in this evidence directory."""
import json
from pathlib import Path
from statistics import median


root = Path(__file__).resolve().parent
summary = {}
for case in ("text-100", "images-100", "text-1000"):
    reports = [json.loads((root / f"{case}-{run}.json").read_text(encoding="utf-8"))
               for run in (1, 2, 3)]
    assert all(report["input_unchanged"] and report["undo_performed"]
               and report["redo_performed"] for report in reports)
    metrics = {}
    for name in ("open", "initial_thumbnails", "save", "max_thumbnail_batch_ms", "rss_mib"):
        if name == "rss_mib":
            values = [report["sampled_peak_rss_bytes"] / 1024 ** 2 for report in reports]
        elif name == "max_thumbnail_batch_ms":
            values = [report[name] for report in reports]
        else:
            values = [report["milliseconds"][name] for report in reports]
        metrics[name] = {"median": round(median(values), 3),
                         "min": round(min(values), 3), "max": round(max(values), 3)}
    summary[case] = {"runs": 3, "metrics": metrics,
                     "max_resident_thumbnails": max(report["peak_resident_thumbnails"]
                                                    for report in reports)}
print(json.dumps(summary, indent=2))
