import json
from pydantic import TypeAdapter

from langchain_ollama import ChatOllama

from src.entities import Theme
from src.services.rag.processor import process_document
from src.services.rag.store import create_documents


class ThemeGenerator:
    def __init__(self, document_path, bio_subject):
        self.bio_subject = bio_subject
        self.store = self.create_vector_store(document_path)
        self.query = f"""
            Collect anything that would be relevant to creating an
            autobiography or family history for {self.bio_subject}.
        """

    @staticmethod
    def create_vector_store(pdf_path):
        doc_chunks = process_document(pdf_path)
        vector_store = create_documents(documents=doc_chunks)

        return vector_store

    async def generate_themes(self):
        try:
            results = await self.store.asimilarity_search_with_relevance_scores(
                query=self.query,
                k=10,
            )

            formatted_results = "\n".join([
                f"Quote: {doc.page_content}\n"
                f"Source: {doc.metadata['source']}\n"
                f"Page: {doc.metadata['page']}\n"
                f"Relevance: {score}\n"
                for doc, score in results
            ])

            prompt = f'''
                Given the information below delimited by '```', please
                generate 3-5 themes/chapter ideas for the autobiography or
                family history of {self.bio_subject}.

                RESPONSE FORMAT:
                You must return a JSON array of themes. Each theme must contain:
                - title (string): A short, descriptive title
                - description (string): A brief explanation of the theme
                - confidence_score (float between 0 and 1)
                - supporting_snippets (array): Each snippet must contain:
                  - content (string): An exact quote from the source text
                  - source (string): The exact file path from the source content
                  - page (integer): The page number from the source content

                Example response structure:
                [
                    {{
                        "title": "Theme Title",
                        "description": "Theme description",
                        "confidence_score": 0.95,
                        "supporting_snippets": [
                            {{
                                "content": "Exact quote from text",
                                "source": "/path/to/source.pdf",
                                "page": 1
                            }}
                        ]
                    }}
                ]

                Remember: Only use EXACT quotes that appear in the text. Never generate or modify quotes.

                Source Content:
                ```
                {formatted_results}
                ```
            '''

            json_llm = ChatOllama(
                model="llama3.2",
                temperature=0,
                format="json",
            )
            messages = [("human", prompt)]
            json_string = json_llm.invoke(messages).content

            try:
                parsed_json = json.loads(json_string)
                themes_list = parsed_json if isinstance(parsed_json, list) else parsed_json.get("themes", [])
                theme_adapter = TypeAdapter(list[Theme])
                return theme_adapter.validate_python(themes_list)

            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON from LLM: {e}")
            except Exception as e:
                raise ValueError(f"Error processing LLM response: {e}")

        except Exception as e:
            raise ValueError(f"Error generating themes: {e}")
