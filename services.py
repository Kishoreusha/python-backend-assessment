import httpx
from core.logging_config import logger

async def fetch_repo(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
    except httpx.RequestError:
        logger.error("GitHub API unreachable")
        raise ValueError("External service unavailable")

    if response.status_code != 200:
        raise ValueError("GitHub repository not found")

    return response.json()