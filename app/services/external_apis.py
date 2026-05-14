"""
HTTP client service for making async API requests.
Provides retry logic, timeouts, and error handling.
"""

import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.config.settings import get_settings
from app.core.exceptions import APIError, TimeoutError


logger = logging.getLogger("app")


class HTTPClientService:
    """Service for making HTTP requests with built-in error handling and retries."""
    
    def __init__(self):
        self.settings = get_settings()
        self._client: Optional[httpx.AsyncClient] = None
        self._retry_count = 3
        self._retry_delay = 1
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=self.settings.http_timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        api_name: str = "external-api",
    ) -> Dict[str, Any]:
        """
        Make async GET request with retries.
        
        Args:
            url: URL to request
            headers: Request headers
            params: Query parameters
            api_name: Name of API for logging
        
        Returns:
            Response JSON as dictionary
        
        Raises:
            APIError: If request fails
            TimeoutError: If request times out
        """
        if not self._client:
            raise RuntimeError("HTTPClientService not initialized. Use 'async with' context manager.")
        
        for attempt in range(self._retry_count):
            try:
                response = await self._client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self.settings.http_timeout,
                )
                
                if response.status_code >= 400:
                    logger.error(
                        f"API request failed: {api_name}",
                        extra={
                            "extra_data": {
                                "url": url,
                                "status_code": response.status_code,
                                "response": response.text[:500],
                            }
                        },
                    )
                    raise APIError(
                        message=f"API request failed with status {response.status_code}",
                        api_name=api_name,
                        status_code=response.status_code,
                    )
                
                logger.info(f"API request succeeded: {api_name}")
                return response.json()
            
            except httpx.TimeoutException as e:
                logger.error(f"API request timeout: {api_name} (attempt {attempt + 1})")
                if attempt == self._retry_count - 1:
                    raise TimeoutError(
                        operation=f"API request to {api_name}",
                        timeout_seconds=self.settings.http_timeout,
                    )
            
            except httpx.RequestError as e:
                logger.error(
                    f"API request error: {api_name} (attempt {attempt + 1})",
                    extra={"extra_data": {"error": str(e)}}
                )
                if attempt == self._retry_count - 1:
                    raise APIError(
                        message=f"API request failed: {str(e)}",
                        api_name=api_name,
                    )
            
            except Exception as e:
                if attempt == self._retry_count - 1:
                    raise
                logger.warning(f"Retrying API request for {api_name}")
            
            if attempt < self._retry_count - 1:
                import asyncio
                await asyncio.sleep(self._retry_delay * (attempt + 1))
    
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        api_name: str = "external-api",
    ) -> Dict[str, Any]:
        """Make async POST request."""
        if not self._client:
            raise RuntimeError("HTTPClientService not initialized. Use 'async with' context manager.")
        
        try:
            response = await self._client.post(
                url,
                json=data,
                headers=headers,
                timeout=self.settings.http_timeout,
            )
            
            if response.status_code >= 400:
                raise APIError(
                    message=f"API request failed with status {response.status_code}",
                    api_name=api_name,
                    status_code=response.status_code,
                )
            
            return response.json()
        
        except httpx.TimeoutException:
            raise TimeoutError(
                operation=f"API request to {api_name}",
                timeout_seconds=self.settings.http_timeout,
            )
        except Exception as e:
            raise APIError(message=str(e), api_name=api_name)


class WeatherService:
    """Service for weather operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_base = "https://api.openweathermap.org/data/2.5/weather"
    
    async def get_weather(self, city: str, unit: str = "metric") -> Dict[str, Any]:
        """
        Fetch weather for a city.
        
        Args:
            city: City name
            unit: Temperature unit (metric, imperial, kelvin)
        
        Returns:
            Weather data dictionary
        """
        if not self.settings.weather_api_key:
            logger.warning("Weather API key not configured")
            return self._get_fallback_weather(city)
        
        async with HTTPClientService() as http_client:
            try:
                data = await http_client.get(
                    self.api_base,
                    params={
                        "q": city,
                        "units": unit,
                        "appid": self.settings.weather_api_key,
                    },
                    api_name="openweathermap",
                )
                
                return {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "cloudiness": data["clouds"]["all"],
                }
            except Exception as e:
                logger.error(f"Weather service error: {str(e)}")
                return self._get_fallback_weather(city)
    
    def _get_fallback_weather(self, city: str) -> Dict[str, Any]:
        """Get fallback weather data."""
        return {
            "city": city,
            "country": "Unknown",
            "temperature": 20.0,
            "feels_like": 20.0,
            "humidity": 65,
            "pressure": 1013,
            "description": "Fallback: API key not configured",
            "wind_speed": 5.0,
            "cloudiness": 50,
        }


class GitHubService:
    """Service for GitHub operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_base = "https://api.github.com"
    
    async def get_user(self, username: str, include_repos: bool = True) -> Dict[str, Any]:
        """
        Fetch GitHub user information.
        
        Args:
            username: GitHub username
            include_repos: Whether to include repositories
        
        Returns:
            User data dictionary
        """
        headers = {}
        if self.settings.github_token:
            headers["Authorization"] = f"token {self.settings.github_token}"
        
        async with HTTPClientService() as http_client:
            # Fetch user data
            user_data = await http_client.get(
                f"{self.api_base}/users/{username}",
                headers=headers,
                api_name="github",
            )
            
            result = {
                "username": user_data["login"],
                "name": user_data.get("name"),
                "bio": user_data.get("bio"),
                "url": user_data["html_url"],
                "followers": user_data["followers"],
                "following": user_data["following"],
                "public_repos": user_data["public_repos"],
                "avatar_url": user_data["avatar_url"],
            }
            
            if include_repos:
                try:
                    repos_data = await http_client.get(
                        f"{self.api_base}/users/{username}/repos",
                        params={"sort": "stars", "per_page": 5},
                        headers=headers,
                        api_name="github",
                    )
                    
                    result["repositories"] = [
                        {
                            "name": repo["name"],
                            "url": repo["html_url"],
                            "description": repo.get("description"),
                            "stars": repo["stargazers_count"],
                            "language": repo.get("language"),
                            "is_fork": repo["fork"],
                        }
                        for repo in repos_data[:5]
                    ]
                except Exception as e:
                    logger.warning(f"Failed to fetch repositories: {str(e)}")
            
            return result


class OpenAIService:
    """Service for OpenAI operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_base = "https://api.openai.com/v1"
    
    async def summarize_text(self, text: str, max_length: int = 100) -> Optional[str]:
        """
        Summarize text using OpenAI API.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
        
        Returns:
            Summary text or None if API key not configured
        """
        if not self.settings.openai_api_key:
            logger.warning("OpenAI API key not configured, using fallback")
            return self._local_summarize(text, max_length)
        
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}
        
        async with HTTPClientService() as http_client:
            try:
                response = await http_client.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    data={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a helpful assistant that summarizes text concisely.",
                            },
                            {
                                "role": "user",
                                "content": f"Summarize this text in {max_length} characters or less:\n\n{text}",
                            },
                        ],
                        "max_tokens": max_length,
                        "temperature": 0.5,
                    },
                    api_name="openai",
                )
                
                return response["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenAI summarization failed: {str(e)}")
                return self._local_summarize(text, max_length)
    
    def _local_summarize(self, text: str, max_length: int) -> str:
        """Local text summarization using simple heuristics."""
        sentences = text.replace(".", ".\n").split("\n")
        summary = ""
        
        for sentence in sentences:
            if len(summary) + len(sentence) <= max_length:
                summary += sentence.strip() + " "
            else:
                break
        
        return summary.strip() or text[:max_length]
