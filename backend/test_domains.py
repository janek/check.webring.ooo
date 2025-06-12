import asyncio
import logging

from app import is_domain_available

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Test domains - mix of clearly taken and clearly available
TEST_DOMAINS = [
    # Clearly taken domains
    "webring.ooo",
    "janek.ooo",
    "google.com",
    "github.com",
    "stackoverflow.com",
    # Clearly NOT taken domains (random gibberish)
    "afjdjskacjakscnafksoa.ooo",
    "xyzqwerty123impossible.ooo",
    "thisdomainshouldnotexist999.ooo",
    "superlongdomainnamethatdoesnotexist.ooo",
    "randomtestdomain12345.ooo",
]


async def test_domain_availability():
    """Test domain availability checking with known taken/available domains."""
    logger.info("🧪 Starting domain availability test")

    results = []

    for domain in TEST_DOMAINS:
        try:
            logger.info(f"🔍 Checking domain: {domain}")

            # Check availability
            available = await is_domain_available(domain)
            status = "AVAILABLE" if available else "TAKEN"

            logger.info(f"  ✅ {domain} -> {status}")

            results.append({"domain": domain, "available": available, "status": status})

            # Small delay to be nice
            await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"  ❌ Error checking {domain}: {e}")
            results.append(
                {
                    "domain": domain,
                    "available": None,
                    "status": "ERROR",
                    "error": str(e),
                }
            )

    # Summary
    logger.info("\n📊 RESULTS SUMMARY:")
    logger.info("=" * 50)

    available_count = sum(1 for r in results if r["available"] is True)
    taken_count = sum(1 for r in results if r["available"] is False)
    error_count = sum(1 for r in results if r["available"] is None)

    for result in results:
        status_emoji = (
            "🟢"
            if result["available"]
            else "🔴"
            if result["available"] is False
            else "⚠️"
        )
        logger.info(f"{status_emoji} {result['domain']:<35} -> {result['status']}")

    logger.info("=" * 50)
    logger.info(f"Available: {available_count}")
    logger.info(f"Taken:     {taken_count}")
    logger.info(f"Errors:    {error_count}")
    logger.info(f"Total:     {len(results)}")

    # Sanity check
    if available_count == 0:
        logger.warning(
            "🚨 WARNING: No domains found as available - this suggests a problem!"
        )
    if taken_count == 0:
        logger.warning(
            "🚨 WARNING: No domains found as taken - this suggests a problem!"
        )

    return results


async def main():
    try:
        await test_domain_availability()
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
