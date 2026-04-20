## Summary

- What changed?
- Why now?

## Verification

- [ ] `python -m pytest`
- [ ] `python scripts/run_smoke.py`
- [ ] `python scripts/run_ecology_probe.py` if ecology behavior changed

## Ecology Guard

- [ ] This change helps the ecology-first north star more than it increases
      mechanism complexity
- [ ] The intended effect is observable in runs, events, or summaries
- [ ] I am not relying on hidden handholding or scripted rescue behavior
- [ ] The claims in this PR are supported by the current evidence

## Notes

- Anything a reviewer should inspect first?
