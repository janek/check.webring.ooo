import argparse
import asyncio
import csv
import re
import time
from datetime import timedelta
from pathlib import Path

from app import is_domain_available
from redis_client import get_redis

DOMAIN_RE = re.compile(r"^[a-z0-9-]+\.ooo$")


async def load_domains_from_csv(csv_path: Path, limit: int | None = None) -> list[str]:
    """Return a list of .ooo domains extracted from *csv_path*.

    The CSV can contain either a "name" column (which will be converted to
    "<name>.ooo") or a "domain" column that already contains the full domain.
    Non-ASCII or otherwise invalid domain labels are filtered out.
    """

    domains: list[str] = []

    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Determine which column to use once, outside the loop
        field_choice: str | None = None
        if "domain" in reader.fieldnames:  # type: ignore[arg-type]
            field_choice = "domain"
        elif "name" in reader.fieldnames:  # type: ignore[arg-type]
            field_choice = "name"
        else:
            raise ValueError(
                f"CSV {csv_path} must contain a 'name' or 'domain' column; found {reader.fieldnames}"
            )

        for row in reader:
            raw = row[field_choice].strip()  # type: ignore[index]

            if field_choice == "name":
                # Only ASCII names that make valid domains when stripped
                if not raw.isascii():
                    continue
                cleaned = raw.replace(" ", "").replace("-", "").replace("'", "")
                if not cleaned.isalnum():
                    continue
                domain = f"{raw.lower()}.ooo"
            else:
                # Already a full domain
                domain = raw.lower()

            # Basic validation – must match our pattern
            if not DOMAIN_RE.fullmatch(domain):
                continue

            domains.append(domain)
            if limit and len(domains) >= limit:
                break
    return domains


async def refresh_ooo_cache(
    *,
    csv_path: Path = Path("data/default_names.csv"),
    skip_cached: bool = False,
    limit: int | None = None,
):
    """Refresh .ooo domain availability cache using *csv_path* as the data source."""

    redis = await get_redis()

    if not csv_path.exists():
        print(f"❌ {csv_path} not found. Provide a valid CSV path (see --csv).")
        return

    # Load domains from CSV
    try:
        domains = await load_domains_from_csv(csv_path, limit=limit)
    except Exception as e:
        print(f"❌ Failed loading CSV: {e}")
        return

    limit_text = f" (limited to {limit})" if limit else ""
    print(
        f"🔄 Checking {len(domains)} .ooo domains{' (skipping cached)' if skip_cached else ''}{limit_text}..."
    )

    start_time = time.time()
    skipped_count = 0

    for i, domain in enumerate(domains):
        try:
            # Skip if already cached
            if skip_cached:
                cached = await redis.get(domain)
                if cached is not None:
                    skipped_count += 1
                    continue

            available = await is_domain_available(domain)
            # Cache policy: 7 days for both available and taken domains
            ttl = int(timedelta(days=7).total_seconds())

            await redis.set(domain, "free" if available else "taken", ex=ttl)

            if (i + 1) % 100 == 0 or i == len(domains) - 1:
                elapsed = time.time() - start_time
                checked = (i + 1) - skipped_count
                rate = checked / elapsed if elapsed > 0 else 0
                remaining = len(domains) - i - 1
                eta = remaining / rate if rate > 0 else 0
                print(
                    f"  {i + 1}/{len(domains)} processed, {checked} checked, {skipped_count} skipped ({rate:.1f}/s, ETA: {eta / 60:.1f}m)"
                )

            # Rate limiting to be nice to DNS servers
            await asyncio.sleep(0.1)

        except Exception as e:
            print(f"  ⚠️  Error checking {domain}: {e}")
            continue

    elapsed = time.time() - start_time
    checked_count = len(domains) - skipped_count
    print(f"✅ Cache refresh complete in {elapsed / 60:.1f} minutes")
    print(f"   Checked: {checked_count}, Skipped: {skipped_count}")
    if checked_count > 0:
        print(f"   Average rate: {checked_count / elapsed:.1f} domains/second")


async def main():
    parser = argparse.ArgumentParser(
        description="Refresh .ooo domain availability cache"
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("data/default_names.csv"),
        help="Path to CSV file with either a 'name' column or a 'domain' column",
    )
    parser.add_argument(
        "--skip-cached",
        action="store_true",
        help="Skip domains that are already cached in Redis",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit the number of domains to check",
    )
    args = parser.parse_args()

    try:
        await refresh_ooo_cache(
            csv_path=args.csv, skip_cached=args.skip_cached, limit=args.limit
        )
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up Redis connection
        from redis_client import close_redis

        await close_redis()


if __name__ == "__main__":
    asyncio.run(main())
