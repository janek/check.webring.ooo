import argparse
import asyncio
import csv
from datetime import datetime
from pathlib import Path

from redis_client import close_redis, get_redis


async def export_cache_to_csv(output_path=None):
    """Export Redis domain cache to CSV file."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        output_path = f"data/cached_domains_{timestamp}.csv"

    redis = await get_redis()

    # Get all .ooo domain keys from Redis
    pattern = "*.ooo"
    keys = []
    cursor = 0

    # Use SCAN to iterate through keys (safer for large datasets)
    while True:
        cursor, batch_keys = await redis.scan(cursor, match=pattern, count=1000)
        keys.extend(
            [key.decode() if isinstance(key, bytes) else key for key in batch_keys]
        )
        if cursor == 0:
            break

    if not keys:
        print("❌ No .ooo domains found in cache")
        return

    print(f"🔍 Found {len(keys)} cached .ooo domains")

    # Fetch all values
    domains_data = []
    for key in keys:
        value = await redis.get(key)
        ttl = await redis.ttl(key)

        if value:
            status = value.decode() if isinstance(value, bytes) else value
            domains_data.append(
                {
                    "domain": key,
                    "status": status,
                    "ttl_seconds": ttl if ttl > 0 else "never_expires",
                }
            )

    # Sort by domain name
    domains_data.sort(key=lambda x: x["domain"])

    # Write to CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["domain", "status", "ttl_seconds"])
        writer.writeheader()
        writer.writerows(domains_data)

    # Stats
    available_count = sum(1 for d in domains_data if d["status"] == "free")
    taken_count = sum(1 for d in domains_data if d["status"] == "taken")

    print(f"✅ Exported {len(domains_data)} domains to {output_path}")
    print(f"   Available: {available_count}")
    print(f"   Taken: {taken_count}")


async def main():
    parser = argparse.ArgumentParser(description="Export Redis domain cache to CSV")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output CSV file path (default: data/cached_domains_YYYY-MM-DD-HH-MM.csv)",
    )
    args = parser.parse_args()

    try:
        await export_cache_to_csv(args.output)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await close_redis()


if __name__ == "__main__":
    asyncio.run(main())
