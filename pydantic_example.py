from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from pydantic import BaseModel

load_dotenv()


# 1. Define schema for Marvel Movie data
class MarvelMovie(BaseModel):
    title: str
    release_year: int
    main_villain: str
    hero_characters: list[str]


parser = PydanticOutputParser(pydantic_object=MarvelMovie)

# 2. Setup Model
llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-7B-Instruct")
model = ChatHuggingFace(llm=llm)

# 3. Prompt + Run
prompt = f"Extract Marvel movie info from: 'Avengers: Endgame came out in 2019 where Earth's heroes like Iron Man, Captain America, and Thor team up to fight Thanos'.\n{parser.get_format_instructions()}"

response = model.invoke(prompt)
result: MarvelMovie = parser.parse(response.content)

# 4. Use your clean Python object!
print(f"Movie: {result.title} ({result.release_year})")
print(f"Villain: {result.main_villain}")
print(f"Heroes: {', '.join(result.hero_characters)}")