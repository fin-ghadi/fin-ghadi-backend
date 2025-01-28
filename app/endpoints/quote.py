from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from pydantic import BaseModel
from app.models.models import Quote
import random
router = APIRouter()

# Create Quote Endpoint
@router.post("/", response_model=Quote)
async def create_quote(quote: Quote):
    """
    Create a new quote.
    """
    # Insert the quote into the database
    await quote.insert()
    return quote

# Get All Quotes Endpoint
@router.get("/", response_model=list[Quote])
async def get_quotes():
    """
    Get a list of all quotes.
    """
    # make a check if the is any quote exidting in the database
    quotes = await Quote.find_all().to_list()
    if not quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quotes found",
        )

    return quotes

 


@router.get("/random_quote", response_model=Quote)
async def get_random_quote():
    """
    Get a random quote.
    """
    # Fetch all quotes from the database
    quotes = await Quote.find_all().to_list()
    
    if not quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quotes found",
        )
    
    # Select a random quote
    random_quote = random.choice(quotes)
    return random_quote


 
 
