# ADR-003: Names Dataset Integration

## Status

**DRAFT** - Under evaluation and testing

## Context

For check.webring.ooo, we need a comprehensive source of first names to check against `.ooo` domain availability. Initial approach was a simple CSV with ~100 sample names, but this doesn't scale for a useful webring tool.

Requirements:

- Large dataset of real first names (10k+ entries)
- Support for search, autocomplete, and fuzzy matching
- Rich metadata (popularity, demographics) for enhanced UX
- Ability to subset data for performance (mobile-friendly)

## Decision

Integrate the `names-dataset` Python library as our primary name data source.

**Library Details:**

- 727,556 first names from 491M+ real person records
- 106 countries represented with popularity rankings
- Built-in search, autocomplete, and metadata APIs
- Country and gender probability data
- Based on comprehensive real-world dataset

## Rationale

### Advantages

- **Scale**: 727k names vs our 100 sample names
- **Quality**: Real names from actual people, not synthetic data
- **Rich metadata**: Country probabilities, gender, popularity rankings
- **Built-in functionality**: Auto-complete, search, metadata queries
- **Performance options**: Can extract subsets (top 10k names) for speed
- **Maintenance-free**: No need to curate/update name lists ourselves
- **International scope**: Matches the global nature of `.ooo` domains

### Disadvantages

- **Size**: 3.2GB RAM requirement for full dataset loading
- **Complexity**: Additional dependency vs simple CSV approach
- **Privacy concerns**: Based on Facebook leak data (though names aren't copyrightable)
- **Overkill**: May be overengineering for a simple domain checker

## Implementation Plan

1. **Phase 1**: Replace CSV with top 10k most popular names from dataset
2. **Phase 2**: Add autocomplete API endpoint using `dataset.auto_complete()`
3. **Phase 3**: Implement rich search with metadata display
4. **Phase 4**: Evaluate full dataset loading vs subset approach based on usage

## API Integration

- `dataset.get_top_names(n=10000)` for initial data subset
- `dataset.auto_complete(query, n=10)` for search suggestions
- `dataset.search(name)` for detailed name metadata
- Consider `dataset.fuzzy_search()` if fuzzywuzzy dependency is acceptable

## Performance Considerations

- **Memory**: Monitor RAM usage with full dataset vs subset approach
- **Loading time**: ~3.2GB initial load - consider caching strategies
- **Response time**: Test performance of library methods under load
- **Mobile impact**: Ensure API responses remain lightweight

## Security & Privacy

- Dataset derived from Facebook leak but contains only publicly available names
- No personal information beyond name demographics
- Names themselves are not copyrightable
- Consider data source transparency in documentation

## Alternatives Considered

1. **Maintain simple CSV**: Simple but limited scale and functionality
2. **Use multiple name APIs**: Complex integration, potential rate limits
3. **Build custom dataset**: High maintenance overhead
4. **Wikipedia/Census data**: Limited international coverage

## Success Metrics

- API response times < 200ms for autocomplete
- Support for international name variations
- User engagement with rich metadata features
- System performance within acceptable memory bounds

---

_This ADR was generated with AI assistance as part of rapid prototyping and architectural exploration._
