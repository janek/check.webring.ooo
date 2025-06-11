import asyncio
import random
import socket
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, Query

# External library (large dataset)
from names_dataset import NameDataset

from redis_client import close_redis, get_redis

# ---------------------------------------------------------------------------
# Lifespan handler for startup/shutdown
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: nothing for now (lazy initialisation elsewhere)
    yield
    # Shutdown
    await close_redis()


app = FastAPI(lifespan=lifespan)

# ---------------------------------------------------------------------------
# NameDataset initialisation (heavy) – done once at startup
# ---------------------------------------------------------------------------

# Lazy singleton so reloads do not re-initialise needlessly
_ND: NameDataset | None = None


def get_dataset() -> NameDataset:
    """Initialise NameDataset once and cache it."""
    global _ND
    if _ND is None:
        _ND = NameDataset()  # type: ignore
    return _ND


# Utility to flatten the nested dict from get_top_names into a list
def flatten_top_names(
    top_names: dict[str, dict[str, list[str]]], limit: int
) -> list[str]:
    collected: set[str] = set()
    # the dict structure is country -> gender -> [names]
    for gender_map in top_names.values():
        for names in gender_map.values():
            for name in names:
                if len(collected) >= limit:
                    return list(collected)
                collected.add(name)
    return list(collected)


@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}


@app.get("/names")
async def get_names(
    count: int = Query(
        30, ge=1, le=10000, description="Number of popular names to return"
    ),
):
    """Return a flat list of popular first names sampled from NameDataset."""
    dataset = get_dataset()
    # Request a bit more than needed in case of duplicates
    fetch_n = min(max(count * 3, 100), 5000)
    top_dict = dataset.get_top_names(n=fetch_n, use_first_names=True)
    flat_names = flatten_top_names(top_dict, limit=count * 2)

    # Finally sample down to requested count (random to add variety)
    if len(flat_names) > count:
        flat_names = random.sample(flat_names, count)

    return {"names": flat_names, "returned": len(flat_names)}


# ---------------------------------------------------------------------------
# Domain availability checker
# ---------------------------------------------------------------------------


async def is_domain_available(domain: str) -> bool:
    """Return True if the domain does NOT resolve (naive availability check)."""
    loop = asyncio.get_running_loop()
    try:
        # getaddrinfo returns at least one record if DNS resolves
        await loop.getaddrinfo(domain, None)
        return False  # resolves → taken
    except socket.gaierror:
        return True  # DNS failed → likely available


# ---------------------------------------------------------------------------
# Endpoint: /check/{domain}
# ---------------------------------------------------------------------------


@app.get("/check/{domain}")
async def check_domain(domain: str, redis=Depends(get_redis)):
    # Normalise
    domain_lower = domain.lower()

    # Quick sanity: must contain a dot
    if "." not in domain_lower:
        raise HTTPException(status_code=400, detail="invalid domain")

    cached = await redis.get(domain_lower)
    if cached is not None:
        return {
            "domain": domain_lower,
            "available": cached == "free",
            "cached": True,
        }

    available = await is_domain_available(domain_lower)

    # Cache policy: available domains checked more frequently
    ttl = (
        int(timedelta(hours=1).total_seconds())
        if available
        else int(timedelta(days=7).total_seconds())
    )
    await redis.set(domain_lower, "free" if available else "taken", ex=ttl)

    return {"domain": domain_lower, "available": available, "cached": False}
