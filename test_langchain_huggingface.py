import os
import json
import time
import streamlit as st
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
from jsonformer.main import Jsonformer

load_dotenv()


class HuggingFaceLLM:
    def __init__(self, temperature=0, top_k=50, model_name="databricks/dolly-v2-12b"):
        self.model = AutoModelForCausalLM.from_pretrained(model_name, use_cache=True, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, use_cache=True)
        self.top_k = top_k

    def generate(self, prompt, max_length=1024):
        json_schema = {
            "type": "object",
            "properties": {
                "flights": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "departure_city": {"type": "string"},
                            "arrival_city": {"type": "string"},
                            "departure_date": {"type": "string"},
                            "return_date": {"type": "string", "nullable": True},
                            "airline": {"type": "string"},
                            "price": {"type": "number"}
                        }
                    }
                }
            }
        }

        builder = Jsonformer(
            model=self.model,
            tokenizer=self.tokenizer,
            json_schema=json_schema,
            prompt=prompt,
            max_string_token_length=20
        )

        print("Generating structured flight information...")
        output = builder()
        return output


def extract_structured_data(content: str, data_points: str):
    llm = HuggingFaceLLM(temperature=0)  # Initialize the Hugging Face model

    template = """
    You are an expert in flight bookings and travel plans. Your job is to extract structured flight information from the provided text.

    Flight Content:
    {content}

    Based on the above content, extract the following details:
    {data_points}
    """

    # Fill in the placeholders in the template
    formatted_template = template.format(content=content, data_points=data_points)
    results = llm.generate(formatted_template)

    return results


def read_txt_file(file_path):
    """Read content from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def main():
    default_data_points = """{
        "flights": [{
            "departure_city": "City of departure",
            "arrival_city": "City of arrival",
            "departure_date": "Date of departure in YYYY-MM-DD format",
            "return_date": "Date of return in YYYY-MM-DD format, if applicable",
            "airline": "Name of the airline",
            "price": "Price of the flight in USD"
        }]
    }"""

    st.set_page_config(page_title="Flight Information Extraction", page_icon="✈️")

    st.header("Flight Information Extraction ✈️")

    data_points = st.text_area(
        "Data Points", value=default_data_points, height=170)

    folder_path = './flight_txts'  # Replace with the folder path containing text files

    txt_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.txt')]

    results = []

    if txt_paths:
        total_start_time = time.time()
        with open("flight_results.txt", "w") as output_file:
            for txt_path in txt_paths:
                output_file.write(f"TXT Path: {txt_path}\n")
                start_time = time.time()  # Record the start time

                # Read content from the text file
                content = read_txt_file(txt_path)
                
                # Extract structured data
                data = extract_structured_data(content, default_data_points)
                json_data = json.dumps(data, indent=2)

                if isinstance(json_data, list):
                    results.extend(json_data)
                else:
                    results.append(json_data)

                end_time = time.time()  # Record the end time
                elapsed_time = end_time - start_time
                output_file.write(f"Execution time: {elapsed_time:.2f} seconds\n")
                output_file.write(f"Results: {json_data}\n\n")

            total_end_time = time.time()
            total_elapsed_time = total_end_time - total_start_time
            output_file.write(f"Total execution time: {total_elapsed_time:.2f} seconds\n")

    st.success("Flight Information Extraction Complete!")


if __name__ == '__main__':
    main()
