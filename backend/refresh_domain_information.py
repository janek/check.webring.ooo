import argparse
import asyncio
import csv
import time
from datetime import timedelta
from pathlib import Path

from app import is_domain_available
from redis_client import get_redis


async def refresh_ooo_cache(skip_cached=False):
    """Refresh .ooo domain availability cache from default names CSV."""
    redis = await get_redis()
    csv_path = Path("data/default_names.csv")

    if not csv_path.exists():
        print(f"❌ {csv_path} not found. Run the notebook first to generate it.")
        return

    # Load names from CSV
    names = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            # Only ASCII names that make valid domains
            if (
                name.isascii()
                and name.replace(" ", "").replace("-", "").replace("'", "").isalnum()
            ):
                names.append(name)

    print(
        f"🔄 Checking {len(names)} .ooo domains{'(skipping cached)' if skip_cached else ''}..."
    )
    start_time = time.time()
    skipped_count = 0

    for i, name in enumerate(names):
        domain = f"{name.lower()}.ooo"

        try:
            # Skip if already cached
            if skip_cached:
                cached = await redis.get(domain)
                if cached is not None:
                    skipped_count += 1
                    continue

            available = await is_domain_available(domain)
            # Cache policy: available checked more often, taken cached longer
            ttl = (
                int(timedelta(hours=1).total_seconds())
                if available
                else int(timedelta(days=7).total_seconds())
            )

            await redis.set(domain, "free" if available else "taken", ex=ttl)

            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                checked = (i + 1) - skipped_count
                rate = checked / elapsed if elapsed > 0 else 0
                remaining = len(names) - i - 1
                eta = remaining / rate if rate > 0 else 0
                print(
                    f"  {i + 1}/{len(names)} processed, {checked} checked, {skipped_count} skipped ({rate:.1f}/s, ETA: {eta / 60:.1f}m)"
                )

            # Rate limiting to be nice to DNS servers
            await asyncio.sleep(0.1)

        except Exception as e:
            print(f"  ⚠️  Error checking {domain}: {e}")
            continue

    elapsed = time.time() - start_time
    checked_count = len(names) - skipped_count
    print(f"✅ Cache refresh complete in {elapsed / 60:.1f} minutes")
    print(f"   Checked: {checked_count}, Skipped: {skipped_count}")
    if checked_count > 0:
        print(f"   Average rate: {checked_count / elapsed:.1f} domains/second")


async def main():
    parser = argparse.ArgumentParser(
        description="Refresh .ooo domain availability cache"
    )
    parser.add_argument(
        "--skip-cached",
        action="store_true",
        help="Skip domains that are already cached in Redis",
    )
    args = parser.parse_args()

    try:
        await refresh_ooo_cache(skip_cached=args.skip_cached)
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
