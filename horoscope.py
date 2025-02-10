from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from cloud_connect import HoroscopeService

horoscope_routes = APIRouter()
client = HoroscopeService()



@horoscope_routes.get("/horoscope")
async def get_horoscope(birthdate: str = Query(..., description="Birthdate in YYYY-MM-DD format")):
    """Fetch horoscope details for a given birthdate."""
    try:
        datetime.strptime(birthdate, "%Y-%m-%d")  # Validate format
        response = client.get_horoscope(birthdate)
        return {"horoscope": response}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@horoscope_routes.get("/astrology-matches")
async def get_astrology_matches(birthdate: str = Query(..., description="Birthdate in YYYY-MM-DD format")):
    """Fetch famous people who share the same astrology profile."""
    try:
        datetime.strptime(birthdate, "%Y-%m-%d")  # Validate format
        response = client.get_astrology_matches(birthdate)
        return {"astrology_matches": response}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


    