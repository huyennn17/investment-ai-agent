from pydantic import BaseModel, Field

class PDFAnswer(BaseModel):
    answer: str = Field(description="The answer in full sentence to the question based on the PDF")
    source_pages: list[int] = Field(description="List of PDF page numbers used for the answer")
